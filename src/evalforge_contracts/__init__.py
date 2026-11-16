"""EvalForge public contracts (Apache-2.0)."""

from __future__ import annotations

from evalforge_contracts.control_plane import SCHEMA_VERSION
from evalforge_contracts.gate import (
    BRIDGE_INTERFACE_ID,
    BRIDGE_INTERFACE_VERSION,
    GateDecision,
    map_to_ci_failure_orchestrator,
)
from evalforge_contracts.response_fn import ModelCallResultLike, ResponseFn

__version__ = "0.1.0"

__all__ = [
    "SCHEMA_VERSION",
    "BRIDGE_INTERFACE_ID",
    "BRIDGE_INTERFACE_VERSION",
    "GateDecision",
    "map_to_ci_failure_orchestrator",
    "ModelCallResultLike",
    "ResponseFn",
    "__version__",
]
