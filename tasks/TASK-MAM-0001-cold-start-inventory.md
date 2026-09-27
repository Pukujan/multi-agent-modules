# TASK-MAM-0001 — Cold Start Inventory

<!-- continuity:task {"acceptance":["Each participating local subagent has a self-reported setup and cold-start record on GitHub issue #1, or its absence is explicitly noted.","All agents with active Jev classifier assignments are asked on the Jev coordination issue to checkpoint safely, then report their actual setup and recovery path on multi-agent-modules issue #1.","Reports distinguish observed, agent-declared, unavailable, and context-only facts; no credentials or identity mapping are published.","This task ends after inventory and handoff; no runtime implementation starts before review by the owner-appointed local GPT session.","Canonical GitHub repository defines project identity across runtimes; every old session assigned to the same repository checkpoints and stops before fresh replacements start."],"depends_on":[],"goal":"Collect current agent setup and cross-runtime handoff procedures, using canonical GitHub repository identity for each project","id":"MAM-0001","issue_url":"https://github.com/Pukujan/multi-agent-modules/issues/1","next_action":"Await setup reports from agents currently working on Jev; after they safely checkpoint and report, hand the inventory to the owner-appointed local GPT session for review.","owner":"initialization-coordinator (/root)","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"The owner wants a slim runtime that starts fresh connected agents across devices and resumes their work from GitHub after failure"} -->

- Status: active
- Owner: initialization-coordinator (/root) — initialization and inventory only, not design authority.
- Priority: P1
- Depends on: none

## Goal

Collect how every current agent is actually started, what responsibility and authorization it has, what state survives process death, and how a new session can cold-start or recover on another device.

For this handoff, the canonical GitHub repository defines the project across all runtimes. Codex/OpenAI, Claude Code, Grokbot, Grok agents, and other sessions assigned to the same repository are part of the same project. Every old session assigned to that repository must checkpoint and stop before any fresh replacement starts.

## Human outcome

The owner-appointed local GPT session will receive evidence about the actual runtime in use, so it can plan a small, testable cold-start system rather than inventing agent configuration or responsibilities.

## Scope and boundaries

- In scope: collect self-reported setup, task ownership, role/authorization, observable model/tool/device telemetry, durable state, and exact cold-start/recovery steps; link each report to canonical GitHub issues.
- In scope: record project identity by canonical GitHub repository and the cross-runtime checkpoint/stop barrier before fresh-session takeover.
- Out of scope: implementation of scripts or runtime services; changing primary Jev project code; assigning hidden model identities; publishing secrets; claiming authority for the future local GPT owner.
- Dependency: GitHub issue #1 is the canonical inventory request; agents working on Jev should checkpoint safely and report before switching.

## Acceptance criteria

- [ ] Each participating local subagent's self-report is present in issue #1.
- [ ] Every currently active Jev project agent has been asked on the Jev coordination issue and either reports here or is marked as not yet responded.
- [ ] Each record distinguishes observed, declared, unavailable, durable, and context-only information.
- [ ] The owner-appointed local GPT receives the issue link and a clear statement that implementation has not started.
- [ ] The project-identity rule is recorded: sessions in different runtimes working in the same canonical GitHub repository are one project handoff; old sessions checkpoint and stop before fresh replacements start.

## Evidence and sources

- Canonical request and agent reports: https://github.com/Pukujan/multi-agent-modules/issues/1
- Owner direction to current Jev agents: https://github.com/Pukujan/jev-classifier/issues/22
- Repository setup commit: 0dd511c
- PCM target preflight: `continuity preflight --root .` → `MODE: TARGET_VALID`.
- PCM record validation: `continuity validate --root .` → `VALID`.

## Related records

- Leaf issue: https://github.com/Pukujan/multi-agent-modules/issues/1
- Parent ancestry: none
- Primary writer: initialization-coordinator (/root); branch: main
- Authority for runtime design: owner-appointed local GPT session, not this task worker.

## Checkpoint log

- Initialized the repository and added PCM/CGM Git submodules; recorded the charter; requested agent setup reports. No runtime code or JEV benchmark was started.
- Followed PCM's non-destructive target-adoption process after `continuity init` correctly refused to overwrite the existing README/PROJECT. Materialized PCM schemas/config and metadata without replacing owner-authored content; preflight and validation passed.
- Owner added the requirement for at least three fresh sessions across multiple devices and recovery from interruption, using spec-driven, property-driven, and test-driven methods while keeping the runtime lean.
- Owner clarified that the canonical GitHub repository defines project identity across runtimes; all old sessions assigned to that repository must checkpoint and stop before fresh sessions take over.
- Waiting for active Jev agents' safe checkpoint and setup reports.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant specification. Refresh issue #1 before acting. The next writer is the owner-appointed local GPT session after this setup inventory is complete.
