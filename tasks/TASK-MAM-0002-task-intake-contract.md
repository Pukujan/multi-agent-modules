# TASK-MAM-0002 — Task Intake Contract

<!-- continuity:task {"acceptance":["The project authority records an accepted precedence order and versioned intake schema on issue #2 before resolver implementation begins.","The schema requires verified target, lane, authority, action, assigned task and role, dependencies, checkpoint state, explicit automation state, and authorization.","A deterministic resolver and property checks prove urgent-owner precedence, fail-closed routing, same-lane replacement, and cross-lane non-interference.","Continuity validation and required repository checks pass on the exact proposed revision.","The issue stays open until the project-wide three fresh-session, multi-device demonstration is observed and recorded; no unobserved cold start is claimed."],"depends_on":[],"goal":"Complete the task-classification and urgent-owner-priority contract required by GitHub issue #2, then implement and verify a small pure resolver without duplicating PCM or claiming the full cold-start runtime is delivered","id":"MAM-0002","issue_url":"https://github.com/Pukujan/multi-agent-modules/issues/2","next_action":"Finish and validate the corrected human contract and JSON Schema, record the final authority decision on issue #2, then implement the resolver and property tests.","owner":"/root (Codex; project authority appointed by owner in current task)","priority":"P1","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"active","why":"A fresh session needs deterministic, durable task, role, authority, checkpoint, and automation state so urgent owner stops are honored and one runtime lane cannot terminate another"} -->

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
- The precedence policy is accepted in principle for correction; the schema remains unaccepted until it carries all required cold-start state.
- PCM `continuity preflight --root .` reported `TARGET_VALID`; `continuity validate --root .` reported `VALID`; issue verification confirmed MAM-0001 is open and MAM-0002/#2 is open. Draft 2020-12 schema meta-validation, one complete baseline record, and structural rejection cases for omitted automation, cross-lane stop authority, empty automation state, handoff without a published checkpoint, and an unknown version passed. No resolver or property tests have yet been implemented.

## Evidence and decisions

- Canonical leaf: https://github.com/Pukujan/multi-agent-modules/issues/2
- Existing draft proposal: https://github.com/Pukujan/multi-agent-modules/pull/3, source revision `45410fd6596849acd7326a23bf04eab3ba185b56`
- Initial authority and task checkpoint: https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-5852589102
- Branch: `codex/mam-0002-task-intake-contract`, based on the reviewed draft branch without modifying it.
- Branch protection was not configured for `main` at the time checked. Pull request checks still must be inspected on the final revision; absent checks cannot be described as passing.

## Next action

Complete the corrected schema and human contract, validate them, record final acceptance on issue #2, then implement and test the resolver.

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
