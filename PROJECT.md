# Project charter

<!-- continuity:project {"id":"multi-agent-modules","protocol_version":"0.1.0-draft","schema":"project-continuity.project.v1","title":"multi-agent-modules"} -->

## Main goal

Provide one slim cold-start script and prompt for a multi-device, multi-agent runtime. The owner supplies one goal to one coordinator. The runtime starts genuinely new connected sessions on multiple devices, gives each agent its current setup and the right task, role, responsibility, ownership, authorization, dependency context, and recovery instructions, and keeps GitHub as the authoritative project record.

**Project identity is the canonical GitHub repository.** Codex, OpenAI, Claude Code, Grokbot, Grok agents, and other runtime/provider sessions assigned to the same repository are working on the same project, even when their sessions and vendors differ. A cold start for that repository must first checkpoint and stop all older sessions assigned to it across runtimes; only after that handoff may replacement sessions start. Different canonical GitHub repositories are different projects.

The intended runtime combines strict agent-role policies, ownership and adjudication, DAG task classification and dependencies, lightweight agent-to-agent communication, durable failure recovery, and checkpoint/push/merge automation governed by PCM. Human-facing project records and outputs adapt CGM. PCM and CGM are referenced as Git submodules; their code is not copied here.

## Why

The current runtime coordinates agents and work across computers, but its setup depends on existing sessions and scattered project instructions. A simple, repeatable cold start should let an owner provide a goal once and let fresh agents resume the right work without relying on the original conversation. Runtime/provider boundaries must not split one GitHub repository into separate project identities or allow old and replacement sessions to write concurrently.

## Scope

Design and build a lean framework that:

- Starts from one owner-provided goal and a single launcher invocation.
- Identifies the target by its canonical GitHub repository and creates fresh agent sessions using each agent's actual current configuration, regardless of runtime/provider.
- Finds older sessions assigned to that repository across runtimes, requires their recoverable checkpoints and stop acknowledgments, and starts replacement sessions only after the handoff barrier is clear.
- Assigns bounded responsibilities, permissions, ownership, and DAG dependencies.
- Uses GitHub issues and pull requests as canonical state, with local state only as a rebuildable aid.
- Supports lightweight, durable, idempotent A2A messages and checkpoints across devices.
- Recovers correctly when an agent process or device fails.
- Uses PCM for continuity/checkpoint coordination and CGM guidance for human-facing documents and outputs.
- Applies spec-driven, property-driven, and test-driven development while keeping the shipped runtime small.

## Non-goals for this initialization

The launcher, agent spawning/routing, DAG engine, A2A transport, telemetry collector, automated checkpoint pusher, PCM merge adapter, deployment, and benchmarks are not implemented yet. Do not copy PCM or CGM source code into this repository.

## Definition of success

The runtime project passes when a fresh coordinator can repeatedly run the same starter script with one goal and create connected sessions that resume across the project's devices with correct responsibilities and authorization, even after a process failure.

Acceptance requires at least three successful cold starts using new sessions rather than reusing the original running conversations. The cold starts must cover multiple devices and demonstrate recovery after an interrupted process. At least one run must hand off between different runtime/provider types assigned to the same canonical GitHub repository. Every prior session assigned to that repository must checkpoint and stop before replacements start; project identity must not depend on vendor, agent label, or session ID. Each fresh session must recover the canonical GitHub goal, its assigned role/task/scope/authorization, dependencies, current checkpoint, and next action without relying on lost chat state. Record the exact script inputs, device/session aliases, issue refs, pushed checkpoint SHAs, recovery event, and observed outcomes. No secrets or model identity mapping are exposed in those records.

## Authority

The owner will use a separate local GPT session as the authoritative owner for this runtime project. This Codex/Claude session initialized the repository and collected setup reports; it is not the design arbiter. GitHub remains canonical for project scope, proposal decisions, ownership, checkpoints, pull requests, and merges. Workers must follow the authoritative decision and fail closed on unresolved conflicts.

## Current phase

**Initialization and setup inventory only.** Issue [#1](https://github.com/Pukujan/multi-agent-modules/issues/1) asks every current agent to record its real setup, responsibility, observed model/tool telemetry, durable state, and cold-start/recovery procedure. Runtime implementation remains not started until the future authoritative owner reviews that inventory and accepts a slim plan.

