# Handoff

## Start here

1. Confirm this is the repository https://github.com/Pukujan/multi-agent-modules and refresh its current GitHub state.
2. Read PROJECT.md, checkpoints/CURRENT.md, and the active task listed there.
3. Read the active GitHub issue and its latest comments. GitHub owns status, scope, authorization, and decisions.
4. Use PCM only as the continuity helper configured in .continuity/config.json. Run continuity preflight and continuity validate before relying on local projections.
5. Check the setup reports on issue #1. Distinguish runtime-observed facts from agent-declared facts and unavailable values.

## Project identity and replacement barrier

The canonical GitHub repository defines the project. Runtime/provider does not: sessions from Codex/OpenAI, Claude Code, Grokbot, Grok agents, and other runtimes assigned to the same repository are part of the same project handoff. Different GitHub repositories are different projects.

Before cold-booting replacements for a repository, locate all old sessions assigned to it across runtimes. Each must publish a durable checkpoint to that repository's canonical GitHub state and stop. Start fresh replacements only after that handoff completes. If the old session is unreachable, verify its write authority has been fenced off before takeover; if that cannot be verified, do not permit concurrent writers.

## Current handoff

This repository is initialized with PCM and CGM as pinned Git submodules and a PCM continuity overlay. The active task is MAM-0001, collecting the current agents' real configuration, responsibilities, authorization, and cold-start/recovery instructions, including how old same-repository sessions checkpoint and stop across runtime/provider boundaries.

The owner will appoint a separate local GPT session as the authoritative owner for runtime design and implementation. This initializer is not that authority. Do not start runtime code until the appointed owner reviews the reports and records an accepted plan in GitHub.

Current Jev agents were asked to finish only a safe checkpoint, pause new Jev work, and report their setup on multi-agent-modules issue #1. Refresh those issues before assuming a response or ownership has changed.

## Recovery

After a process or device failure, reconstruct the next action from GitHub issue #1, the active GitHub task, and the pushed task/checkpoint records. Do not depend on this conversation, an existing live agent session, local chat memory, a private model-identity map, or environment secrets. Start a genuinely new connected session when exercising the future cold-start script.

## Not implemented

There is no starter script, agent launcher, DAG engine, A2A transport, telemetry collector, checkpoint automation, or PCM merge adapter in this repository yet. The acceptance target is in PROJECT.md.
