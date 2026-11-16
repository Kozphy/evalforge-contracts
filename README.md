# evalforge-contracts

Apache-2.0 **contracts-only** package for EvalForge open-core.

This repository publishes provider-neutral interfaces and JSON schemas so other
tools (for example CI failure orchestrators) can speak EvalForge’s evaluation
vocabulary. It does **not** contain finance graders, failure taxonomies, policy
engines, golden datasets, or planted-error answer keys.

| Artifact | License |
|---|---|
| This package (`evalforge-contracts`) | **Apache-2.0** (explicit patent grant) |
| EvalForge core (graders, datasets, policy, runners) | **Proprietary** — private repository |

## Install

```bash
pip install -e ".[dev]"
pytest -q
```

## Contents

- `evalforge_contracts.control_plane` — canonical evaluation models (`schema_version` 1.0.0)
- `evalforge_contracts.gate` — Agent Reliability gate enums (`PASS` / `WARN` / `BLOCK`) and peer mapping
- `evalforge_contracts.response_fn` — `ResponseFn` Protocol (signature only)
- `evalforge_contracts.export_v1` — helpers for `evalforge.export.v1` (no prompt/response fields by default)
- `schemas/evalforge.export.v1.json` — JSON Schema

## Export contract

```json
{
  "schema_version": "evalforge.export.v1",
  "producer_revision": "<git-sha>",
  "run_id": "...",
  "results": []
}
```

`producer_revision` is metadata only (git SHA of the producing build). Prompt and
response bodies are **omitted by default**; enable them only with an explicit
opt-in in a producer that is allowed to export content.

## Not included (proprietary)

Finance graders, taxonomy, policy, judge, human-review seeds, evidence writers,
live model clients, and `finance_eval/dataset/**` remain in the private EvalForge
core and must never be copied into this public package.
