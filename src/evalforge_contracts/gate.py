"""Agent Reliability / CI-failure peer gate vocabulary (enums only)."""

from __future__ import annotations

from enum import Enum

BRIDGE_INTERFACE_ID = "evalforge.ci_failure_bridge"
BRIDGE_INTERFACE_VERSION = "1.0.0"

# Peer vocabulary documented for ci-failure-orchestrator (not imported).
CFO_APPROVE = "APPROVE"
CFO_REJECT = "REJECT"
CFO_ESCALATE = "ESCALATE"


class GateDecision(str, Enum):
    """Local-first reliability gate decision."""

    PASS = "PASS"
    WARN = "WARN"
    BLOCK = "BLOCK"


def map_to_ci_failure_orchestrator(decision: GateDecision) -> str:
    """Map EvalForge gate decisions onto ci-failure-orchestrator outcomes."""
    if decision is GateDecision.PASS:
        return CFO_APPROVE
    if decision is GateDecision.WARN:
        return CFO_ESCALATE
    if decision is GateDecision.BLOCK:
        return CFO_REJECT
    raise AssertionError(f"unhandled decision: {decision!r}")
