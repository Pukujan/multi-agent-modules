# TASK-MAM-0002 — Task Intake Contract

<!-- continuity:task {"acceptance":["The project authority records an accepted precedence order and versioned intake schema on issue #2 before resolver implementation begins.","The schema requires verified target, lane, authority, action, assigned task and role, dependencies, checkpoint state, explicit automation state, and authorization.","A deterministic resolver and property checks prove urgent-owner precedence, fail-closed routing, same-lane replacement, and cross-lane non-interference.","Continuity validation and required repository checks pass on the exact proposed revision.","The issue stays open until the project-wide three fresh-session, multi-device demonstration is observed and recorded; no unobserved cold start is claimed."],"depends_on":[],"goal":"Complete the task-classification and urgent-owner-priority contract required by GitHub issue #2, then implement and verify a small pure resolver without duplicating PCM or claiming the full cold-start runtime is delivered","id":"MAM-0002","issue_url":"https://github.com/Pukujan/multi-agent-modules/issues/2","next_action":"Open a reviewable PR for the resolver and property suite, verify GitHub CI on its exact revision, and keep issue #2 open until the three required cold starts are observed.","owner":"/root (Codex; project authority appointed by owner in current task)","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"A fresh session needs deterministic, durable task, role, authority, checkpoint, and automation state so urgent owner stops are honored and one runtime lane cannot terminate another"} -->

- Status: active
- Owner: `/root` (Codex; project authority appointed by the owner in this task)
- Priority: P1
- Depends on: none
- Leaf issue: [multi-agent-modules #2](https://github.com/Pukujan/multi-agent-modules/issues/2)
- Parent ancestry: none
- Primary writer: `/root`; branch `codex/mam-0002-task-intake-contract`

## Goal

Accept and implement the smallest testable task-intake and priority contract that satisfies issue #2. The contract must preserve PCM's workspace and continuity ownership and must never stop or replace a different provider lane.

## Human outcome

A genuinely new session can recover its repository, task, role, authority, checkpoint, and explicit goal/watchdog state from a versioned record. An authorized urgent owner stop outranks ordinary work while preserving a checkpoint, and a session cannot terminate work owned by another runtime lane.

## Scope and boundaries

- In scope: authoritative review and acceptance of the precedence order and JSON Schema; a deterministic, side-effect-free resolver; property tests; cold-start instructions for the schema and resolver.
- Out of scope: a launcher, agent-spawning transport, task DAG engine, A2A messaging, checkpoint service, merge adapter, or a second workspace manager.
- PCM remains the source for continuity and canonical-checkout behavior. Do not change its schemas or copy its implementation.
- The three fresh-session, multi-device runs are still required by the project goal and issue #2. They require a real runtime and observations on the owner's devices; this task must not report them as passed without evidence.

## Checkpoint log

- Refreshed GitHub issue #2 and draft PR #3. The proposed precedence table is directionally sound, but its schema did not require task, role, authorization, automation, or checkpoint state; there was no executable resolver or property suite.
- Recorded the authoritative task owner, branch, initial decision, and correction plan on issue #2 before creating this task projection.
- The precedence and original v1 schema were accepted in issue comment 5852705358. Before implementation began, a state-model gap was found: goals must be `paused` while jobs/watchdogs are `stopped`. The authority recorded the correction in issue comment 5852730090 and required schema version `mam.task-intake.v1.1`. The authority accepted corrected v1.1 at revision `868464144c4a552ecd8960c55f16992341ccdb28` in issue comment 5852760046. Resolver review then found the schema could list only one old session; issue comment 5852850796 amends that shape to v1.2 with a complete replacements array. The v1.2 shape is not yet accepted, and local resolver work is uncommitted.
- PCM `continuity preflight --root .` reported `TARGET_VALID`; `continuity validate --root .` reported `VALID`; issue verification confirmed MAM-0001 is open and MAM-0002/#2 is open. Draft 2020-12 schema meta-validation, one complete baseline record, and structural rejection cases for omitted automation, cross-lane stop authority, empty automation state, handoff without a published checkpoint, and an unknown version passed. No resolver or property tests have yet been implemented.

## Evidence and decisions

- Canonical leaf: https://github.com/Pukujan/multi-agent-modules/issues/2
- Existing draft proposal: https://github.com/Pukujan/multi-agent-modules/pull/3, source revision `45410fd6596849acd7326a23bf04eab3ba185b56`
- Initial authority and task checkpoint: https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-5852589102
- Initial design acceptance and subsequent pre-implementation state correction: https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-5852705358 and https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-5852730090
- Corrected schema v1.1 acceptance: https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-5852760046
- Branch: `codex/mam-0002-task-intake-contract`, based on the reviewed draft branch without modifying it.
- Branch protection was not configured for `main` at the time checked. Pull request checks still must be inspected on the final revision; absent checks cannot be described as passing.

## Progress after the first checkpoint

- Corrected the contract to use schema version `mam.task-intake.v1.1`; goals now distinguish `active` and `paused`, while scheduled jobs and watchdogs distinguish `active` and `stopped`.
- The earlier checkpoint records v1 and the pre-correction proposal. They remain immutable history; the v1.1 correction is tracked by issue comment 5852730090 and this new source revision.

## Pre-acceptance history (as recorded on issue #2)

- The owner amended the schema before any resolver code was committed so every prior same-lane session assigned to the repository must be listed and verified. Schema version is now v1.2 pending final acceptance.
- A local resolver prototype exists but is uncommitted and is being realigned to the complete replacement list. No implementation is delivered or authorized until v1.2 acceptance is recorded.
- The v1.2 schema meta-validates and accepts a complete intake with a replacement list; structural rejection cases for omitted state, invalid version/action, unauthorized cross-lane stop, empty automation, and missing handoff checkpoint pass. PCM preflight/validation and the pinned CGM contract validator also pass. The resolver prototype is stashed locally pending final v1.2 acceptance.

## Progress after v1.2 acceptance

- The authority accepted schema v1.2 at design revision `f971618e1907db25282ade86c995e26a8256ec80` in issue comment 5852903406, requiring a complete list of prior same-lane sessions. The accepted schema is at `schemas/mam/v1/task-intake.schema.json`.
- Implemented a side-effect-free resolver that checks intake claims against independently verified issue, permission, checkout, checkpoint, automation, and prior-session facts. Dispatch returns the complete intake and verified-facts snapshot; stop/handoff returns a checkpoint-first plan and never closes the task.
- Added 25 unit/property checks for urgent-owner precedence, self-promotion and impersonation, exact issue binding, scope/priority/dependency authorization, independently matched automation inventory, complete replacement lists, cross-lane isolation, deterministic routing, restored context, and schema enforcement. `python -m unittest discover -s tests` passes all 25 tests locally.
- Resolver review also confirmed that stop/handoff records may report prior-session inventory without asking to replace those sessions; only start/resume produces a replacement action.
- Added a CI workflow with the pinned runtime dependency. GitHub CI has not yet run on this branch. The project-level launcher and three fresh-session multi-device runs remain outstanding.

## Next action

Open a reviewable PR for the resolver and property suite, verify GitHub CI on its exact revision, and keep issue #2 open until the three required cold starts are observed.

### 2026-09-27 04:42:46 UTC — /root (Codex project authority)

<!-- continuity:checkpoint {"agent":"/root (Codex project authority)","blocked":["No resolver or property tests yet. Full runtime and three observed fresh-session runs remain outstanding."],"changed":["PROJECT.md, checkpoints/CURRENT.md, HANDOFF.md, proposals/0001-task-intake-and-urgent-owner-priority.md, proposals/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md"],"completed":["Corrected the intake schema and precedence proposal; validated the draft-2020-12 schema and structural rejection cases; updated PROJECT, CURRENT, HANDOFF, and the task projection."],"decisions":["The precedence is accepted in principle for correction. The v1 schema is not yet finally accepted; record that decision before implementing the resolver. The three-device cold-start acceptance remains outstanding."],"evidence":["Issue #2 is OPEN; reviewed draft PR #3 at source revision 45410fd6596849acd7326a23bf04eab3ba185b56. continuity preflight=TARGET_VALID; continuity validate=VALID; schema meta-validation, complete baseline record, and negative structural cases=PASS."],"next_action":"Publish this design-only checkpoint, then record final acceptance on issue #2 before implementing the resolver.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"MAM-0002","timestamp":"2026-09-27T04:42:46Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"df41ebcef55ff3375f9c3fe3e384b42f1ca2229422640b40125be3f17902669e","request_id":"23a1ab3c6ad44c8fa5b6da0188c574e6","schema":"project-continuity.checkpoint-operation.v1","task_id":"MAM-0002"} -->

Completed:
- Corrected the intake schema and precedence proposal; validated the draft-2020-12 schema and structural rejection cases; updated PROJECT, CURRENT, HANDOFF, and the task projection.

Evidence:
- Issue #2 is OPEN; reviewed draft PR #3 at source revision 45410fd6596849acd7326a23bf04eab3ba185b56. continuity preflight=TARGET_VALID; continuity validate=VALID; schema meta-validation, complete baseline record, and negative structural cases=PASS.

Decisions:
- The precedence is accepted in principle for correction. The v1 schema is not yet finally accepted; record that decision before implementing the resolver. The three-device cold-start acceptance remains outstanding.

Changed:
- PROJECT.md, checkpoints/CURRENT.md, HANDOFF.md, proposals/0001-task-intake-and-urgent-owner-priority.md, proposals/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md

Blocked/uncertain:
- No resolver or property tests yet. Full runtime and three observed fresh-session runs remain outstanding.

Next:
- Publish this design-only checkpoint, then record final acceptance on issue #2 before implementing the resolver.

### 2026-09-27 04:52:45 UTC — /root (Codex project authority)

<!-- continuity:checkpoint {"agent":"/root (Codex project authority)","blocked":["No resolver or property tests yet. Full runtime and three observed fresh-session runs remain outstanding."],"changed":["proposals/0001-task-intake-and-urgent-owner-priority.md, proposals/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md, checkpoints/CURRENT.md, HANDOFF.md"],"completed":["Corrected the accepted intake proposal before implementation: the v1.1 schema distinguishes paused goals from stopped scheduled jobs/watchdogs. Added a fail-closed rule for goal state and updated handoff/task projections."],"decisions":["The authority's accepted precedence and safety boundaries remain in force. Schema v1.1 replaces v1 by making goal pause auditable; final v1.1 approval is still required before resolver implementation."],"evidence":["Issue #2 correction comment 5852730090 amends earlier decision 5852705358; continuity preflight=TARGET_VALID; continuity validate=VALID; v1.1 JSON Schema meta-validation, baseline record, and structural rejection cases=PASS."],"next_action":"Push this schema correction, record its receipt, then make the final v1.1 authority decision before coding.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"MAM-0002","timestamp":"2026-09-27T04:52:45Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"cb30cf869e9ae178033de42c2b6274e3f8adc70b0e0d63e34ae08ace1967ccbf","request_id":"b6f351b6c042457ab5985ffbab24b144","schema":"project-continuity.checkpoint-operation.v1","task_id":"MAM-0002"} -->

Completed:
- Corrected the accepted intake proposal before implementation: the v1.1 schema distinguishes paused goals from stopped scheduled jobs/watchdogs. Added a fail-closed rule for goal state and updated handoff/task projections.

Evidence:
- Issue #2 correction comment 5852730090 amends earlier decision 5852705358; continuity preflight=TARGET_VALID; continuity validate=VALID; v1.1 JSON Schema meta-validation, baseline record, and structural rejection cases=PASS.

Decisions:
- The authority's accepted precedence and safety boundaries remain in force. Schema v1.1 replaces v1 by making goal pause auditable; final v1.1 approval is still required before resolver implementation.

Changed:
- proposals/0001-task-intake-and-urgent-owner-priority.md, proposals/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md, checkpoints/CURRENT.md, HANDOFF.md

Blocked/uncertain:
- No resolver or property tests yet. Full runtime and three observed fresh-session runs remain outstanding.

Next:
- Push this schema correction, record its receipt, then make the final v1.1 authority decision before coding.

### 2026-09-27 05:14:48 UTC — /root (Codex project authority)

<!-- continuity:checkpoint {"agent":"/root (Codex project authority)","blocked":["Resolver prototype and property tests are not delivered. Full runtime and three observed fresh-session runs remain outstanding."],"changed":["README.md, HANDOFF.md, PROJECT.md, checkpoints/CURRENT.md, proposals/0001-task-intake-and-urgent-owner-priority.md, schemas/mam/v1/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md"],"completed":["Published the corrected task-intake v1.2 design candidate, moved the accepted MAM schema into its namespace, updated the README/current/handoff records, and validated schema shape."],"decisions":["Final acceptance of schema v1.2 is pending. Local resolver prototype is held uncommitted until that decision. Earlier precedence, authorization, and goal-pause/job-stop decisions remain in force."],"evidence":["Issue #2 correction comment 5852850796 requires every prior same-lane session to be represented. v1.2 schema meta-validation, complete baseline, replacement-array example, and negative cases=PASS; continuity preflight=TARGET_VALID; continuity validate=VALID; CGM contract validator=VALID."],"next_action":"Record final acceptance of schema v1.2 on issue #2, then restore and align the resolver prototype.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"MAM-0002","timestamp":"2026-09-27T05:14:48Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"6f98ce02d2bc73d71e8b9e5c329ca5978407cfc30cf0ab1a80ed727155a7a35b","request_id":"ea9ea120127f474ca3e4c6efbf7f183a","schema":"project-continuity.checkpoint-operation.v1","task_id":"MAM-0002"} -->

Completed:
- Published the corrected task-intake v1.2 design candidate, moved the accepted MAM schema into its namespace, updated the README/current/handoff records, and validated schema shape.

Evidence:
- Issue #2 correction comment 5852850796 requires every prior same-lane session to be represented. v1.2 schema meta-validation, complete baseline, replacement-array example, and negative cases=PASS; continuity preflight=TARGET_VALID; continuity validate=VALID; CGM contract validator=VALID.

Decisions:
- Final acceptance of schema v1.2 is pending. Local resolver prototype is held uncommitted until that decision. Earlier precedence, authorization, and goal-pause/job-stop decisions remain in force.

Changed:
- README.md, HANDOFF.md, PROJECT.md, checkpoints/CURRENT.md, proposals/0001-task-intake-and-urgent-owner-priority.md, schemas/mam/v1/task-intake.schema.json, tasks/TASK-MAM-0002-task-intake-contract.md

Blocked/uncertain:
- Resolver prototype and property tests are not delivered. Full runtime and three observed fresh-session runs remain outstanding.

Next:
- Record final acceptance of schema v1.2 on issue #2, then restore and align the resolver prototype.
