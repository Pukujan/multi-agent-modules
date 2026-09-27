# multi-agent-modules

A reusable, cold-startable runtime for coordinating agents across devices and repositories, with GitHub as the authoritative project state.

## Project goal

Let an owner give one goal to one coordinator. The runtime should turn that goal into scoped tasks, assign agents with explicit roles and authorization, coordinate dependencies as a DAG, pass bounded messages agent-to-agent, and preserve enough checkpoints that a fresh process or another device can resume reliably.

GitHub issues, proposals, and pull requests remain canonical. Local state is a rebuildable helper. PCM and CGM are referenced as Git submodules; their code is not copied into this repository.

## Current phase

**Initialization and setup inventory only.** The first issue asks current agents to document their actual setup, active responsibilities, durable state, and cold-start/recovery instructions. No runtime implementation is started in this phase.

See [PROJECT.md](PROJECT.md) and the [GitHub project issue tracker](https://github.com/Pukujan/multi-agent-modules/issues).

## Helper modules

- [Project Continuity Modules](adapters/project-continuity-modules) — continuity, evidence, and checkpointing helper.
- [Content Generation Modules](adapters/content-generation-modules) — human-facing writing and documentation guidance.

Both are Git submodules pinned to specific upstream commits. Update them through submodule pointer changes; do not vendor-copy their code.

