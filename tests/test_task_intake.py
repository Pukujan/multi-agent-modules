from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from runtime.task_intake import (
    SCHEMA_PATH,
    AutomationFacts,
    ReplacementFacts,
    VerifiedFacts,
    PRIORITY_RANK,
    resolve_intake,
    schema_errors,
)


REPO = "Pukujan/multi-agent-modules"
ISSUE = f"{REPO}#2"
COMMIT = "a" * 40


def automation_item(name: str, state: str = "not_installed") -> dict[str, object]:
    if state == "not_installed":
        return {
            "name": name,
            "state": state,
            "stop_action": None,
            "restart_action": None,
            "verified": True,
        }
    action = "pause /goal task-2" if state in {"active", "paused"} else f"stop {name}"
    restart = "resume /goal task-2" if state in {"active", "paused"} else f"restart {name}"
    return {
        "name": name,
        "state": state,
        "stop_action": action,
        "restart_action": restart,
        "verified": True,
    }


def make_record() -> dict[str, object]:
    return {
        "schema_version": "mam.task-intake.v1.2",
        "intake_id": "intake:test-1",
        "recorded_at": "2026-09-27T12:00:00Z",
        "target": {
            "canonical_repo": REPO,
            "remote_verified": True,
            "checkout_role": "canonical",
            "issue_ref": ISSUE,
        },
        "lane": {"provider": "Codex", "agent_alias": "codex-owner", "replacements": []},
        "requester": {"authority": "worker", "delegation_ref": None, "urgent": False},
        "action": "start",
        "task": {
            "issue_owner_agent_alias": "codex-owner",
            "owner_agent_alias": "codex-owner",
            "role": "resolver maintainer",
            "scope": "Implement the pure task-intake resolver.",
            "priority": "P1",
            "depends_on": [],
        },
        "checkpoint": {"state": "none", "commit": None, "issue_ref": None},
        "automation": {
            "goals": [automation_item("none on this host")],
            "scheduled_jobs": [automation_item("none on this host")],
            "watchdogs": [automation_item("none on this host")],
        },
        "authorization": {
            "may_write_repo": True,
            "may_stop_own_automation": True,
            "may_stop_other_lanes": False,
        },
    }


def automation_facts(groups: dict[str, list[dict[str, object]]]) -> tuple[AutomationFacts, ...]:
    return tuple(
        AutomationFacts(
            category=category,
            name=item["name"],
            state=item["state"],
            stop_action=item["stop_action"],
            restart_action=item["restart_action"],
        )
        for category, items in groups.items()
        for item in items
    )


def make_facts(record: dict[str, object] | None = None, **changes: object) -> VerifiedFacts:
    record = record or make_record()
    target = record["target"]
    lane = record["lane"]
    requester = record["requester"]
    task = record["task"]
    checkpoint = record["checkpoint"]
    replacements = lane["replacements"]
    default_replacements = tuple(
        ReplacementFacts(
            provider=item["provider"],
            agent_alias=item["agent_alias"],
            canonical_repo=target["canonical_repo"],
            session_reachable=item["session_reachable"],
            checkpoint_commit=item["checkpoint_commit"],
            checkpoint_published=item["checkpoint_published"],
            stop_verified=item["stop_verified"],
            write_authority_fenced=item["write_authority_fenced"],
            session_ref=item["session_ref"],
        )
        for item in replacements
    )
    defaults: dict[str, object] = {
        "canonical_repo": target["canonical_repo"],
        "issue_ref": target["issue_ref"],
        "remote_matches": True,
        "checkout_role": target["checkout_role"],
        "requester_authority": requester["authority"],
        "delegation_ref": requester["delegation_ref"],
        "issue_owner_agent_alias": task["issue_owner_agent_alias"],
        "task_role": task["role"],
        "task_scope": task["scope"],
        "task_priority": task["priority"],
        "issue_dependencies": frozenset(task["depends_on"]),
        "completed_dependencies": frozenset(task["depends_on"]),
        "checkpoint_state_verified": True,
        "checkpoint_commit": checkpoint["commit"],
        "checkpoint_issue_ref": checkpoint["issue_ref"],
        "checkpoint_published": checkpoint["state"] == "published",
        "automation_states_verified": True,
        "automation_inventory": automation_facts(record["automation"]),
        "prior_session_inventory_verified": True,
        "authorization_verified": True,
        "may_write_repo": record["authorization"]["may_write_repo"],
        "may_stop_own_automation": record["authorization"]["may_stop_own_automation"],
        "prior_sessions": default_replacements,
    }
    defaults.update(changes)
    return VerifiedFacts(**defaults)


def set_published_checkpoint(record: dict[str, object], commit: str = COMMIT) -> None:
    record["checkpoint"] = {"state": "published", "commit": commit, "issue_ref": ISSUE}


def replacement_record(
    *,
    provider: str = "Codex",
    agent_alias: str = "codex-previous",
    session_ref: str = "https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567890",
    reachable: bool = True,
    fenced: bool = False,
    stop_verified: bool = True,
    commit: str = COMMIT,
) -> dict[str, object]:
    return {
        "session_ref": session_ref,
        "provider": provider,
        "agent_alias": agent_alias,
        "session_reachable": reachable,
        "checkpoint_commit": commit,
        "checkpoint_published": True,
        "stop_verified": stop_verified,
        "write_authority_fenced": fenced,
    }


class TaskIntakeSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def assert_invalid(self, record: dict[str, object]) -> None:
        self.assertTrue(tuple(self.validator.iter_errors(record)))

    def test_schema_meta_validates_and_accepts_complete_baseline(self) -> None:
        self.assertEqual(schema_errors(make_record()), ())

    def test_schema_requires_every_cold_start_state(self) -> None:
        record = make_record()
        del record["automation"]
        self.assert_invalid(record)

        record = make_record()
        record["automation"]["goals"] = []
        self.assert_invalid(record)

    def test_schema_rejects_unsupported_version_and_action(self) -> None:
        record = make_record()
        record["schema_version"] = "mam.task-intake.v1.1"
        self.assert_invalid(record)

        record = make_record()
        record["action"] = "continue_forever"
        self.assert_invalid(record)

    def test_schema_cannot_claim_authority_to_stop_other_lanes(self) -> None:
        record = make_record()
        record["authorization"]["may_stop_other_lanes"] = True
        self.assert_invalid(record)

    def test_schema_requires_published_checkpoint_for_handoff(self) -> None:
        record = make_record()
        record["action"] = "handoff"
        self.assert_invalid(record)

    def test_schema_requires_goal_pause_and_restart_actions(self) -> None:
        record = make_record()
        record["automation"]["goals"] = [{
            "name": "task-2",
            "state": "paused",
            "stop_action": None,
            "restart_action": None,
            "verified": True,
        }]
        self.assert_invalid(record)


class TaskIntakeResolverTests(unittest.TestCase):
    def test_authorized_urgent_owner_stop_outranks_p0_and_returns_safe_plan(self) -> None:
        record = make_record()
        record["action"] = "stop"
        record["requester"] = {"authority": "owner", "delegation_ref": None, "urgent": True}
        record["task"]["priority"] = "P0"
        set_published_checkpoint(record)
        record["automation"] = {
            "goals": [automation_item("active goal", "active")],
            "scheduled_jobs": [automation_item("daily job", "active")],
            "watchdogs": [automation_item("repo watchdog", "active")],
        }

        result = resolve_intake(record, make_facts(record, requester_authority="owner"))

        self.assertEqual(result["status"], "plan")
        self.assertEqual(result["resolved_priority"], "urgent_owner")
        self.assertLess(PRIORITY_RANK[result["resolved_priority"]], PRIORITY_RANK["P0"])
        self.assertEqual(
            [control["operation"] for control in result["controls_to_stop"]],
            ["pause_goal", "stop_job", "stop_watchdog"],
        )
        self.assertEqual(result["issue_status_effect"], "unchanged")
        self.assertFalse(result["dispatch"])
        self.assertEqual(result["other_lanes_to_stop"], [])

    def test_worker_urgency_does_not_promote_p0(self) -> None:
        record = make_record()
        record["requester"]["urgent"] = True
        record["task"]["priority"] = "P0"

        result = resolve_intake(record, make_facts(record))

        self.assertEqual(result["status"], "dispatch")
        self.assertEqual(result["resolved_priority"], "P0")

    def test_dispatch_restores_task_role_authority_checkpoint_and_controls(self) -> None:
        record = make_record()
        record["action"] = "resume"
        set_published_checkpoint(record)
        record["automation"] = {
            "goals": [automation_item("task-2", "paused")],
            "scheduled_jobs": [automation_item("daily job", "stopped")],
            "watchdogs": [automation_item("none on this host")],
        }
        result = resolve_intake(record, make_facts(record))

        restored = result["restored_context"]
        self.assertEqual(result["status"], "dispatch")
        self.assertEqual(restored["intake"]["target"]["canonical_repo"], REPO)
        self.assertEqual(restored["intake"]["task"]["role"], "resolver maintainer")
        self.assertEqual(restored["intake"]["task"]["scope"], "Implement the pure task-intake resolver.")
        self.assertEqual(restored["intake"]["requester"]["authority"], "worker")
        self.assertEqual(restored["intake"]["checkpoint"]["commit"], COMMIT)
        self.assertEqual(restored["intake"]["automation"]["goals"][0]["state"], "paused")
        self.assertTrue(restored["verified_facts"]["checkpoint_state_verified"])
        self.assertTrue(restored["verified_facts"]["authorization_verified"])

    def test_recorded_owner_delegate_can_use_urgent_priority(self) -> None:
        record = make_record()
        record["requester"] = {
            "authority": "owner_delegate",
            "delegation_ref": "https://github.com/Pukujan/multi-agent-modules/issues/2#issuecomment-42",
            "urgent": True,
        }

        result = resolve_intake(
            record,
            make_facts(
                record,
                requester_authority="owner_delegate",
                delegation_ref=record["requester"]["delegation_ref"],
            ),
        )

        self.assertEqual(result["status"], "dispatch")
        self.assertEqual(result["resolved_priority"], "urgent_owner")

    def test_urgent_owner_stop_overrides_stale_priority_and_incomplete_dependencies(self) -> None:
        record = make_record()
        record["action"] = "stop"
        record["requester"] = {"authority": "owner", "delegation_ref": None, "urgent": True}
        record["task"]["priority"] = "P3"
        set_published_checkpoint(record)

        result = resolve_intake(
            record,
            make_facts(
                record,
                requester_authority="owner",
                task_priority="P0",
                issue_dependencies=frozenset({"Pukujan/multi-agent-modules#1"}),
                completed_dependencies=frozenset(),
            ),
        )

        self.assertEqual(result["status"], "plan")
        self.assertEqual(result["resolved_priority"], "urgent_owner")
        self.assertEqual(result["issue_status_effect"], "unchanged")

    def test_record_cannot_impersonate_an_authenticated_owner(self) -> None:
        record = make_record()
        record["requester"] = {"authority": "owner", "delegation_ref": None, "urgent": True}

        result = resolve_intake(record, make_facts(record, requester_authority="worker"))

        self.assertEqual(result["status"], "unresolved")
        self.assertIsNone(result["resolved_priority"])
        self.assertFalse(result["dispatch"])
        self.assertTrue(any("authenticated GitHub authority" in item for item in result["reasons"]))

    def test_issue_reference_must_match_the_verified_github_issue(self) -> None:
        record = make_record()
        record["target"]["issue_ref"] = f"{REPO}#999"

        result = resolve_intake(record, make_facts(record, issue_ref=ISSUE))

        self.assertEqual(result["status"], "unresolved")
        self.assertTrue(any("independently verified GitHub issue" in item for item in result["reasons"]))

    def test_claimed_automation_must_match_observed_inventory(self) -> None:
        record = make_record()
        record["automation"]["scheduled_jobs"] = [automation_item("daily job", "stopped")]
        observed = automation_facts(make_record()["automation"])

        result = resolve_intake(record, make_facts(record, automation_inventory=observed))

        self.assertEqual(result["status"], "unresolved")
        self.assertTrue(any("does not match the independently verified control inventory" in item
                            for item in result["reasons"]))

    def test_record_cannot_promote_priority_expand_scope_or_grant_permissions(self) -> None:
        cases = []
        record = make_record()
        record["task"]["priority"] = "P0"
        cases.append((record, {"task_priority": "P3"}))

        record = make_record()
        record["task"]["scope"] = "All repository files"
        cases.append((record, {"task_scope": "Only the task-intake resolver"}))

        record = make_record()
        record["authorization"]["may_write_repo"] = True
        cases.append((record, {"may_write_repo": False}))

        for candidate, fact_changes in cases:
            with self.subTest(fact_changes=fact_changes):
                result = resolve_intake(candidate, make_facts(candidate, **fact_changes))
                self.assertEqual(result["status"], "unresolved")
                self.assertFalse(result["dispatch"])

    def test_record_cannot_omit_canonical_issue_dependencies(self) -> None:
        record = make_record()
        issue_dependencies = frozenset({"Pukujan/multi-agent-modules#1"})

        result = resolve_intake(
            record,
            make_facts(record, issue_dependencies=issue_dependencies, completed_dependencies=issue_dependencies),
        )

        self.assertEqual(result["status"], "unresolved")
        self.assertTrue(any("do not match" in item for item in result["reasons"]))

    def test_same_lane_replacement_requires_published_checkpoint_and_verified_stop(self) -> None:
        record = make_record()
        record["action"] = "resume"
        set_published_checkpoint(record)
        record["lane"]["replacements"] = [replacement_record()]
        record["automation"] = {
            "goals": [automation_item("task-2 goal", "paused")],
            "scheduled_jobs": [automation_item("daily job", "stopped")],
            "watchdogs": [automation_item("repo watcher", "not_installed")],
        }
        actual = ReplacementFacts(
            provider="Codex",
            agent_alias="codex-previous",
            canonical_repo=REPO,
            session_reachable=True,
            checkpoint_commit=COMMIT,
            checkpoint_published=True,
            stop_verified=True,
            write_authority_fenced=False,
            session_ref="https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567890",
        )

        result = resolve_intake(
            record,
            make_facts(record, prior_sessions=(actual,)),
        )

        self.assertEqual(result["status"], "dispatch")
        self.assertEqual(result["replaced_session"], [{
            "session_ref": "https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567890",
            "provider": "Codex",
            "agent_alias": "codex-previous",
        }])
        self.assertEqual(result["other_lanes_to_stop"], [])

    def test_stop_records_prior_session_inventory_without_replacing_it(self) -> None:
        record = make_record()
        record["action"] = "stop"
        record["requester"] = {"authority": "owner", "delegation_ref": None, "urgent": True}
        set_published_checkpoint(record)
        previous = replacement_record()
        record["lane"]["replacements"] = [previous]

        result = resolve_intake(record, make_facts(record, requester_authority="owner"))

        self.assertEqual(result["status"], "plan")
        self.assertIsNone(result["replaced_session"])
        self.assertEqual(result["other_lanes_to_stop"], [])

    def test_cross_provider_replacement_is_refused_without_stopping_that_lane(self) -> None:
        record = make_record()
        record["action"] = "resume"
        set_published_checkpoint(record)
        record["lane"]["replacements"] = [replacement_record(provider="Claude Code", agent_alias="claude-old")]
        record["automation"]["goals"] = [automation_item("paused goal", "paused")]
        record["automation"]["scheduled_jobs"] = [automation_item("stopped job", "stopped")]
        actual = ReplacementFacts(
            provider="Claude Code",
            agent_alias="claude-old",
            canonical_repo=REPO,
            session_reachable=True,
            checkpoint_commit=COMMIT,
            checkpoint_published=True,
            stop_verified=True,
            write_authority_fenced=False,
            session_ref="https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567890",
        )

        result = resolve_intake(
            record,
            make_facts(record, prior_sessions=(actual,)),
        )

        self.assertEqual(result["status"], "unresolved")
        self.assertFalse(result["dispatch"])
        self.assertEqual(result["other_lanes_to_stop"], [])
        self.assertTrue(any("cross-provider" in item for item in result["reasons"]))

    def test_unreachable_prior_session_requires_a_write_fence(self) -> None:
        record = make_record()
        record["action"] = "resume"
        set_published_checkpoint(record)
        record["lane"]["replacements"] = [replacement_record(reachable=False, fenced=False)]
        record["automation"]["goals"] = [automation_item("paused goal", "paused")]
        record["automation"]["scheduled_jobs"] = [automation_item("stopped job", "stopped")]
        actual = ReplacementFacts(
            "Codex", "codex-previous", REPO, False, COMMIT, True, True, False,
            "https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567890",
        )

        result = resolve_intake(
            record,
            make_facts(record, prior_sessions=(actual,)),
        )

        self.assertEqual(result["status"], "unresolved")
        self.assertTrue(any("write fence" in item for item in result["reasons"]))

    def test_replacement_requires_evidence_for_every_prior_same_lane_session(self) -> None:
        record = make_record()
        record["action"] = "resume"
        set_published_checkpoint(record)
        first = replacement_record()
        second = replacement_record(
            agent_alias="codex-older",
            session_ref="https://github.com/Pukujan/multi-agent-modules/issues/1#issuecomment-1234567891",
        )
        record["lane"]["replacements"] = [first]
        record["automation"]["goals"] = [automation_item("paused goal", "paused")]
        record["automation"]["scheduled_jobs"] = [automation_item("stopped job", "stopped")]
        actual_first = ReplacementFacts(
            provider="Codex", agent_alias="codex-previous", canonical_repo=REPO,
            session_reachable=True, checkpoint_commit=COMMIT, checkpoint_published=True,
            stop_verified=True, write_authority_fenced=False, session_ref=first["session_ref"],
        )
        actual_second = ReplacementFacts(
            provider="Codex", agent_alias="codex-older", canonical_repo=REPO,
            session_reachable=True, checkpoint_commit=COMMIT, checkpoint_published=True,
            stop_verified=True, write_authority_fenced=False, session_ref=second["session_ref"],
        )

        omitted = resolve_intake(
            record,
            make_facts(record, prior_sessions=(actual_first, actual_second)),
        )
        record["lane"]["replacements"] = [first, second]
        complete = resolve_intake(
            record,
            make_facts(record, prior_sessions=(actual_first, actual_second)),
        )

        self.assertEqual(omitted["status"], "unresolved")
        self.assertTrue(any("omits verified prior sessions" in item for item in omitted["reasons"]))
        self.assertEqual(complete["status"], "dispatch")
        self.assertEqual(len(complete["replaced_session"]), 2)

    def test_fail_closed_on_unverified_target_owner_dependencies_and_automation(self) -> None:
        cases: list[tuple[str, dict[str, object], dict[str, object]]] = []

        record = make_record()
        cases.append(("remote", record, {"remote_matches": False}))

        record = make_record()
        record["target"]["checkout_role"] = "collision"
        cases.append(("checkout", record, {"checkout_role": "collision"}))

        record = make_record()
        record["requester"]["authority"] = "unknown"
        cases.append(("authority", record, {"requester_authority": "unknown"}))

        record = make_record()
        record["task"]["depends_on"] = ["Pukujan/multi-agent-modules#1"]
        cases.append(("dependency", record, {"completed_dependencies": frozenset()}))

        record = make_record()
        record["automation"]["goals"] = [{
            "name": "unavailable goal", "state": "unavailable",
            "stop_action": None, "restart_action": None, "verified": None,
        }]
        cases.append(("automation", record, {}))

        record = make_record()
        cases.append(("checkpoint observation", record, {"checkpoint_state_verified": False}))

        record = make_record()
        cases.append(("session inventory", record, {"prior_session_inventory_verified": False}))

        record = make_record()
        record["task"]["issue_owner_agent_alias"] = "someone-else"
        cases.append(("issue owner", record, {}))

        for name, candidate, fact_changes in cases:
            with self.subTest(name=name):
                result = resolve_intake(candidate, make_facts(candidate, **fact_changes))
                self.assertEqual(result["status"], "unresolved")
                self.assertFalse(result["dispatch"])

    def test_active_own_controls_block_start_and_paused_goal_requires_resume(self) -> None:
        record = make_record()
        record["automation"]["goals"] = [automation_item("active goal", "active")]
        result = resolve_intake(record, make_facts(record))
        self.assertEqual(result["status"], "unresolved")

        record = make_record()
        record["automation"]["goals"] = [automation_item("paused goal", "paused")]
        result = resolve_intake(record, make_facts(record))
        self.assertEqual(result["status"], "unresolved")
        self.assertTrue(any("resume action" in item for item in result["reasons"]))

    def test_stop_plan_is_deterministic_when_control_order_changes(self) -> None:
        record = make_record()
        record["action"] = "handoff"
        record["requester"] = {"authority": "owner", "delegation_ref": None, "urgent": True}
        set_published_checkpoint(record)
        record["automation"] = {
            "goals": [automation_item("z goal", "active"), automation_item("a goal", "active")],
            "scheduled_jobs": [automation_item("z job", "active"), automation_item("a job", "active")],
            "watchdogs": [automation_item("z watcher", "active"), automation_item("a watcher", "active")],
        }
        facts = make_facts(record, requester_authority="owner")
        first = resolve_intake(record, facts)

        shuffled = copy.deepcopy(record)
        for controls in shuffled["automation"].values():
            controls.reverse()
        second = resolve_intake(shuffled, facts)

        self.assertEqual(first, second)
        self.assertEqual(first["status"], "plan")
        self.assertEqual(first["issue_status_effect"], "unchanged")

    def test_schema_errors_are_stable_and_refuse_without_routing(self) -> None:
        record = make_record()
        record["schema_version"] = "mam.task-intake.v0-draft"
        first = resolve_intake(record, make_facts(record))
        second = resolve_intake(record, make_facts(record))
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "refused")
        self.assertIsNone(first["route_to"])
        self.assertFalse(first["dispatch"])
        self.assertTrue(first["reasons"])


if __name__ == "__main__":
    unittest.main()
