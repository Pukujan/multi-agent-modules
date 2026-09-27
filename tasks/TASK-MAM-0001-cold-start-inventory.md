# TASK-MAM-0001 — Cold Start Inventory

<!-- continuity:task {"acceptance":["Each participating local subagent has a self-reported setup and cold-start record on GitHub issue #1, or its absence is explicitly noted.","All agents with active Jev classifier assignments are asked on the Jev coordination issue to checkpoint safely, then report their actual setup and recovery path on multi-agent-modules issue #1.","Reports distinguish observed, agent-declared, unavailable, and context-only facts; no credentials or identity mapping are published.","This task ends after inventory and handoff; no runtime implementation starts before review by the owner-appointed local GPT session.","Canonical GitHub repository plus the same runtime lane defines session replacement; a different runtime lane is not stopped or replaced.","Each Jev agent reports its own active goal and repo-specific watchdog/scheduled-job state, stop action, verification, and restart procedure in both repository issue logs."],"depends_on":[],"goal":"Collect current agent setup, repo authority, canonical checkout, same-runtime takeover, and verified goal/watchdog self-stop procedures","id":"MAM-0001","issue_url":"https://github.com/Pukujan/multi-agent-modules/issues/1","next_action":"Collect same-runtime setup and verified goal/watchdog stop reports from Jev agents on both repositories, then hand the inventory to the owner-appointed local GPT session.","owner":"initialization-coordinator (/root)","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"The owner wants a slim runtime that starts fresh connected agents across devices and resumes their work from GitHub after failure"} -->

- Status: active
- Owner: initialization-coordinator (/root) — initialization and inventory only, not design authority.
- Priority: P1
- Depends on: none

## Goal

Collect how every current agent is actually started, what responsibility and authorization it has, what state survives process death, and how a new session can cold-start or recover on another device.

The canonical GitHub repository the agent is working for defines the project, not the folder where its runtime started. Keep one canonical checkout per device (`D:\claude\<project>` on Windows; `~/Documents/projects/<project>` on Mac). PCM already has the canonical-checkout policy, private per-device workspace registry, and strict `single-checkout` mode. The bootstrap should reuse those capabilities and only resolve the target path, since PCM intentionally does not scan drives for unregistered clones. Initialize the fresh session from the existing canonical checkout. Replacement applies only to an older session in the same runtime lane and repository; other runtime/provider lanes must not stop or replace one another.

## Human outcome

The owner-appointed local GPT session will receive evidence about the actual runtime in use, so it can plan a small, testable cold-start system rather than inventing agent configuration or responsibilities.

## Scope and boundaries

- In scope: collect self-reported setup, task ownership, role/authorization, observable model/tool/device telemetry, durable state, and exact cold-start/recovery steps; link each report to canonical GitHub issues.
- In scope: record PCM's existing workspace/reuse capabilities and limits; specify only the thin bootstrap path resolution needed to locate the per-device canonical checkout and start the session there; record same-lane replacement, cross-vendor non-interference, and each agent's self-stop/resume procedure for its own goal and repo-specific watchdog.
- Out of scope: implementation of scripts or runtime services; changing primary Jev project code; assigning hidden model identities; publishing secrets; claiming authority for the future local GPT owner.
- Dependency: GitHub issue #1 is the canonical inventory request; agents working on Jev should checkpoint safely and report before switching.

## Acceptance criteria

- [ ] Each participating local subagent's self-report is present in issue #1.
- [ ] Every currently active Jev project agent has been asked on the Jev coordination issue and either reports here or is marked as not yet responded.
- [ ] Each record distinguishes observed, declared, unavailable, durable, and context-only information.
- [ ] The owner-appointed local GPT receives the issue link and a clear statement that implementation has not started.
- [ ] The target is located by verified canonical GitHub remote, not runtime initialization folder; likely Windows and Mac project roots are checked.
- [ ] PCM's existing canonical-checkout, workspace-registry, and `single-checkout` behaviors are used; no parallel MAM workspace manager is invented.
- [ ] Any remaining target-path discovery is limited to the designated path and known registry entries; the bootstrap does not assume PCM scans disks or create a duplicate clone/worktree.
- [ ] Fresh sessions initialize from the verified target checkout and load its repo instructions and continuity state as their project context.
- [ ] Same-lane sessions for the same repository hand off through checkpoint and stop before replacement; other vendor/runtime lanes are not stopped or replaced.
- [ ] Each Jev agent reports its own `/goal` state and exact pause/stop method, plus any repo-specific watchdog/scheduled-job state, stop verification, and restart procedure in both JEV and MAM issue logs; unavailable controls are marked explicitly.

## Evidence and sources

- Canonical request and agent reports: https://github.com/Pukujan/multi-agent-modules/issues/1
- Task-classification and urgent-owner-priority requirement: https://github.com/Pukujan/multi-agent-modules/issues/2
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
- Owner clarified that GitHub repo identity determines the target independent of runtime launch folder; replacement is same runtime lane + same repo only, with cross-vendor sessions left running.
- Owner directed current Jev agents to checkpoint, mirror setup/ownership/authority reports to both repos, pause their own Jev goal and watchdog, verify and report stop status, and stop Jev work for today.
- First current Jev writer `jev-classifier@teresa` posted matching reports on MAM #1 and JEV #14. It reports the same-runtime lane as Grok Bot/Cursor; open Jev PRs #75 and #83; no uncommitted work intended; its two Jev routines are paused; this Grok runtime has no `/goal`; its Windows host has no macOS LaunchAgent. Other agent reports remain pending.
- PCM's pinned source confirms canonical checkout guidance, per-device registry, `single-checkout` refusal of managed worktrees, and no drive scan. Set MAM mode to `single-checkout`; registered this checkout locally. `continuity preflight` → `TARGET_VALID`; `continuity validate` → `VALID`.
- MAM issue #2 now tracks the missing strict task-classification and urgent-owner-priority policy; implementation awaits the owner-appointed GPT.
- Waiting for active Jev agents' safe checkpoint and setup reports.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant specification. Refresh issue #1 before acting. The next writer is the owner-appointed local GPT session after this setup inventory is complete.
