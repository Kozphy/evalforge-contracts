from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from evalforge_contracts.control_plane import (
    SCHEMA_VERSION,
    EvaluationResult,
    ExperimentSpec,
    PolicyDecisionType,
)
from evalforge_contracts.export_v1 import EXPORT_SCHEMA_VERSION, ExportEnvelope, ExportResultRow
from evalforge_contracts.gate import (
    BRIDGE_INTERFACE_ID,
    GateDecision,
    map_to_ci_failure_orchestrator,
)
from evalforge_contracts.response_fn import ResponseFn


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "evalforge.export.v1.json"


def test_gate_mapping() -> None:
    assert map_to_ci_failure_orchestrator(GateDecision.PASS) == "APPROVE"
    assert map_to_ci_failure_orchestrator(GateDecision.WARN) == "ESCALATE"
    assert map_to_ci_failure_orchestrator(GateDecision.BLOCK) == "REJECT"
    assert BRIDGE_INTERFACE_ID == "evalforge.ci_failure_bridge"


def test_control_plane_models_roundtrip() -> None:
    spec = ExperimentSpec(name="demo", dataset_id="synthetic-empty")
    assert spec.schema_version == SCHEMA_VERSION
    result = EvaluationResult(
        run_id="run_1",
        experiment_id=spec.experiment_id,
        evaluator_name="heuristic",
        metric_name="accuracy",
        score=1.0,
        passed=True,
    )
    assert result.schema_version == SCHEMA_VERSION
    assert PolicyDecisionType.ALLOW.value == "ALLOW"


def test_export_strips_content_by_default() -> None:
    envelope = ExportEnvelope(
        producer_revision="1143a7e2abd969a94e13d9ca9391479511e63f75",
        run_id="1",
        include_content=False,
        results=[
            ExportResultRow(
                case_id="c1",
                predicted_label="pass",
                prompt="SECRET PROMPT",
                response="SECRET RESPONSE",
            )
        ],
    )
    assert envelope.schema_version == EXPORT_SCHEMA_VERSION
    assert envelope.results[0].prompt is None
    assert envelope.results[0].response is None


def test_export_schema_validates_fixture() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    payload = {
        "schema_version": "evalforge.export.v1",
        "producer_revision": "1143a7e2abd969a94e13d9ca9391479511e63f75",
        "run_id": "run_demo",
        "include_content": False,
        "results": [
            {
                "case_id": "fixture-001",
                "expected_label": "pass",
                "predicted_label": "pass",
                "correct": True,
                "control_action": "allow",
                "release_allowed": True,
            }
        ],
    }
    jsonschema.validate(payload, schema)


def test_response_fn_protocol_is_callable_shape() -> None:
    def sample(case: object) -> str:
        return "ok"

    assert isinstance(sample, ResponseFn)


def test_synthetic_fixture_has_no_answer_key() -> None:
    fixture = ROOT / "tests" / "fixtures" / "synthetic_case.json"
    data = json.loads(fixture.read_text(encoding="utf-8"))
    assert "planted_failure" not in data
    assert "expected_answer" not in data
    assert "candidate_response" not in data
    assert data["case_id"] == "contracts-synth-001"
