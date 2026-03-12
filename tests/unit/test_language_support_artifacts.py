from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESS_DIR = ROOT / "src" / "processes"
OBJECT_DIR = ROOT / "src" / "object-definitions"
REGISTER_PATH = ROOT / "docs" / "architecture" / "IMF_Language_Key_Register.csv"

EXPECTED_PROCESSES = {
    "IMF.P.Text.Resolve",
    "IMF.P.Text.ResolveWithFallback",
    "IMF.P.Text.ValidateCoverage",
    "IMF.P.Text.ReportMissing",
    "IMF.P.Text.Export",
    "IMF.P.Text.Import",
    "IMF.P.Text.Init",
}

EXPECTED_LOCALES = ["en-US", "sv-SE", "fi-FI", "sv-FI", "no-NO", "da-DK", "de-DE"]


def test_language_processes_exist_with_pairs() -> None:
    for process_name in EXPECTED_PROCESSES:
        ti_path = PROCESS_DIR / f"{process_name}.ti"
        json_path = PROCESS_DIR / f"{process_name}.json"
        assert ti_path.exists(), f"Missing TI file for {process_name}"
        assert json_path.exists(), f"Missing JSON file for {process_name}"


def test_language_process_json_tags_are_consistent() -> None:
    for process_name in EXPECTED_PROCESSES:
        payload = json.loads((PROCESS_DIR / f"{process_name}.json").read_text(encoding="utf-8"))
        assert {"IMF", "TM1", "PAW", "v12", "Language"}.issubset(payload["tags"])


def test_fallback_and_missing_marker_are_declared() -> None:
    payload = json.loads((PROCESS_DIR / "IMF.P.Text.ResolveWithFallback.json").read_text(encoding="utf-8"))
    assert "en-US" in payload["prolog"]
    assert "[missing:" in payload["prolog"]


def test_language_dimension_matches_supported_locales() -> None:
    payload = json.loads((OBJECT_DIR / "dimensions" / "IMF.D.Language.json").read_text(encoding="utf-8"))
    seed_names = [item["name"] for item in payload["hierarchy"]["seedElements"]]
    assert seed_names == EXPECTED_LOCALES


def test_text_key_register_is_seeded_in_dimension_definition() -> None:
    register_keys: list[str] = []
    with REGISTER_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            register_keys.append(row["Key"])

    payload = json.loads((OBJECT_DIR / "dimensions" / "IMF.D.TextKey.json").read_text(encoding="utf-8"))
    seed_names = [item["name"] for item in payload["hierarchy"]["seedElements"]]
    assert seed_names == register_keys


def test_technical_object_names_are_not_translation_keys() -> None:
    payload = json.loads((OBJECT_DIR / "dimensions" / "IMF.D.TextKey.json").read_text(encoding="utf-8"))
    for item in payload["hierarchy"]["seedElements"]:
        assert not item["name"].startswith(("IMF.P.", "IMF.C.", "IMF.D."))
