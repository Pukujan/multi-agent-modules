# Handoff

## Start here

1. Confirm this is the repository https://github.com/Pukujan/multi-agent-modules and refresh its current GitHub state.
2. Read PROJECT.md, checkpoints/CURRENT.md, and the active task listed there.
3. Read the active GitHub issue and its latest comments. GitHub owns status, scope, authorization, and decisions.
4. Use PCM only as the continuity helper configured in .continuity/config.json. Run continuity preflight and continuity validate before relying on local projections.
5. Check the setup reports on issue #1. Distinguish runtime-observed facts from agent-declared facts and unavailable values.

## Project identity and replacement boundary

The canonical GitHub repository the agent is working for defines the project. The runtime's own initialization folder does not. Keep one canonical checkout per device: `D:\claude\<project>` on Windows and `~/Documents/projects/<project>` on the MacBook. PCM already provides canonical-checkout guidance, a per-device private workspace registry, and `workspace.mode: single-checkout` to refuse managed worktrees. Use those instead of creating another workspace manager. PCM does not scan drives or discover unregistered clones, so the bootstrap must resolve the target through the designated path and known registry entries, verify the GitHub remote, and start the session from the existing checkout. Do not clone a second copy just to cold-start. If multiple copies make the canonical checkout unclear, preserve local work and record the collision for authoritative resolution.

Replace only an older session in the same runtime lane assigned to that same repository. For example, a new Codex session takes over from an old Codex session after its checkpoint and stop; Claude Code or Grok must not stop or replace Codex. Other runtime lanes may continue working on the repository under their own GitHub task ownership and branch/PR scopes.

If the old same-lane session is unreachable, verify its write authority has been fenced off before takeover; if that cannot be verified, do not allow a concurrent same-lane writer.

## Current handoff

This repository is initialized with PCM and CGM as pinned Git submodules and a PCM continuity overlay. The current authoritative task is MAM-0002 on issue #2, designing and implementing the task-intake and urgent-owner-priority contract. The project owner appointed the current Codex task as authority; the appointment, scope, and branch are recorded on issue #2.

MAM-0001 / issue #1 remains open for current-agent setup and recovery reports. Its missing reports remain unresolved. The current authority has begun the separate issue #2 contract task while preserving issue #1 as an open inventory task; do not claim the inventory is complete.

Current Jev agents were asked to finish only a safe checkpoint, pause new Jev work, and report their setup on multi-agent-modules issue #1. Refresh those issues before assuming a response or ownership has changed.

The owner also instructed each Jev agent to pause its own Jev goal and any Jev-specific scheduled watchdog it controls after the handoff appears in both repos. Record the goal/job name or ID, verified stopped status, exact stop action, and restart action. On macOS, if installed, the JEV storage-watchdog removal is `scripts/install_watchdog_launchagent.sh --uninstall`; verify the LaunchAgent is unloaded and its plist is removed. Do not stop another provider's session or another project's automation.

For MAM-0002, read the latest issue #2 decision and the task-intake proposal. Schema v1.1 was accepted in comment 5852760046, then amended before code delivery by comment 5852850796 to list every prior same-lane session. Schema v1.2 requires final acceptance before any resolver work is committed or pushed. Keep PCM's `schemas/v1/` untouched. The full launcher/runtime and three fresh-session demonstrations remain outstanding.

## Recovery

After a process or device failure, reconstruct the next action from GitHub issue #1, the active GitHub task, and the pushed task/checkpoint records. Do not depend on this conversation, an existing live agent session, local chat memory, a private model-identity map, or environment secrets. Start a genuinely new connected session when exercising the future cold-start script.

## Not implemented

There is no starter script, agent launcher, DAG engine, A2A transport, telemetry collector, checkpoint automation, or PCM merge adapter in this repository yet. The acceptance target is in PROJECT.md.
