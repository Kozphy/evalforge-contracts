"""evalforge.export.v1 — redacted-by-default export envelope."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

EXPORT_SCHEMA_VERSION: Literal["evalforge.export.v1"] = "evalforge.export.v1"


class ExportResultRow(BaseModel):
    """One evaluated case row without prompt/response content by default."""

    result_id: str | None = None
    case_id: str | None = None
    external_case_id: str | None = None
    case_name: str | None = None
    expected_label: str | None = None
    predicted_label: str | None = None
    correct: bool | None = None
    confidence: float | None = None
    needs_human_review: bool | None = None
    review_status: str | None = None
    control_action: str | None = None
    release_allowed: bool | None = None
    groundedness: float | None = None
    citation_coverage: float | None = None
    retrieval_max_score: float | None = None
    grader_provider: str | None = None
    model: str | None = None
    prompt_version: str | None = None
    evaluated_at: str | None = None
    # Content fields are optional and omitted from producers by default.
    prompt: str | None = None
    response: str | None = None


class ExportEnvelope(BaseModel):
    schema_version: Literal["evalforge.export.v1"] = EXPORT_SCHEMA_VERSION
    producer_revision: str = Field(
        ...,
        description="Git SHA (or equivalent build id) of the producing revision; metadata only.",
        min_length=7,
        max_length=64,
    )
    run_id: str
    project_id: str | int | None = None
    include_content: bool = False
    results: list[ExportResultRow] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:  # noqa: ANN401
        if not self.include_content:
            for row in self.results:
                row.prompt = None
                row.response = None
