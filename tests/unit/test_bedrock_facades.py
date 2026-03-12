from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESS_DIR = ROOT / "src" / "processes"

TARGETS = {
    "IMF.P.Dimension.Create": "}bedrock.dim.create",
    "IMF.P.Dimension.Clear": "}bedrock.dim.clone",
    "IMF.P.Dimension.CopyRelations": "}bedrock.hier.clone",
    "IMF.P.Attribute.CopyDefinitions": "}bedrock.dim.attr.create",
    "IMF.P.Log.Event": "}bedrock.server.writetomessagelog",
    "IMF.P.Security.CreateGroups": "}bedrock.security.group.create",
    "IMF.P.Security.SetCubeAccess": "}bedrock.security.object.assign",
    "IMF.P.Security.SetDimensionAccess": "}bedrock.security.object.assign",
}


def test_wave1_bedrock_json_contracts_exist() -> None:
    for process_name, bedrock_process in TARGETS.items():
        payload = json.loads((PROCESS_DIR / f"{process_name}.json").read_text(encoding="utf-8"))
        parameter_names = {parameter["Name"] for parameter in payload["Parameters"]}
        assert {"pUseBedrock", "pBedrockProcess", "pStrictBedrock"}.issubset(parameter_names)
        assert "Bedrock" in payload["tags"]
        bedrock_entry = next(parameter for parameter in payload["Parameters"] if parameter["Name"] == "pBedrockProcess")
        assert bedrock_entry["Value"] == bedrock_process


def test_wave1_bedrock_ti_files_document_delegation() -> None:
    for process_name, bedrock_process in TARGETS.items():
        source = (PROCESS_DIR / f"{process_name}.ti").read_text(encoding="utf-8")
        assert "TODO:" in source
        assert bedrock_process in source
        assert "pUseBedrock" in source
