#!/usr/bin/env python3
"""Validate and deploy TM1 v12 process artifacts from this repository.

This script is intentionally conservative:
- validate local source structure before any network call
- never deploy unless --execute is supplied
- never store secrets in the repository
- support either basic auth or a caller-provided Authorization header

Current deployment scope:
- deploys processes from src/processes
- validates custom object-definition JSON files, but does not compile them
  into native TM1 dimensions or cubes yet
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROCESS_JSON_GLOB = "*.json"
TI_REGION_NAMES = ("prolog", "metadata", "data", "epilog")


class DeployError(RuntimeError):
    """Raised when validation or deployment cannot continue safely."""


@dataclass
class Config:
    base_url: str
    api_path: str
    auth_mode: str
    user: str
    password: str
    namespace: str
    authorization_header: str
    verify_ssl: bool
    timeout_s: int
    process_root: Path
    object_definition_root: Path
    deploy_processes: bool
    validate_object_definitions: bool
    process_name_prefix: str
    allow_overwrite: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and deploy TM1 v12 repo artifacts.")
    parser.add_argument(
        "command",
        choices=["validate", "plan", "deploy-processes"],
        help="validate local files, print a deployment plan, or deploy processes",
    )
    parser.add_argument(
        "--config",
        default="tools/tm1.deploy.local.json",
        help="Path to local config JSON. Safe to omit; env vars are also supported.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required for deploy-processes. Without this flag the script refuses to deploy.",
    )
    parser.add_argument(
        "--filter",
        default="",
        help="Optional substring filter on process names.",
    )
    return parser.parse_args()


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DeployError(f"Invalid JSON in {path}: {exc}") from exc


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value.strip().upper() in {"1", "Y", "YES", "TRUE", "ON"}


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise DeployError(f"Environment variable {name} must be an integer.") from exc


def load_config(config_path: Path, repo_root: Path) -> Config:
    file_config: dict[str, Any] = {}
    if config_path.exists():
        file_config = read_json_file(config_path)

    def cfg(name: str, env_name: str, default: Any) -> Any:
        if os.getenv(env_name) not in (None, ""):
            return os.getenv(env_name)
        return file_config.get(name, default)

    base_url = str(cfg("base_url", "IMF_TM1_BASE_URL", "")).rstrip("/")
    api_path = str(cfg("api_path", "IMF_TM1_API_PATH", "/api/v1"))
    auth_mode = str(cfg("auth_mode", "IMF_TM1_AUTH_MODE", "basic")).lower()
    user = str(cfg("user", "IMF_TM1_USER", ""))
    password = str(cfg("password", "IMF_TM1_PASSWORD", ""))
    namespace = str(cfg("namespace", "IMF_TM1_NAMESPACE", ""))
    authorization_header = str(cfg("authorization_header", "IMF_TM1_AUTHORIZATION_HEADER", ""))
    verify_ssl = env_bool("IMF_TM1_VERIFY_SSL", bool(file_config.get("verify_ssl", True)))
    timeout_s = env_int("IMF_TM1_TIMEOUT_S", int(file_config.get("timeout_s", 60)))
    process_root = repo_root / str(cfg("process_root", "IMF_TM1_PROCESS_ROOT", "src/processes"))
    object_definition_root = repo_root / str(
        cfg("object_definition_root", "IMF_TM1_OBJECT_DEFINITION_ROOT", "src/object-definitions")
    )
    deploy_processes = env_bool(
        "IMF_TM1_DEPLOY_PROCESSES",
        bool(file_config.get("deploy_processes", True)),
    )
    validate_object_definitions = env_bool(
        "IMF_TM1_VALIDATE_OBJECT_DEFINITIONS",
        bool(file_config.get("validate_object_definitions", True)),
    )
    process_name_prefix = str(cfg("process_name_prefix", "IMF_TM1_PROCESS_PREFIX", "IMF."))
    allow_overwrite = env_bool(
        "IMF_TM1_ALLOW_OVERWRITE",
        bool(file_config.get("allow_overwrite", True)),
    )

    return Config(
        base_url=base_url,
        api_path=api_path,
        auth_mode=auth_mode,
        user=user,
        password=password,
        namespace=namespace,
        authorization_header=authorization_header,
        verify_ssl=verify_ssl,
        timeout_s=timeout_s,
        process_root=process_root,
        object_definition_root=object_definition_root,
        deploy_processes=deploy_processes,
        validate_object_definitions=validate_object_definitions,
        process_name_prefix=process_name_prefix,
        allow_overwrite=allow_overwrite,
    )


def parse_ti_regions(ti_path: Path) -> dict[str, str]:
    lines = ti_path.read_text(encoding="utf-8").splitlines()
    sections = {name: [] for name in TI_REGION_NAMES}
    seen_regions: set[str] = set()
    current: str | None = None

    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith("#region "):
            region_name = stripped.split(maxsplit=1)[1]
            if region_name in sections:
                seen_regions.add(region_name)
            current = region_name if region_name in sections else None
            continue
        if stripped == "#endregion":
            current = None
            continue
        if current:
            sections[current].append(line)

    missing = [name for name in TI_REGION_NAMES if name not in seen_regions]
    if missing:
        raise DeployError(
            f"{ti_path} is missing one or more required TI regions: {', '.join(missing)}"
        )

    return {name: "\n".join(content).strip() for name, content in sections.items()}


def load_process_definitions(process_root: Path, name_filter: str) -> list[dict[str, Any]]:
    if not process_root.exists():
        raise DeployError(f"Process root does not exist: {process_root}")

    process_defs: list[dict[str, Any]] = []
    for json_path in sorted(process_root.glob(PROCESS_JSON_GLOB)):
        data = read_json_file(json_path)
        name = data.get("Name") or data.get("name")
        if not name or not isinstance(name, str):
            continue
        if name_filter and name_filter not in name:
            continue
        code_link = data.get("Code@Code.link")
        if not code_link:
            raise DeployError(f"Process JSON is missing Code@Code.link: {json_path}")
        ti_path = json_path.with_name(code_link)
        if not ti_path.exists():
            raise DeployError(f"Linked TI file does not exist for {json_path}: {ti_path}")

        regions = parse_ti_regions(ti_path)
        parameters = data.get("Parameters", [])
        if not isinstance(parameters, list):
            raise DeployError(f"Parameters must be a list in {json_path}")

        process_defs.append(
            {
                "name": name,
                "json_path": json_path,
                "ti_path": ti_path,
                "parameters": parameters,
                "payload": {
                    "Name": name,
                    "Parameters": parameters,
                    "PrologProcedure": regions["prolog"],
                    "MetadataProcedure": regions["metadata"],
                    "DataProcedure": regions["data"],
                    "EpilogProcedure": regions["epilog"],
                },
            }
        )

    if not process_defs:
        raise DeployError(f"No process definitions found in {process_root}")
    return process_defs


def validate_object_definitions(object_root: Path) -> list[str]:
    warnings: list[str] = []
    if not object_root.exists():
        warnings.append(f"Object-definition root does not exist: {object_root}")
        return warnings

    for json_path in sorted(object_root.rglob("*.json")):
        data = read_json_file(json_path)
        if "name" not in data:
            warnings.append(f"{json_path} does not contain a top-level 'name' field.")

    warnings.append(
        "Custom object-definition JSON files are validated only for structure here; "
        "native TM1 dimension/cube compilation is not implemented in this deploy script."
    )
    return warnings


def build_headers(config: Config) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }

    if config.authorization_header:
        headers["Authorization"] = config.authorization_header
    elif config.auth_mode == "basic":
        if not config.user or not config.password:
            raise DeployError(
                "Basic auth selected but IMF_TM1_USER / IMF_TM1_PASSWORD are not set."
            )
        token = base64.b64encode(f"{config.user}:{config.password}".encode("utf-8")).decode("ascii")
        headers["Authorization"] = f"Basic {token}"
    else:
        raise DeployError(
            "Unsupported auth mode. Use auth_mode='basic' or supply IMF_TM1_AUTHORIZATION_HEADER."
        )

    if config.namespace:
        headers["CAMNamespace"] = config.namespace

    return headers


def build_ssl_context(verify_ssl: bool) -> ssl.SSLContext:
    if verify_ssl:
        return ssl.create_default_context()
    return ssl._create_unverified_context()  # noqa: SLF001


class TM1RestClient:
    def __init__(self, config: Config):
        if not config.base_url:
            raise DeployError("Missing TM1 base URL. Set IMF_TM1_BASE_URL or use a local config file.")
        self.config = config
        self.base_api_url = f"{config.base_url}{config.api_path}"
        self.headers = build_headers(config)
        self.ssl_context = build_ssl_context(config.verify_ssl)

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        expected_statuses: tuple[int, ...] = (200,),
    ) -> tuple[int, Any]:
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        url = f"{self.base_api_url}{path}"
        request = urllib.request.Request(url=url, data=body, method=method.upper())
        for key, value in self.headers.items():
            request.add_header(key, value)

        try:
            with urllib.request.urlopen(
                request,
                context=self.ssl_context,
                timeout=self.config.timeout_s,
            ) as response:
                status = response.getcode()
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            status = exc.code
            raw = exc.read().decode("utf-8", errors="replace")
            if status not in expected_statuses:
                raise DeployError(f"{method} {url} failed with HTTP {status}: {raw}") from exc
            return status, raw
        except urllib.error.URLError as exc:
            raise DeployError(f"Could not reach TM1 endpoint {url}: {exc}") from exc

        if status not in expected_statuses:
            raise DeployError(f"{method} {url} returned unexpected HTTP {status}: {raw}")

        if not raw.strip():
            return status, None
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, raw

    def ping(self) -> None:
        self.request("GET", "/Configuration", expected_statuses=(200,))

    def process_exists(self, process_name: str) -> bool:
        escaped = process_name.replace("'", "''")
        path = f"/Processes('{urllib.parse.quote(escaped, safe='')}')?$select=Name"
        status, _ = self.request("GET", path, expected_statuses=(200, 404))
        return status == 200

    def create_process(self, payload: dict[str, Any]) -> None:
        self.request("POST", "/Processes", payload=payload, expected_statuses=(201, 204))

    def update_process(self, process_name: str, payload: dict[str, Any]) -> None:
        escaped = process_name.replace("'", "''")
        path = f"/Processes('{urllib.parse.quote(escaped, safe='')}')"
        self.request("PATCH", path, payload=payload, expected_statuses=(204,))


def print_plan(process_defs: list[dict[str, Any]], object_warnings: list[str]) -> None:
    print(f"Processes discovered: {len(process_defs)}")
    if process_defs:
        print(f"First process: {process_defs[0]['name']}")
        print(f"Last process:  {process_defs[-1]['name']}")
    print("")
    print("Object-definition validation:")
    for warning in object_warnings:
        print(f"- {warning}")


def deploy_processes(config: Config, process_defs: list[dict[str, Any]]) -> None:
    client = TM1RestClient(config)
    client.ping()
    print(f"Connected to {config.base_url}{config.api_path}")

    created = 0
    updated = 0
    skipped = 0

    for process_def in process_defs:
        name = process_def["name"]
        payload = process_def["payload"]
        exists = client.process_exists(name)

        if exists and not config.allow_overwrite:
            skipped += 1
            print(f"SKIP  {name} (already exists, allow_overwrite=false)")
            continue

        if exists:
            client.update_process(name, payload)
            updated += 1
            print(f"PATCH {name}")
        else:
            client.create_process(payload)
            created += 1
            print(f"POST  {name}")

    print("")
    print(f"Deployment complete. created={created} updated={updated} skipped={skipped}")


def validate_config_for_deploy(config: Config) -> None:
    if not config.deploy_processes:
        raise DeployError("deploy_processes=false in config; refusing to deploy.")
    if not config.base_url:
        raise DeployError("Missing TM1 base URL. Set IMF_TM1_BASE_URL or use --config.")
    if not config.process_name_prefix:
        raise DeployError("process_name_prefix must not be empty.")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo_root / config_path

    try:
        config = load_config(config_path=config_path, repo_root=repo_root)
        process_defs = load_process_definitions(config.process_root, args.filter)
        process_defs = [
            process_def
            for process_def in process_defs
            if process_def["name"].startswith(config.process_name_prefix)
        ]
        if not process_defs:
            raise DeployError(
                f"No process definitions matched prefix '{config.process_name_prefix}' in {config.process_root}"
            )

        object_warnings = []
        if config.validate_object_definitions:
            object_warnings = validate_object_definitions(config.object_definition_root)

        if args.command == "validate":
            print_plan(process_defs, object_warnings)
            print("")
            print("Validation successful. No remote calls were made.")
            return 0

        if args.command == "plan":
            print_plan(process_defs, object_warnings)
            print("")
            print("Plan complete. Deploy command still requires --execute.")
            return 0

        validate_config_for_deploy(config)
        if not args.execute:
            raise DeployError("Refusing to deploy without --execute.")

        deploy_processes(config, process_defs)
        if object_warnings:
            print("")
            print("Post-deploy warnings:")
            for warning in object_warnings:
                print(f"- {warning}")
        return 0
    except DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
