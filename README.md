# multi-agent-modules

When a project runs across several computers, a single agent session can hold important context that another session cannot see after a crash. The first setup reports in [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1) already show which findings existed only in temporary agent context before they were recorded.

## Why this exists

Picture an owner starting research on one device and handing implementation to an agent on another. If the first process disappears, the second agent needs to know which issue is authoritative, what it owns, what it is allowed to change, which work depends on other tasks, and exactly where the previous agent stopped.

This project is meant to make that handoff a repeatable one-command start, backed by durable GitHub state.

## What counts as the same project

The canonical GitHub repository the agent is working for defines project identity; the agent's launch folder does not. Keep one canonical checkout per device: `D:\claude\<project>` on Windows and `~/Documents/projects/<project>` on the MacBook. PCM already has a private per-device workspace registry and `single-checkout` mode to refuse managed linked worktrees. The bootstrap only needs to resolve the target repo to its existing canonical folder and start the new session there; it should not rebuild PCM's workspace policy or clone a second copy. PCM does not scan drives for unregistered copies, so check the designated path and known registry entries.

Replacement is within the same runtime lane and repository: a new Codex session takes over an older Codex session after it checkpoints and stops. A Claude Code or Grok session must not stop or replace Codex. Different runtime lanes can remain active on the same repo and coordinate through GitHub's task ownership and branch/PR workflow.

## What this project is

A **planned, not yet implemented** cold-start runtime. The owner will give one goal to a coordinator; a starter script should create fresh connected sessions across devices and give each agent its own responsibility, authorization, dependency state, checkpoint, and next action.

The owner plans to appoint a separate local GPT session as the authoritative owner for the runtime design. This repository's setup session is not that arbiter.

## How it should work

1. The owner gives the coordinator one goal and target GitHub repository.
2. The starter finds and verifies the one canonical target checkout on this device, then reads the canonical GitHub issue, current ownership decisions, and sessions in the same runtime lane assigned to that repository.
3. The old same-lane session publishes a recoverable checkpoint and stops; the fresh same-lane replacement starts after handoff. Other runtime lanes are left running.
4. The fresh session is initialized with the target checkout as its project/workspace and working directory, and loads that repo's own agent instructions and continuity state.
5. Fresh agents connect on the available devices and receive bounded tasks, roles, and permissions.
6. Agents coordinate through a small task DAG and durable A2A messages.
7. Checkpoints go back to GitHub through PCM-governed steps, so a fresh session can resume after interruption.

These are design requirements, not shipped behavior.

## Evidence and boundaries

The repository currently contains the charter, setup inventory, PCM continuity metadata, and PCM/CGM as pinned Git submodules. Current agents are posting how they were actually started and how a new process can resume in [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1).

**No starter script, agent launcher, DAG engine, A2A transport, checkpoint automation, or merge adapter exists yet.** The acceptance target is three successful fresh starts across multiple devices, including same-runtime takeover, recovery after interruption, and proof that another runtime lane is not stopped. See [PROJECT.md](PROJECT.md) for the exact owner requirements and [HANDOFF.md](HANDOFF.md) for the current resume path.

## Current next step

Read the setup reports on [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1) and the task-classification/priority requirement in [issue #2](https://github.com/Pukujan/multi-agent-modules/issues/2). The next design session should be the owner-appointed local GPT session; it should review the actual agent configurations and propose the smallest plan that can pass the three-cold-start acceptance test.

## Helper repositories

- [Project Continuity Modules](adapters/project-continuity-modules) is the continuity, issue, and checkpoint helper.
- [Content Generation Modules](adapters/content-generation-modules) provides guidance for human-facing documentation and outputs.

Both are pinned as Git submodules. Their source code is not copied into this repository.

