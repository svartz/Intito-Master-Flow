#!/usr/bin/env python3
"""Validate and package IMF PAW workbook specs into a deterministic deploy bundle."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class PawDeployError(RuntimeError):
    """Raised when PAW bundle validation fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and package IMF PAW workbook specs.")
    parser.add_argument(
        "command",
        choices=["validate", "plan", "build-bundle"],
        help="Validate specs, print the deployment plan, or build a deterministic bundle.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--workbook",
        default="IMF.PAW.MasterFlow",
        help="Workbook spec name to validate/package.",
    )
    parser.add_argument(
        "--output",
        default="build/paw",
        help="Bundle output directory for build-bundle.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PawDeployError(f"Invalid JSON in {path}: {exc}") from exc


def load_spec(repo_root: Path, file_name: str) -> dict[str, Any]:
    path = repo_root / "src" / "paw-reports" / file_name
    if not path.exists():
        raise PawDeployError(f"Missing PAW spec: {path}")
    return read_json(path)


def load_workbook_bundle(repo_root: Path, workbook_name: str) -> dict[str, Any]:
    workbook = load_spec(repo_root, f"{workbook_name}.Workbook.json")
    action_spec = load_spec(repo_root, f"{workbook_name}.Actions.json")
    subset_spec = load_spec(repo_root, f"{workbook_name}.Subsets.json")
    view_spec = load_spec(repo_root, f"{workbook_name}.Views.json")
    runtime_spec = load_spec(repo_root, f"{workbook_name}.Runtime.json")
    layout_spec = load_spec(repo_root, f"{workbook_name}.Layout.json")
    deployment_spec = load_spec(repo_root, f"{workbook_name}.Deployment.json")
    return {
        "workbook": workbook,
        "actions": action_spec,
        "subsets": subset_spec,
        "views": view_spec,
        "runtime": runtime_spec,
        "layout": layout_spec,
        "deployment": deployment_spec,
    }


def validate_bundle(repo_root: Path, bundle: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    workbook = bundle["workbook"]
    actions = bundle["actions"]
    subsets = bundle["subsets"]
    views = bundle["views"]
    runtime = bundle["runtime"]
    layout = bundle["layout"]
    deployment = bundle["deployment"]

    tab_ids = {tab["Id"] for tab in workbook.get("Tabs", [])}
    layout_tab_ids = {page["TabId"] for page in layout.get("Pages", [])}
    missing_layout_tabs = sorted(tab_ids - layout_tab_ids)
    if missing_layout_tabs:
        raise PawDeployError(f"Layout spec is missing tabs: {', '.join(missing_layout_tabs)}")

    view_names = {item["Name"] for item in views.get("Views", [])}
    runtime_views = set(runtime.get("PublicViews", []))

    subset_names = {item["Name"] for item in subsets.get("Subsets", [])}
    runtime_subsets = set(runtime.get("PublicSubsets", []))
    missing_runtime_subsets = sorted(
        name
        for name in subset_names
        if name.startswith("IMF.PAW.SS.") and name not in runtime_subsets
    )
    if missing_runtime_subsets:
        warnings.append(
            "Subsets not included in runtime public subsets: " + ", ".join(missing_runtime_subsets)
        )

    action_ids = {item["Id"] for item in actions.get("Actions", [])}
    for page in layout.get("Pages", []):
        for widget in page.get("Widgets", []):
            if widget.get("Type") == "action-bar":
                for action_id in widget.get("Actions", []):
                    if action_id not in action_ids:
                        raise PawDeployError(
                            f"Layout references unknown action '{action_id}' on page '{page['TabId']}'."
                        )
            view_name = widget.get("View")
            if view_name and view_name not in view_names and view_name not in runtime_views:
                raise PawDeployError(
                    f"Layout references unknown view '{view_name}' on page '{page['TabId']}'."
                )

    deployment_dependencies = deployment.get("Dependencies", {})
    expected_dependencies = {
        "RuntimeSpec": f"{workbook['Name']}.Runtime",
        "LayoutSpec": f"{workbook['Name']}.Layout",
        "ActionSpec": f"{workbook['Name']}.Actions",
        "ViewSpec": f"{workbook['Name']}.Views",
        "SubsetSpec": f"{workbook['Name']}.Subsets",
    }
    for key, expected_value in expected_dependencies.items():
        if deployment_dependencies.get(key) != expected_value:
            raise PawDeployError(
                f"Deployment spec dependency {key} must be '{expected_value}'."
            )

    builder_process = runtime.get("BuilderProcess", "")
    if not builder_process:
        raise PawDeployError("Runtime spec must declare BuilderProcess.")
    process_path = repo_root / "src" / "processes" / f"{builder_process}.json"
    if not process_path.exists():
        raise PawDeployError(f"Runtime builder process does not exist: {process_path}")

    return warnings


def build_bundle_file(output_dir: Path, bundle: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    workbook_name = bundle["workbook"]["Name"]
    output_path = output_dir / f"{workbook_name}.bundle.json"
    output_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return output_path


def print_plan(bundle: dict[str, Any], warnings: list[str]) -> None:
    workbook = bundle["workbook"]
    runtime = bundle["runtime"]
    layout = bundle["layout"]
    print(f"Workbook: {workbook['Name']}")
    print(f"Tabs: {len(workbook.get('Tabs', []))}")
    print(f"Runtime subsets: {len(runtime.get('PublicSubsets', []))}")
    print(f"Runtime views: {len(runtime.get('PublicViews', []))}")
    print(f"Layout pages: {len(layout.get('Pages', []))}")
    if warnings:
        print("")
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    try:
        bundle = load_workbook_bundle(repo_root, args.workbook)
        warnings = validate_bundle(repo_root, bundle)
        if args.command == "validate":
            print_plan(bundle, warnings)
            print("")
            print("Validation successful.")
            return 0
        if args.command == "plan":
            print_plan(bundle, warnings)
            print("")
            print("Plan complete.")
            return 0

        output_path = build_bundle_file(repo_root / args.output, bundle)
        print_plan(bundle, warnings)
        print("")
        print(f"Bundle written to {output_path}")
        return 0
    except PawDeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
