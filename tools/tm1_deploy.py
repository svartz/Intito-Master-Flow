#!/usr/bin/env python3
"""Validate and deploy TM1 v12 IMF artifacts from this repository.

This script is intentionally conservative:
- validate local source structure before any network call
- never deploy unless --execute is supplied
- never store secrets in the repository
- support either basic auth or a caller-provided Authorization header

Current deployment scope:
- deploys processes from src/processes
- deploys custom IMF object definitions from src/object-definitions into
  native TM1 dimensions and cubes
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
STRING_ESCAPE = "\\'"


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
    parser = argparse.ArgumentParser(description="Validate and deploy TM1 v12 IMF artifacts.")
    parser.add_argument(
        "command",
        choices=["validate", "plan", "deploy-processes", "deploy-objects"],
        help="validate local files, print a deployment plan, deploy processes, or deploy native objects",
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
    parser.add_argument(
        "--deploy-objects",
        action="store_true",
        help="When used with deploy-processes, deploy native object definitions after processes.",
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
    api_path = str(cfg("api_path", "IMF_TM1_API_PATH", "/api/v1")).strip()
    if api_path in {".", "/"}:
        api_path = ""
    elif api_path and not api_path.startswith("/"):
        api_path = f"/{api_path}"
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
        sanitized_parameters: list[dict[str, Any]] = []
        for parameter in parameters:
            if not isinstance(parameter, dict):
                raise DeployError(f"Each parameter must be an object in {json_path}")
            sanitized_parameter = {
                key: parameter[key]
                for key in ("Name", "Prompt", "Value")
                if key in parameter
            }
            if "Name" not in sanitized_parameter:
                raise DeployError(f"Parameter missing Name in {json_path}")
            sanitized_parameters.append(sanitized_parameter)

        process_defs.append(
            {
                "name": name,
                "json_path": json_path,
                "ti_path": ti_path,
                "parameters": sanitized_parameters,
                "payload": {
                    "Name": name,
                    "Parameters": sanitized_parameters,
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
    return warnings


def load_object_definitions(object_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not object_root.exists():
        raise DeployError(f"Object-definition root does not exist: {object_root}")

    dimension_defs: list[dict[str, Any]] = []
    cube_defs: list[dict[str, Any]] = []

    for json_path in sorted(object_root.rglob("*.json")):
        data = read_json_file(json_path)
        name = data.get("name")
        kind = data.get("kind")
        if not name or not isinstance(name, str):
            raise DeployError(f"Object-definition missing valid 'name': {json_path}")
        if not kind or not isinstance(kind, str):
            raise DeployError(f"Object-definition missing valid 'kind': {json_path}")
        record = {"path": json_path, "name": name, "kind": kind, "data": data}
        if "dimension" in kind:
            dimension_defs.append(record)
        elif "cube" in kind:
            cube_defs.append(record)
        else:
            raise DeployError(f"Unsupported object kind '{kind}' in {json_path}")

    if not dimension_defs and not cube_defs:
        raise DeployError(f"No object definitions found in {object_root}")

    return dimension_defs, cube_defs


def tm1_element_type(element_type: str) -> str:
    normalized = element_type.strip().upper()
    mapping = {
        "N": "Numeric",
        "NUMERIC": "Numeric",
        "S": "String",
        "STRING": "String",
        "C": "Consolidated",
        "CONSOLIDATED": "Consolidated",
    }
    if normalized not in mapping:
        raise DeployError(f"Unsupported element type '{element_type}' in object definition.")
    return mapping[normalized]


def tm1_attribute_type(attribute_type: str) -> str:
    normalized = attribute_type.strip().lower()
    mapping = {
        "string": "String",
        "numeric": "Numeric",
        "number": "Numeric",
        "alias": "Alias",
    }
    if normalized not in mapping:
        raise DeployError(f"Unsupported attribute type '{attribute_type}' in object definition.")
    return mapping[normalized]


def ti_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", STRING_ESCAPE)


def build_headers(config: Config) -> dict[str, str]:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
    }
    parsed_base = urllib.parse.urlparse(config.base_url)
    origin = f"{parsed_base.scheme}://{parsed_base.netloc}"
    headers["Origin"] = origin
    headers["Referer"] = f"{origin}/"

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
        self.base_api_url = f"{config.base_url}{config.api_path}".rstrip("/")
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
        self.request("GET", "/Processes?$top=1", expected_statuses=(200,))

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

    def delete_process(self, process_name: str) -> None:
        escaped = process_name.replace("'", "''")
        path = f"/Processes('{urllib.parse.quote(escaped, safe='')}')"
        self.request("DELETE", path, expected_statuses=(204, 404))

    def execute_process(self, process_name: str) -> None:
        escaped = process_name.replace("'", "''")
        path = f"/Processes('{urllib.parse.quote(escaped, safe='')}')/tm1.Execute"
        self.request("POST", path, payload={}, expected_statuses=(204,))

    def dimension_exists(self, dimension_name: str) -> bool:
        escaped = dimension_name.replace("'", "''")
        path = f"/Dimensions('{urllib.parse.quote(escaped, safe='')}')?$select=Name"
        status, _ = self.request("GET", path, expected_statuses=(200, 404))
        return status == 200

    def create_dimension(self, dimension_name: str) -> None:
        self.request("POST", "/Dimensions", payload={"Name": dimension_name}, expected_statuses=(201,))

    def create_hierarchy(self, dimension_name: str, hierarchy_name: str) -> None:
        escaped = dimension_name.replace("'", "''")
        path = f"/Dimensions('{urllib.parse.quote(escaped, safe='')}')/Hierarchies"
        self.request("POST", path, payload={"Name": hierarchy_name}, expected_statuses=(201,))

    def get_hierarchy_snapshot(self, dimension_name: str, hierarchy_name: str) -> dict[str, Any]:
        escaped_dimension = dimension_name.replace("'", "''")
        escaped_hierarchy = hierarchy_name.replace("'", "''")
        path = (
            f"/Dimensions('{urllib.parse.quote(escaped_dimension, safe='')}')"
            f"/Hierarchies('{urllib.parse.quote(escaped_hierarchy, safe='')}')"
            "?$expand=Elements,Edges,ElementAttributes"
        )
        _, payload = self.request("GET", path, expected_statuses=(200,))
        if not isinstance(payload, dict):
            raise DeployError(f"Unexpected hierarchy payload for {dimension_name}:{hierarchy_name}")
        return payload

    def create_element(self, dimension_name: str, hierarchy_name: str, element_name: str, element_type: str) -> None:
        escaped_dimension = dimension_name.replace("'", "''")
        escaped_hierarchy = hierarchy_name.replace("'", "''")
        path = (
            f"/Dimensions('{urllib.parse.quote(escaped_dimension, safe='')}')"
            f"/Hierarchies('{urllib.parse.quote(escaped_hierarchy, safe='')}')/Elements"
        )
        self.request(
            "POST",
            path,
            payload={"Name": element_name, "Type": element_type},
            expected_statuses=(201,),
        )

    def create_edge(self, dimension_name: str, hierarchy_name: str, parent_name: str, component_name: str, weight: float) -> None:
        escaped_dimension = dimension_name.replace("'", "''")
        escaped_hierarchy = hierarchy_name.replace("'", "''")
        path = (
            f"/Dimensions('{urllib.parse.quote(escaped_dimension, safe='')}')"
            f"/Hierarchies('{urllib.parse.quote(escaped_hierarchy, safe='')}')/Edges"
        )
        self.request(
            "POST",
            path,
            payload={"ParentName": parent_name, "ComponentName": component_name, "Weight": weight},
            expected_statuses=(201,),
        )

    def create_element_attribute(self, dimension_name: str, hierarchy_name: str, attribute_name: str, attribute_type: str) -> None:
        escaped_dimension = dimension_name.replace("'", "''")
        escaped_hierarchy = hierarchy_name.replace("'", "''")
        path = (
            f"/Dimensions('{urllib.parse.quote(escaped_dimension, safe='')}')"
            f"/Hierarchies('{urllib.parse.quote(escaped_hierarchy, safe='')}')/ElementAttributes"
        )
        self.request(
            "POST",
            path,
            payload={"Name": attribute_name, "Type": attribute_type},
            expected_statuses=(201,),
        )

    def cube_exists(self, cube_name: str) -> bool:
        escaped = cube_name.replace("'", "''")
        path = f"/Cubes('{urllib.parse.quote(escaped, safe='')}')?$select=Name"
        status, _ = self.request("GET", path, expected_statuses=(200, 404))
        return status == 200

    def create_cube(self, cube_name: str, dimensions: list[str]) -> None:
        binds = [f"Dimensions('{dimension_name}')" for dimension_name in dimensions]
        payload = {"Name": cube_name, "Dimensions@odata.bind": binds}
        self.request("POST", "/Cubes", payload=payload, expected_statuses=(201,))


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


def deploy_dimensions(client: TM1RestClient, dimension_defs: list[dict[str, Any]]) -> None:
    created = 0
    updated = 0

    for definition in dimension_defs:
        data = definition["data"]
        dimension_name = definition["name"]
        hierarchy = data.get("hierarchy", {})
        hierarchy_name = str(hierarchy.get("name") or dimension_name)
        root_name = hierarchy.get("root")
        seed_elements = hierarchy.get("seedElements", [])
        attributes = data.get("attributes", [])

        if not client.dimension_exists(dimension_name):
            client.create_dimension(dimension_name)
            created += 1
            print(f"POST  dimension {dimension_name}")
        else:
            print(f"KEEP  dimension {dimension_name}")

        try:
            snapshot = client.get_hierarchy_snapshot(dimension_name, hierarchy_name)
        except DeployError:
            client.create_hierarchy(dimension_name, hierarchy_name)
            updated += 1
            print(f"POST  hierarchy {dimension_name}:{hierarchy_name}")
            snapshot = client.get_hierarchy_snapshot(dimension_name, hierarchy_name)

        existing_elements = {
            element.get("Name")
            for element in snapshot.get("Elements", [])
            if isinstance(element, dict) and element.get("Name")
        }
        existing_edges = {
            (
                edge.get("ParentName"),
                edge.get("ComponentName"),
                float(edge.get("Weight", 1)),
            )
            for edge in snapshot.get("Edges", [])
            if isinstance(edge, dict)
        }
        existing_attributes = {
            attribute.get("Name")
            for attribute in snapshot.get("ElementAttributes", [])
            if isinstance(attribute, dict) and attribute.get("Name")
        }

        if root_name and root_name not in existing_elements:
            client.create_element(dimension_name, hierarchy_name, root_name, "Consolidated")
            existing_elements.add(root_name)
            updated += 1
            print(f"POST  element {dimension_name}:{root_name}")

        for element in seed_elements:
            element_name = element["name"]
            element_type = tm1_element_type(str(element.get("type", "N")))
            if element_name not in existing_elements:
                client.create_element(dimension_name, hierarchy_name, element_name, element_type)
                existing_elements.add(element_name)
                updated += 1
                print(f"POST  element {dimension_name}:{element_name}")

        for element in seed_elements:
            parent_name = element.get("parent")
            if not parent_name:
                continue
            weight = float(element.get("weight", 1))
            edge_key = (parent_name, element["name"], weight)
            if edge_key not in existing_edges:
                client.create_edge(dimension_name, hierarchy_name, parent_name, element["name"], weight)
                existing_edges.add(edge_key)
                updated += 1
                print(f"POST  edge {dimension_name}:{parent_name}->{element['name']}")

        for attribute in attributes:
            attribute_name = attribute["name"]
            attribute_type = tm1_attribute_type(str(attribute.get("type", "string")))
            if attribute_name not in existing_attributes:
                client.create_element_attribute(dimension_name, hierarchy_name, attribute_name, attribute_type)
                existing_attributes.add(attribute_name)
                updated += 1
                print(f"POST  attribute {dimension_name}:{attribute_name}")

    print("")
    print(f"Dimension deployment complete. created={created} updated={updated}")


def deploy_cubes(client: TM1RestClient, cube_defs: list[dict[str, Any]]) -> None:
    created = 0

    for definition in cube_defs:
        cube_name = definition["name"]
        dimensions = definition["data"].get("dimensions", [])
        if not isinstance(dimensions, list) or not dimensions:
            raise DeployError(f"Cube {cube_name} must define a non-empty dimensions list.")
        if client.cube_exists(cube_name):
            print(f"KEEP  cube {cube_name}")
            continue
        client.create_cube(cube_name, [str(name) for name in dimensions])
        created += 1
        print(f"POST  cube {cube_name}")

    print("")
    print(f"Cube deployment complete. created={created}")


def build_seed_process_payload(process_name: str, statements: list[str]) -> dict[str, Any]:
    prolog_lines = [
        "#region prolog",
        f"# Generated seed process: {process_name}",
        "#endregion",
        "",
        "#region metadata",
        "#endregion",
        "",
        "#region data",
        "#endregion",
        "",
        "#region epilog",
    ]
    prolog_lines.extend(statements)
    prolog_lines.append("#endregion")
    regions = parse_ti_regions_from_text("\n".join(prolog_lines))
    return {
        "Name": process_name,
        "Parameters": [],
        "PrologProcedure": regions["prolog"],
        "MetadataProcedure": regions["metadata"],
        "DataProcedure": regions["data"],
        "EpilogProcedure": regions["epilog"],
    }


def parse_ti_regions_from_text(text: str) -> dict[str, str]:
    lines = text.splitlines()
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
        raise DeployError(f"Generated TI text is missing required regions: {', '.join(missing)}")

    return {name: "\n".join(content).strip() for name, content in sections.items()}


def deploy_seed_data(client: TM1RestClient, cube_defs: list[dict[str, Any]]) -> None:
    statements: list[str] = []
    process_name = "ZZZ.Codex.Seed.IMF.Objects"

    for definition in cube_defs:
        cube_name = definition["name"]
        seed_data = definition["data"].get("seedData", [])
        if not isinstance(seed_data, list):
            raise DeployError(f"Cube {cube_name} seedData must be a list.")
        for seed in seed_data:
            intersection = seed.get("intersection", [])
            if not isinstance(intersection, list) or not intersection:
                raise DeployError(f"Cube {cube_name} has invalid seedData intersection.")
            coordinates = ", ".join(f"'{ti_escape(str(item))}'" for item in intersection)
            value = seed.get("value")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                statements.append(f"CellPutN({value}, '{ti_escape(cube_name)}', {coordinates});")
            else:
                statements.append(
                    f"CellPutS('{ti_escape(str(value))}', '{ti_escape(cube_name)}', {coordinates});"
                )

    if not statements:
        print("No cube seed data to apply.")
        return

    payload = build_seed_process_payload(process_name, statements)
    if client.process_exists(process_name):
        client.delete_process(process_name)
    client.create_process(payload)
    try:
        client.execute_process(process_name)
        print(f"EXEC  seed-data {process_name}")
    finally:
        client.delete_process(process_name)
        print(f"DELETE seed-data {process_name}")


def deploy_objects(config: Config, dimension_defs: list[dict[str, Any]], cube_defs: list[dict[str, Any]]) -> None:
    client = TM1RestClient(config)
    client.ping()
    print(f"Connected to {config.base_url}{config.api_path}")
    deploy_dimensions(client, dimension_defs)
    deploy_cubes(client, cube_defs)
    deploy_seed_data(client, cube_defs)


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
        dimension_defs: list[dict[str, Any]] = []
        cube_defs: list[dict[str, Any]] = []
        if config.validate_object_definitions:
            object_warnings = validate_object_definitions(config.object_definition_root)
            dimension_defs, cube_defs = load_object_definitions(config.object_definition_root)

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

        if args.command == "deploy-objects":
            deploy_objects(config, dimension_defs, cube_defs)
        else:
            deploy_processes(config, process_defs)
            if args.deploy_objects:
                deploy_objects(config, dimension_defs, cube_defs)
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
