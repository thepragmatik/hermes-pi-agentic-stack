# Research Sources — snapshot 2026-08-31

Primary/authoritative sources are preferred. Volatile model/provider/plugin details must be re-verified before implementation; model IDs, prices and unreleased roadmap items are evidence snapshots, not architecture constants.

## Hermes — fresh install, profiles, config and provider routing
- https://hermes-agent.nousresearch.com/docs/
- https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- https://hermes-agent.nousresearch.com/docs/user-guide/features/profiles
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing
- https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search
- https://github.com/NousResearch/hermes-agent

Current design uses documented profile/Blank-Slate/model/config/query-file mechanisms. A Hermes profile isolates config/state but is not treated as a filesystem sandbox.

## OpenRouter — gateway, provider routing, privacy, session affinity and model routing
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/features/privacy-and-logging
- https://openrouter.ai/docs/features/presets
- https://openrouter.ai/docs/features/routers
- https://openrouter.ai/docs/features/model-routing
- https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
- https://openrouter.ai/z-ai/glm-5.3-flash
- https://openrouter.ai/deepseek/deepseek-v4-flash-0731

OpenRouter is the default external gateway. Local deterministic eligibility/privacy/security and local mission/workflow/model decisions remain upstream. Provider allow/deny, parameter filtering, data/ZDR policy, price/latency/throughput preferences, fallback and session affinity are downstream capabilities to reuse where the installed Hermes/OpenRouter integration demonstrably forwards/enforces them. Direct providers remain benchmarked adapters.

## Routing frameworks / local models
- https://github.com/aurelio-labs/semantic-router
- https://github.com/aurelio-labs/semantic-router/releases
- https://github.com/vllm-project/semantic-router
- https://github.com/vllm-project/semantic-router/tree/main/website/docs
- https://github.com/vllm-project/semantic-router/tree/main/config/recipes/agent
- https://github.com/ulab-uiuc/LLMRouter
- https://github.com/lm-sys/RouteLLM
- https://huggingface.co/answerdotai/ModernBERT-base
- https://huggingface.co/nomic-ai/modernbert-embed-base
- https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- https://github.com/ml-explore/mlx-lm

Interpretation used by the playbook:
- Aurelio Semantic Router: lightweight local semantic-classification challenger/component.
- vLLM Semantic Router: strongest medium-term adoption candidate for richer signal/session/model routing; stable released capabilities must be separated from roadmap/backlog.
- LLMRouter: research/training/evaluation plane for comparing many algorithms, not default hot path.
- RouteLLM: strong-vs-economical/difficulty preference scorer, primarily Tier 3 rather than mission ontology.
- ModernBERT: future multi-label/multi-head learned mission-profile component only after representative redacted outcome data justifies training.
- OpenRouter Auto: shadow/teacher/bootstrap/fallback signal only after Tier-0 eligibility; never privacy/security authority.

## Hermes sessions / skills / context
- https://hermes-agent.nousresearch.com/docs/user-guide/sessions
- https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage
- https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
- https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
- https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin
- https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin/
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers/
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://hermes-agent.nousresearch.com/docs/reference/tools-reference/
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

## Local context / memory
- https://github.com/stephenschoettler/hermes-lcm
- https://github.com/stephenschoettler/hermes-lcm/releases
- https://github.com/stephenschoettler/hermes-lcm/blob/main/docs/operator-guide.md
- https://github.com/mnemosyne-oss/mnemosyne
- https://github.com/mnemosyne-oss/mnemosyne/releases
- https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/hermes-integration.md
- https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/api/configuration.mdx
- https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/hygiene.md

## Pi / sandboxing / LSP
- https://github.com/earendil-works/pi
- https://pi.dev
- https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md
- https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/containerization.md
- https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/environment-variables.md
- https://github.com/samfoy/pi-lsp-extension
- https://kotlinlang.org/docs/kotlin-lsp.html
- https://github.com/typescript-language-server/typescript-language-server
- https://github.com/microsoft/pyright
- https://github.com/eclipse-jdtls/eclipse.jdt.ls
- https://github.com/hrsh7th/vscode-langservers-extracted

## Spec-driven development
- https://github.com/github/spec-kit
- https://github.github.io/spec-kit/

## Security / privacy
- https://github.com/data-privacy-stack/presidio
- https://github.com/gitleaks/gitleaks
- https://github.com/trufflesecurity/trufflehog

## Publishing / agent discovery
- https://docs.github.com/en/pages
- https://llmstxt.org/

## Evaluation data
- https://github.com/SWE-bench/SWE-bench
- https://github.com/github/CodeSearchNet
- https://huggingface.co/datasets/allenai/WildChat-1M
- https://huggingface.co/datasets/lmsys/lmsys-chat-1m

Public datasets seed coverage only. The highest-value routing evidence is locally redacted/deduplicated Hermes/Pi mission telemetry joined to actual workflow/model/provider outcomes, with mission/repository/session/time holdouts and privacy-controlled retention.