"""Deterministic, side-effect-free routing for MAM task-intake v1.2."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "mam" / "v1" / "task-intake.schema.json"
PRIORITY_RANK = {"urgent_owner": 0, "P0": 1, "P1": 2, "P2": 3, "P3": 4}
KNOWN_AUTHORITIES = {"owner", "owner_delegate", "arbiter", "worker"}


@dataclass(frozen=True)
class ReplacementFacts:
    """Prior-session evidence independently read from GitHub/runtime controls."""

    provider: str
    agent_alias: str
    canonical_repo: str
    session_reachable: bool
    checkpoint_commit: str
    checkpoint_published: bool
    stop_verified: bool
    write_authority_fenced: bool
    session_ref: str


@dataclass(frozen=True)
class AutomationFacts:
    """One control observed in the recipient's owning runtime."""

    category: str
    name: str
    state: str
    stop_action: str | None
    restart_action: str | None


@dataclass(frozen=True)
class VerifiedFacts:
    """Facts a caller verified outside the untrusted intake record.

    The resolver never treats a record's booleans as authentication. The caller
    must derive these values from the GitHub identity/issue, the canonical
    checkout and PCM, and the runtime controls for this provider lane.
    """

    canonical_repo: str | None
    issue_ref: str | None
    remote_matches: bool
    checkout_role: str
    requester_authority: str
    delegation_ref: str | None
    issue_owner_agent_alias: str | None
    task_role: str | None
    task_scope: str | None
    task_priority: str | None
    issue_dependencies: frozenset[str]
    completed_dependencies: frozenset[str]
    checkpoint_state_verified: bool
    checkpoint_commit: str | None
    checkpoint_issue_ref: str | None
    checkpoint_published: bool
    automation_states_verified: bool
    automation_inventory: tuple[AutomationFacts, ...]
    prior_session_inventory_verified: bool
    authorization_verified: bool
    may_write_repo: bool
    may_stop_own_automation: bool
    prior_sessions: tuple[ReplacementFacts, ...] = ()


def load_schema() -> dict[str, Any]:
    """Load the accepted, MAM-owned intake schema."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def schema_errors(record: Mapping[str, Any]) -> tuple[str, ...]:
    """Return stable, human-readable schema errors (empty means valid)."""
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(record),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    return tuple(
        f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in errors
    )


def _same(left: str | None, right: str | None) -> bool:
    return left is not None and right is not None and left.casefold() == right.casefold()


def _refers_to_repo(issue_ref: str | None, canonical_repo: str) -> bool:
    return bool(issue_ref) and issue_ref.casefold().startswith(f"{canonical_repo}#".casefold())


def _result(
    status: str,
    *,
    route_to: str | None,
    reasons: tuple[str, ...] = (),
    resolved_priority: str | None = None,
    actions: tuple[dict[str, Any], ...] = (),
    controls_to_stop: tuple[dict[str, str], ...] = (),
    replaced_session: list[dict[str, str]] | None = None,
    restored_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "route_to": route_to,
        "dispatch": status == "dispatch",
        "resolved_priority": resolved_priority,
        "priority_rank": PRIORITY_RANK.get(resolved_priority) if resolved_priority else None,
        "reasons": list(reasons),
        "actions": list(actions),
        "controls_to_stop": list(controls_to_stop),
        "replaced_session": replaced_session,
        "restored_context": restored_context,
        "other_lanes_to_stop": [],
        "issue_status_effect": "unchanged",
    }


def _automation_issues(record: Mapping[str, Any], facts: VerifiedFacts) -> list[str]:
    if not facts.automation_states_verified:
        return ["automation state was not independently verified"]

    issues: list[str] = []
    groups = record["automation"]
    claimed_controls: dict[tuple[str, str], tuple[str, str | None, str | None]] = {}
    for category in ("goals", "scheduled_jobs", "watchdogs"):
        items = groups[category]
        names = [item["name"].casefold() for item in items]
        if len(names) != len(set(names)):
            issues.append(f"{category} contains duplicate names")
        if any(item["state"] in {"unknown", "unavailable"} for item in items):
            issues.append(f"{category} contains unknown or unavailable state")
        if any(item["state"] == "not_installed" for item in items) and len(items) != 1:
            issues.append(f"{category} mixes not_installed with other controls")
        claimed_controls.update(
            {
                (category, item["name"].casefold()): (
                    item["state"], item["stop_action"], item["restart_action"]
                )
                for item in items
            }
        )

    observed_controls: dict[tuple[str, str], tuple[str, str | None, str | None]] = {}
    for item in facts.automation_inventory:
        key = (item.category, item.name.casefold())
        if key in observed_controls:
            issues.append("verified automation inventory contains duplicate controls")
        observed_controls[key] = (item.state, item.stop_action, item.restart_action)
    if claimed_controls != observed_controls:
        issues.append("intake automation does not match the independently verified control inventory")

    return issues


def _replacement_issues(record: Mapping[str, Any], facts: VerifiedFacts) -> list[str]:
    lane = record["lane"]
    claimed = lane["replacements"]
    observed_by_ref = {item.session_ref: item for item in facts.prior_sessions}
    claimed_by_ref = {item["session_ref"]: item for item in claimed}
    issues: list[str] = []

    if not facts.prior_session_inventory_verified:
        issues.append("complete prior same-lane session inventory was not independently verified")

    if len(claimed_by_ref) != len(claimed):
        issues.append("replacement list contains duplicate session references")
    if len(observed_by_ref) != len(facts.prior_sessions):
        issues.append("verified prior-session list contains duplicate references")
    missing = sorted(set(observed_by_ref) - set(claimed_by_ref))
    extra = sorted(set(claimed_by_ref) - set(observed_by_ref))
    if missing:
        issues.append("intake omits verified prior sessions: " + ", ".join(missing))
    if extra:
        issues.append("replacement evidence was not independently verified: " + ", ".join(extra))

    for session_ref in sorted(set(claimed_by_ref) & set(observed_by_ref)):
        claim = claimed_by_ref[session_ref]
        observed = observed_by_ref[session_ref]
        if not _same(claim["provider"], lane["provider"]):
            issues.append(f"cross-provider replacement is forbidden: {session_ref}")
        if not _same(observed.provider, lane["provider"]):
            issues.append(f"verified prior session belongs to a different provider lane: {session_ref}")
        if not _same(claim["agent_alias"], observed.agent_alias):
            issues.append(f"replacement alias does not match verified prior session: {session_ref}")
        if not _same(observed.canonical_repo, record["target"]["canonical_repo"]):
            issues.append(f"verified prior session belongs to a different repository: {session_ref}")
        if claim["checkpoint_commit"].casefold() != observed.checkpoint_commit.casefold():
            issues.append(f"replacement checkpoint does not match verified checkpoint: {session_ref}")
        if not (claim["checkpoint_published"] and observed.checkpoint_published):
            issues.append(f"replacement checkpoint is not verified as published: {session_ref}")
        if not (claim["stop_verified"] and observed.stop_verified):
            issues.append(f"replacement stop is not verified: {session_ref}")
        if claim["session_reachable"] != observed.session_reachable:
            issues.append(f"replacement reachability does not match observed state: {session_ref}")
        if claim["write_authority_fenced"] != observed.write_authority_fenced:
            issues.append(f"replacement write-fence state does not match observed state: {session_ref}")
        if not observed.session_reachable and not observed.write_authority_fenced:
            issues.append(f"unreachable prior session has no verified write fence: {session_ref}")

    return issues


def _fact_issues(record: Mapping[str, Any], facts: VerifiedFacts) -> list[str]:
    target = record["target"]
    requester = record["requester"]
    task = record["task"]
    lane = record["lane"]
    checkpoint = record["checkpoint"]
    action = record["action"]
    issues: list[str] = []

    if not target["remote_verified"] or not facts.remote_matches:
        issues.append("canonical GitHub remote is not independently verified")
    if not _same(target["canonical_repo"], facts.canonical_repo):
        issues.append("intake repository does not match the independently verified remote")
    if target["checkout_role"] != "canonical" or facts.checkout_role != "canonical":
        issues.append("checkout is not verified as the one canonical checkout")
    if not _refers_to_repo(target["issue_ref"], target["canonical_repo"]):
        issues.append("task issue reference does not belong to the canonical repository")
    if not _same(target["issue_ref"], facts.issue_ref):
        issues.append("intake issue reference does not match the independently verified GitHub issue")

    if requester["authority"] not in KNOWN_AUTHORITIES or requester["authority"] == "unknown":
        issues.append("requester authority is unknown")
    if requester["authority"] != facts.requester_authority:
        issues.append("requester authority claim does not match authenticated GitHub authority")
    if requester["authority"] == "owner_delegate":
        if not requester["delegation_ref"]:
            issues.append("owner delegation has no durable reference")
        if not facts.delegation_ref or requester["delegation_ref"] != facts.delegation_ref:
            issues.append("owner delegation is not independently verified")

    aliases = (task["issue_owner_agent_alias"], task["owner_agent_alias"], lane["agent_alias"])
    if len({alias.casefold() for alias in aliases}) != 1:
        issues.append("issue owner, assigned task owner, and lane alias do not match")
    if not _same(task["issue_owner_agent_alias"], facts.issue_owner_agent_alias):
        issues.append("task owner does not match canonical GitHub issue ownership")
    if task["role"] != facts.task_role:
        issues.append("task role does not match the authoritative issue assignment")
    if task["scope"] != facts.task_scope:
        issues.append("task scope does not match the authoritative issue scope")
    if facts.task_priority not in {"P0", "P1", "P2", "P3"}:
        issues.append("canonical GitHub task priority is unknown")
    if action in {"start", "resume"} and task["priority"] != facts.task_priority:
        issues.append("task priority does not match canonical GitHub priority")

    if action in {"start", "resume"}:
        if set(task["depends_on"]) != set(facts.issue_dependencies):
            issues.append("intake dependencies do not match the canonical issue dependency list")
        incomplete = sorted(set(facts.issue_dependencies) - set(facts.completed_dependencies))
        if incomplete:
            issues.append("dependencies are not verified complete: " + ", ".join(incomplete))

    if not facts.checkpoint_state_verified:
        issues.append("current checkpoint presence/state was not independently verified")
    if checkpoint["state"] == "unavailable":
        issues.append("current checkpoint is unavailable")
    elif checkpoint["state"] == "published":
        if not facts.checkpoint_published:
            issues.append("checkpoint is not independently verified as published")
        if checkpoint["commit"] != facts.checkpoint_commit:
            issues.append("checkpoint commit does not match the verified checkpoint")
        if not _same(checkpoint["issue_ref"], facts.checkpoint_issue_ref):
            issues.append("checkpoint issue does not match the verified checkpoint")
    elif facts.checkpoint_published or facts.checkpoint_commit is not None:
        issues.append("intake omits the existing published checkpoint")

    issues.extend(_automation_issues(record, facts))
    issues.extend(_replacement_issues(record, facts))

    if not facts.authorization_verified:
        issues.append("repository and self-automation permissions were not independently verified")
    elif (
        record["authorization"]["may_write_repo"] != facts.may_write_repo
        or record["authorization"]["may_stop_own_automation"] != facts.may_stop_own_automation
    ):
        issues.append("authorization claims do not match verified permissions")

    if action in {"start", "resume"}:
        goal_states = [item["state"] for item in record["automation"]["goals"]]
        if "active" in goal_states:
            issues.append("an active goal must be paused and checkpointed before dispatch")
        if action == "start" and "paused" in goal_states:
            issues.append("a paused goal requires resume action, not start")
        for category in ("scheduled_jobs", "watchdogs"):
            if any(item["state"] == "active" for item in record["automation"][category]):
                issues.append(f"active {category} must be stopped before dispatch")

    if action in {"stop", "handoff"}:
        authorization = record["authorization"]
        if not (authorization["may_write_repo"] and facts.may_write_repo):
            issues.append("stop/handoff cannot publish a checkpoint without repository write authority")
        if not (authorization["may_stop_own_automation"] and facts.may_stop_own_automation):
            issues.append("stop/handoff is not authorized to pause/stop the recipient's own controls")

    return issues


def _stop_plan(record: Mapping[str, Any]) -> tuple[tuple[dict[str, Any], ...], tuple[dict[str, str], ...]]:
    actions: list[dict[str, Any]] = [
        {"step": "publish_checkpoint", "detail": "Commit and publish recoverable current task state."},
        {"step": "publish_handoff", "detail": "Cross-link the handoff on the task and collection issues."},
    ]
    controls: list[dict[str, str]] = []
    categories = (
        ("goals", "pause_goal"),
        ("scheduled_jobs", "stop_job"),
        ("watchdogs", "stop_watchdog"),
    )
    for category, operation in categories:
        for item in sorted(record["automation"][category], key=lambda entry: entry["name"].casefold()):
            if item["state"] == "active":
                controls.append({
                    "category": category,
                    "name": item["name"],
                    "operation": operation,
                    "action": item["stop_action"],
                    "restart_action": item["restart_action"],
                })
    actions.extend([
        {"step": "apply_own_control_actions", "detail": "Pause active goals and stop active scheduled jobs/watchdogs listed below."},
        {"step": "verify_and_record", "detail": "Verify paused/stopped states and record exact restart actions."},
        {"step": "stop_session", "detail": "Stop only after the checkpoint and own-control states are published."},
    ])
    return tuple(actions), tuple(controls)


def _restored_context(record: Mapping[str, Any], facts: VerifiedFacts) -> dict[str, Any]:
    """Carry the accepted task record and verified observations to the caller."""
    intake = deepcopy(dict(record))
    intake["task"]["depends_on"] = sorted(intake["task"]["depends_on"], key=str.casefold)
    intake["lane"]["replacements"] = sorted(
        intake["lane"]["replacements"], key=lambda item: item["session_ref"]
    )
    for category in ("goals", "scheduled_jobs", "watchdogs"):
        intake["automation"][category] = sorted(
            intake["automation"][category], key=lambda item: item["name"].casefold()
        )
    return {
        "intake": intake,
        "verified_facts": {
            "canonical_repo": facts.canonical_repo,
            "issue_ref": facts.issue_ref,
            "remote_matches": facts.remote_matches,
            "checkout_role": facts.checkout_role,
            "requester_authority": facts.requester_authority,
            "delegation_ref": facts.delegation_ref,
            "issue_owner_agent_alias": facts.issue_owner_agent_alias,
            "task_role": facts.task_role,
            "task_scope": facts.task_scope,
            "task_priority": facts.task_priority,
            "issue_dependencies": sorted(facts.issue_dependencies),
            "completed_dependencies": sorted(facts.completed_dependencies),
            "checkpoint_state_verified": facts.checkpoint_state_verified,
            "checkpoint_commit": facts.checkpoint_commit,
            "checkpoint_issue_ref": facts.checkpoint_issue_ref,
            "checkpoint_published": facts.checkpoint_published,
            "automation_states_verified": facts.automation_states_verified,
            "automation_inventory": [
                asdict(item) for item in sorted(
                    facts.automation_inventory,
                    key=lambda entry: (entry.category, entry.name.casefold()),
                )
            ],
            "prior_session_inventory_verified": facts.prior_session_inventory_verified,
            "prior_sessions": [
                asdict(item) for item in sorted(facts.prior_sessions, key=lambda entry: entry.session_ref)
            ],
            "authorization_verified": facts.authorization_verified,
            "may_write_repo": facts.may_write_repo,
            "may_stop_own_automation": facts.may_stop_own_automation,
        },
    }


def resolve_intake(record: Mapping[str, Any], facts: VerifiedFacts) -> dict[str, Any]:
    """Validate and resolve an intake without launching or stopping anything."""
    errors = schema_errors(record)
    if errors:
        return _result("refused", route_to=None, reasons=errors)

    issues = _fact_issues(record, facts)
    if issues:
        return _result("unresolved", route_to="project_authority", reasons=tuple(issues))

    requester = record["requester"]
    urgent_owner = requester["urgent"] and requester["authority"] in {"owner", "owner_delegate"}
    priority = "urgent_owner" if urgent_owner else facts.task_priority

    if record["action"] in {"stop", "handoff"}:
        actions, controls = _stop_plan(record)
        return _result(
            "plan",
            route_to="current_session",
            resolved_priority=priority,
            actions=actions,
            controls_to_stop=controls,
            restored_context=_restored_context(record, facts),
        )

    replaced = [
        {"session_ref": item["session_ref"], "provider": item["provider"], "agent_alias": item["agent_alias"]}
        for item in sorted(record["lane"]["replacements"], key=lambda entry: entry["session_ref"])
    ]
    return _result(
        "dispatch",
        route_to="fresh_session",
        resolved_priority=priority,
        replaced_session=replaced,
        restored_context=_restored_context(record, facts),
    )
