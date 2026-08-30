# Refinement Validation Report

Snapshot: 2026-08-30.

## Executed checks

The refinement package is designed to run these gates in CI and locally: Python compilation for the router/site tools; JSON parsing and JSON-Schema validation of task/state examples; YAML parsing of policy/model configs and skill frontmatter; site generation; internal-link validation; HTML alternate-link checks; accessibility checks for generated SVG title/description; agent-manifest hash validation; and router smoke/regression tests.

During refinement, these checks found real defects rather than merely confirming the design: invalid YAML frontmatter caused by an unquoted colon; incomplete SVG accessibility metadata; insufficient warning that a policy example is not enforcement; and an overbroad privacy regex that treated the vocabulary word “PII” as sensitive payload. Those findings were corrected in the refined source.

## Latest executed local gate

On the publication candidate, the following checks passed in the available Linux/x86-64 validation runtime (not the target M3 Max):

- Python compilation for the router and site tools;
- Draft 2020-12 schema validation for both schemas and both worked examples;
- YAML parsing for policy/model configs and sliced-skill frontmatter;
- exactly eight uplift phase slices discovered;
- generation and validation of 16 human HTML pages plus agent discovery/contract endpoints;
- internal site links, Markdown alternates, `llms.txt` alternates, JSON parse checks and SVG title/description checks;
- rules-router smoke corpus: **1.000 accuracy, 1.000 macro-F1, 1.000 determinism**, zero `local_only -> cloud`, `glm -> deepseek`, or `deepseek -> glm` high-severity errors over three repeats; warm routing p50 was approximately **0.013 ms** and p95 approximately **0.022 ms** in this runtime.

These numbers only validate deterministic regression behavior. They are **not** claims about M3 Max latency, semantic-router accuracy, provider quality, or production workload performance.

## Evidence classification

A passing smoke test is **not production benchmark evidence**. The included router dataset is intentionally small and only guards regressions in deterministic behavior. Production promotion still requires a representative redacted mission corpus, temporal holdout, real provider/tool outcomes and measurement on the target M3 Max under normal workstation load.

## CI acceptance

The Pages workflow must fail if site generation or validation fails. Production uplift implementation should add additional CI for policy enforcement, sandbox escape, egress canaries, Pi bridge compatibility and M3 performance evidence; those are P0 gates in the artifact usability review.
