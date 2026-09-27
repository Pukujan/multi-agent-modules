# Project charter

<!-- continuity:project {"id":"multi-agent-modules","protocol_version":"0.1.0-draft","schema":"project-continuity.project.v1","title":"multi-agent-modules"} -->

## Main goal

Provide one slim cold-start script and prompt for a multi-device, multi-agent runtime. The owner supplies one goal to one coordinator. The runtime starts genuinely new connected sessions on multiple devices, gives each agent its current setup and the right task, role, responsibility, ownership, authorization, dependency context, and recovery instructions, and keeps GitHub as the authoritative project record.

**Project identity is the canonical GitHub repository the agent is working for, not the folder where its runtime was initialized.** The owner wants one canonical local checkout per target repository on each computer: `D:\claude\<project>` on Windows and `~/Documents/projects/<project>` on the MacBook. PCM already provides the canonical-checkout policy, a private per-device workspace registry, and `workspace.mode: single-checkout`, which refuses managed linked worktrees. MAM should configure and use those PCM capabilities rather than rebuild them.

PCM does not scan drives or automatically discover unregistered clones. The cold-start bootstrap's remaining responsibility is narrow: inspect the designated path and already-known workspace locations, verify the GitHub remote, reuse the existing checkout, and initialize the session there. If a matching checkout is found elsewhere, do not clone another copy; inspect its state and resolve which checkout is canonical without discarding local work. If multiple matching copies or uncommitted states make that unclear, preserve them and record the collision for authoritative resolution.

Session replacement is scoped to the same runtime lane and target repository. A new Codex session takes over from an older Codex session assigned to the same repository after the old session checkpoints and stops. The same applies within each other runtime lane. A Claude Code, Grokbot, or other cross-vendor session must not stop or replace a Codex session. Different providers may remain active on the same repository and coordinate through GitHub ownership, task scopes, proposals, branches, and PRs.

The intended runtime combines strict agent-role policies, ownership and adjudication, DAG task classification and dependencies, lightweight agent-to-agent communication, durable failure recovery, and checkpoint/push/merge automation governed by PCM. Human-facing project records and outputs adapt CGM. PCM and CGM are referenced as Git submodules; their code is not copied here.

## Why

The current runtime coordinates agents and work across computers, but its setup depends on existing sessions and scattered project instructions. A simple, repeatable cold start should let an owner provide a goal once and let fresh agents resume the right work without relying on the original conversation. Runtime/provider boundaries must not split one GitHub repository into separate project identities or allow old and replacement sessions to write concurrently.

## Scope

Design and build a lean framework that:

- Starts from one owner-provided goal and a single launcher invocation.
- Uses PCM's per-device workspace registry and strict single-checkout policy rather than implementing another workspace manager. The bootstrap resolves the target canonical GitHub repository independently of the runtime's launch folder, checks the owner's per-device canonical path, verifies the GitHub remote, reuses the checkout, and initializes the fresh session there. Since PCM deliberately does not scan drives or discover unregistered clones, the bootstrap only needs the small path-resolution step and must not clone when an existing project folder is found.
- Finds older sessions in the same runtime lane assigned to that repository, requires their recoverable checkpoints and stop acknowledgments, and then starts same-lane replacements with the current configuration. It does not stop or replace sessions from other runtime/provider lanes.
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

Acceptance requires at least three successful cold starts using new sessions rather than reusing the original running conversations. The cold starts must cover multiple devices and demonstrate recovery after an interrupted process. At least one run must hand off from an old session to a fresh session in the same runtime lane and target repository; another must demonstrate that a different runtime lane working on that repository is not stopped or replaced. Same-lane replacement requires the old session's recoverable checkpoint and stop before the replacement starts. Agents must identify the project by verified canonical GitHub remote and use the per-device canonical checkout (`D:\claude\<project>` on Windows; `~/Documents/projects/<project>` on Mac), searching the known path/registry before any clone. The fresh session must be initialized from that one checkout as its workspace/current directory and load its repo instructions and continuity state. PCM's strict single-checkout mode must be enabled; no duplicate clone/worktree is created for a cold start. Each fresh session must recover the canonical GitHub goal, its assigned role/task/scope/authorization, dependencies, current checkpoint, and next action without relying on lost chat state. Record the exact script inputs, device/session aliases, issue refs, pushed checkpoint SHAs, recovery event, and observed outcomes. No secrets or model identity mapping are exposed in those records.

## Authority

The owner will use a separate local GPT session as the authoritative owner for this runtime project. This Codex/Claude session initialized the repository and collected setup reports; it is not the design arbiter. GitHub remains canonical for project scope, proposal decisions, ownership, checkpoints, pull requests, and merges. Workers must follow the authoritative decision and fail closed on unresolved conflicts.

## Current phase

**Initialization and setup inventory only.** Issue [#1](https://github.com/Pukujan/multi-agent-modules/issues/1) asks every current agent to record its real setup, responsibility, observed model/tool telemetry, durable state, cold-start/recovery procedure, and how it stops its own active goal and repo-specific watchdog. First-class issue [#2](https://github.com/Pukujan/multi-agent-modules/issues/2) records the missing strict task-classification and urgent-owner-priority policy. Runtime implementation remains not started until the future authoritative owner reviews the inventory and records an accepted plan.

