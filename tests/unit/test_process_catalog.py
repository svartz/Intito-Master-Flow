from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESS_DIR = ROOT / "src" / "processes"
REQUIRED_JSON_KEYS = {"Name", "name", "Purpose", "purpose", "Parameters", "parameters", "Prolog", "prolog", "Metadata", "metadata", "tags", "environmentScope", "Code@Code.link"}


def test_each_process_has_matching_ti_and_json() -> None:
    ti_files = sorted(PROCESS_DIR.glob("IMF.P*.ti"))
    assert ti_files, "Expected IMF process files"
    for ti in ti_files:
        json_path = ti.with_suffix(".json")
        assert json_path.exists(), f"Missing JSON pair for {ti.name}"


def test_json_contract_fields_present() -> None:
    for json_path in sorted(PROCESS_DIR.glob("IMF.P*.json")):
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        missing = REQUIRED_JSON_KEYS - payload.keys()
        assert not missing, f"{json_path.name} missing keys: {sorted(missing)}"
        assert payload["Code@Code.link"] == json_path.with_suffix(".ti").name
        assert payload["environmentScope"] == ["DEV", "TEST", "PROD"]
