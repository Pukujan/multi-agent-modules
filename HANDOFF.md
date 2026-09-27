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

This repository is initialized with PCM and CGM as pinned Git submodules and a PCM continuity overlay. The active task is MAM-0001, collecting the current agents' real configuration, responsibilities, authorization, and cold-start/recovery instructions, including same-lane handoff and target checkout discovery.

The owner will appoint a separate local GPT session as the authoritative owner for runtime design and implementation. This initializer is not that authority. Do not start runtime code until the appointed owner reviews the reports and records an accepted plan in GitHub.

Current Jev agents were asked to finish only a safe checkpoint, pause new Jev work, and report their setup on multi-agent-modules issue #1. Refresh those issues before assuming a response or ownership has changed.

The owner also instructed each Jev agent to pause its own Jev goal and any Jev-specific scheduled watchdog it controls after the handoff appears in both repos. Record the goal/job name or ID, verified stopped status, exact stop action, and restart action. On macOS, if installed, the JEV storage-watchdog removal is `scripts/install_watchdog_launchagent.sh --uninstall`; verify the LaunchAgent is unloaded and its plist is removed. Do not stop another provider's session or another project's automation.

MAM issue [#2](https://github.com/Pukujan/multi-agent-modules/issues/2) records the missing strict task-classification and urgent-owner-priority policy. It awaits the future owner-appointed GPT session's decision; implementation has not been authorized.

## Recovery

After a process or device failure, reconstruct the next action from GitHub issue #1, the active GitHub task, and the pushed task/checkpoint records. Do not depend on this conversation, an existing live agent session, local chat memory, a private model-identity map, or environment secrets. Start a genuinely new connected session when exercising the future cold-start script.

## Not implemented

There is no starter script, agent launcher, DAG engine, A2A transport, telemetry collector, checkpoint automation, or PCM merge adapter in this repository yet. The acceptance target is in PROJECT.md.
