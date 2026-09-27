# multi-agent-modules

When a project runs across several computers, a single agent session can hold important context that another session cannot see after a crash. The first setup reports in [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1) already show which findings existed only in temporary agent context before they were recorded.

## Why this exists

Picture an owner starting research on one device and handing implementation to an agent on another. If the first process disappears, the second agent needs to know which issue is authoritative, what it owns, what it is allowed to change, which work depends on other tasks, and exactly where the previous agent stopped.

This project is meant to make that handoff a repeatable one-command start, backed by durable GitHub state.

## What counts as the same project

The canonical GitHub repository defines project identity. Codex, OpenAI, Claude Code, Grokbot, Grok agents, or another runtime working in that repository are all working on the same project. When a cold start replaces those sessions, every older session assigned to that repository must checkpoint and stop before any replacement session starts. Different GitHub repositories are different projects, even when the agents or runtime are the same.

## What this project is

A **planned, not yet implemented** cold-start runtime. The owner will give one goal to a coordinator; a starter script should create fresh connected sessions across devices and give each agent its own responsibility, authorization, dependency state, checkpoint, and next action.

The owner plans to appoint a separate local GPT session as the authoritative owner for the runtime design. This repository's setup session is not that arbiter.

## How it should work

1. The owner gives the coordinator one goal and target GitHub repository.
2. The starter reads the canonical GitHub issue, current ownership decisions, and the sessions assigned to that repository across runtimes.
3. Those older sessions publish recoverable checkpoints and stop; replacements do not start until the handoff is complete.
4. Fresh agents connect on the available devices and receive bounded tasks, roles, and permissions.
5. Agents coordinate through a small task DAG and durable A2A messages.
6. Checkpoints go back to GitHub through PCM-governed steps, so a fresh session can resume after interruption.

These are design requirements, not shipped behavior.

## Evidence and boundaries

The repository currently contains the charter, setup inventory, PCM continuity metadata, and PCM/CGM as pinned Git submodules. Current agents are posting how they were actually started and how a new process can resume in [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1).

**No starter script, agent launcher, DAG engine, A2A transport, checkpoint automation, or merge adapter exists yet.** The acceptance target is three successful starts of fresh sessions across multiple devices, including recovery after interruption and a cross-runtime handoff in the same repository. See [PROJECT.md](PROJECT.md) for the exact owner requirements and [HANDOFF.md](HANDOFF.md) for the current resume path.

## Current next step

Read the setup reports on [issue #1](https://github.com/Pukujan/multi-agent-modules/issues/1). The next design session should be the owner-appointed local GPT session; it should review the actual agent configurations and propose the smallest plan that can pass the three-cold-start acceptance test.

## Helper repositories

- [Project Continuity Modules](adapters/project-continuity-modules) is the continuity, issue, and checkpoint helper.
- [Content Generation Modules](adapters/content-generation-modules) provides guidance for human-facing documentation and outputs.

Both are pinned as Git submodules. Their source code is not copied into this repository.

