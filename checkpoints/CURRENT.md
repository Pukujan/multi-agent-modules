# Current checkpoint

<!-- continuity:current {"active_task":"MAM-0002","active_task_file":"tasks/TASK-MAM-0002-task-intake-contract.md","protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

This is an as-of projection; GitHub issues #1 and #2 own the setup inventory and authoritative task-intake contract, respectively.

## Program state

Phase: authoritative task-intake design and policy implementation. The full cold-start runtime has not started.

## Completed

- Created and pushed the initial repository charter and PCM/CGM submodule pointers.
- Initialized PCM metadata and schema files without replacing the existing charter.
- Asked current agents to post their actual setup and cold-start instructions on issue #1.
- Recorded the owner's three-fresh-session, multi-device, interruption-recovery acceptance requirement.
- Recorded the corrected identity and replacement rule: target is the verified canonical GitHub repo, independent of launch folder; only same-runtime sessions for that repo are replaced after checkpoint and stop.
- Confirmed PCM already provides canonical-checkout guidance, a private per-device workspace registry, and strict `single-checkout` mode. Only thin target-path resolution remains because PCM intentionally does not scan drives for unregistered clones.
- Created the first-class task-classification and urgent-owner-priority requirement as issue #2, linked to the JEV policy gap issue #94.
- Posted the owner stop-for-today and self-stop/watchdog-report directive to MAM issue #1 and current open JEV task/coordination issues.
- Received the first complete dual-repo handoff from Grok Bot lane `jev-classifier@teresa` on MAM #1 / JEV #14; that agent reported its two Jev routines paused, `/goal` unavailable, and the macOS LaunchAgent not installed on its Windows host.
- Registered this MAM checkout in PCM's private Windows workspace registry and enabled `single-checkout`; `continuity preflight` reports `TARGET_VALID` and `continuity validate` reports `VALID`.
- Filed MAM issue #2 and linked JEV issue #94 for the missing strict task-classification and urgent owner-priority policy.
- The project owner appointed the current local Codex task as project authority for continuation; the appointment and task ownership are recorded on issue #2.
- Refreshed draft PR #3 and found that it did not require task, role, authorization, automation, or checkpoint state in every intake. A corrected contract is being prepared on the separately owned branch `codex/mam-0002-task-intake-contract`; the Claude-authored branch is unchanged.
- Created task MAM-0002 for issue #2. The authority accepted the precedence and schema in comment 5852705358, then recorded a pre-implementation correction in comment 5852730090 so goal `paused` state is distinct from stopped jobs/watchdogs. The corrected v1.1 schema awaits a final decision; no resolver or property tests exist yet.

## Active

- MAM-0002: correct and accept the task-intake contract, then implement its deterministic resolver and property checks.
- MAM-0001 / issue #1 remains open for same-runtime setup, ownership, goal, and watchdog stop reports from the remaining Jev agents.

## Blockers

- The setup inventory on issue #1 remains incomplete; outstanding agent reports and verified self-stop statuses are pending.
- Reports and verified self-stop statuses from the other remote agents currently on Jev issues are pending.
- The starter script and orchestration runtime do not exist yet; the three fresh-session demonstrations cannot pass until they exist and are run on multiple devices.

## Next atomic action

Finish and validate MAM-0002's corrected contract, record final acceptance on issue #2, then implement and test its pure resolver. Keep the three-run project acceptance gate open until observed evidence exists.
