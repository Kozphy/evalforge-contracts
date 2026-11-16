"""Signature-only protocol for model response callables."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ModelCallResultLike(Protocol):
    """Minimal shape returned by live/offline model adapters."""

    text: str


@runtime_checkable
class ResponseFn(Protocol):
    """Callable that maps a case-like object to text or a result-like object.

    Implementations live in proprietary runners. This Protocol is the public
    boundary only — no HTTP, secrets, or prompts are defined here.
    """

    def __call__(self, case: object) -> str | ModelCallResultLike: ...
