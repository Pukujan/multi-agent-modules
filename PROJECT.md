# Project charter

## Main goal

Provide a reusable cold-start script and prompt for a multi-device, multi-agent runtime. The owner gives one goal to one coordinator; the runtime creates the project workspace and its authoritative GitHub issue plan, assigns agents scoped goals, and gives each agent the current task, ownership, authority, dependencies, and resume instructions.

The runtime must support:

- Multiple computers and agents working on one project.
- Explicit agent roles, task classification, ownership claims, and authorization boundaries.
- An authoritative adjudication/proposal layer that resolves collisions and contradictions.
- DAG-based task dependencies, sequencing, retries, and recoverable long-running work.
- Lightweight agent-to-agent messages with sender, recipient, scope, timestamp, idempotency, and durable references.
- GitHub issues and pull requests as canonical project state; local databases and continuity records are rebuildable helpers.
- Automated, idempotent checkpoint pushes and proposal-governed auto-merges through a PCM adapter.
- Human-facing README, issue, PR, project, and output writing that adapts CGM rather than copying its code.
- Opaque stable agent/model aliases and available run telemetry, without publishing identity mappings or secrets.
- Cold starts and recovery from both clean and interrupted processes on another device.

These are owner requirements to design and validate, not claims that the runtime already implements them.

## Current scope

This repository has been initialized only. Its first active work is to collect each current agent's actual setup and operating instructions. Runtime architecture and implementation are intentionally not started until that inventory is recorded and the owner or authoritative project process accepts a concrete plan.

## Source and authority rules

1. GitHub is canonical for goals, issues, proposals, decisions, ownership, checkpoints, PRs, and merges.
2. The designated authoritative agent decides proposal conflicts; a worker must not infer approval from an issue being open.
3. Local SQLite, PCM records, and cached boards are continuity aids, never an alternate authority.
4. Agents report only host, model, temperature, tools, and identity details that are actually observable or explicitly declared. Unknown values remain unavailable.
5. Never place API keys, environment files, identity maps, or private authentication material in GitHub.
6. PCM and CGM are upstream helper projects referenced as Git submodules. This repository does not copy their code.

## Initialization boundary

Completed: create the GitHub repository, add the two helper submodules, record this charter, and request an inventory of current agent setups and cold-start procedures.

Not started: bootstrap script, agent spawning/routing, cross-device transport, DAG engine, A2A protocol implementation, run telemetry implementation, auto-push/merge automation, runtime deployment, and benchmarks.

