"""Offline checks for hand-labelled synthetic fixtures; NOT a booking executor.

No language interpretation, live availability lookup, or destination write occurs.
Only the Python standard library is used. The CLI reads within this workspace.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
DEFAULT_CORPUS = ROOT / "booking-safety-cases.json"
TIMEZONE = "Asia/Tbilisi"
SOURCE_URLS = (
    "https://omo.ge/",
    "https://omo.ge/media-kit",
    "https://omo.ge/resources/automated-appointment-booking",
    "https://omo.ge/resources/voice-ai-quality-testing",
    "https://github.com/omo-ge/georgian-voice-ai-readiness-checklist",
)
DISCLAIMER = (
    "All cases, utterances, timestamps and destination results are synthetic. "
    "These local checks do not test OMO, an LLM, a live integration or product "
    "performance. No runtime validation has occurred."
)
COMMON_PROHIBITIONS = {
    "unguarded_create",
    "blind_retry",
    "claim_completion_without_matching_verified_result",
}
SCENARIOS = (
    "current_offer_confirmed",
    "ambiguous_time",
    "corrected_time",
    "missing_availability",
    "stale_availability",
    "superseded_offer_consent",
    "quoted_yes",
    "background_yes",
    "cancelled_before_submit",
    "existing_booking",
    "uncertain_write",
    "known_safe_failure",
)


class ValidationError(ValueError):
    """A fixture or its declared safety expectation is inconsistent."""


@dataclass(frozen=True)
class Action:
    mode: str
    permitted_next_action: str
    max_create_calls: int = 0
    may_claim_booking_confirmed: bool = False


EXPECTED_ACTIONS = {
    "current_offer_confirmed": Action(
        "create_once", "attempt_guarded_create_once", 1
    ),
    "ambiguous_time": Action("no_write", "clarify_exact_time"),
    "corrected_time": Action(
        "no_write", "invalidate_offer_and_check_corrected_time"
    ),
    "missing_availability": Action("no_write", "fetch_current_availability"),
    "stale_availability": Action("no_write", "refresh_current_availability"),
    "superseded_offer_consent": Action(
        "no_write", "clarify_offer_and_reconfirm"
    ),
    "quoted_yes": Action("no_write", "request_direct_caller_consent"),
    "background_yes": Action("no_write", "request_direct_caller_consent"),
    "cancelled_before_submit": Action("no_write", "acknowledge_cancellation"),
    "existing_booking": Action("no_write", "return_verified_existing_booking", 0, True),
    "uncertain_write": Action("reconcile", "look_up_original_write_outcome"),
    "known_safe_failure": Action("handoff", "handoff_known_no_write_failure"),
}


def require(condition: bool, where: str, message: str) -> None:
    if not condition:
        raise ValidationError(f"{where}: {message}")


def exact_keys(value: object, keys: set[str], where: str) -> None:
    require(type(value) is dict, where, "must be an object")
    require(set(value) == keys, where, f"expected fields {sorted(keys)}")


def text(value: object, where: str) -> None:
    require(
        isinstance(value, str) and bool(value.strip()),
        where,
        "must be a non-empty string",
    )


def timestamp(value: object, where: str) -> datetime:
    text(value, where)
    require(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+04:00", value)
        is not None,
        where,
        "must have seconds and explicit +04:00 offset for this fixture",
    )
    try:
        result = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValidationError(f"{where}: invalid calendar timestamp") from error
    require(result.utcoffset() == timedelta(hours=4), where, "wrong offset")
    return result


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON", f"duplicate key {key!r}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise ValidationError(f"JSON: non-finite number {value} is not allowed")


def parse_document(raw: str) -> dict:
    try:
        return json.loads(
            raw,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
    except json.JSONDecodeError as error:
        raise ValidationError(f"JSON: {error.msg} at line {error.lineno}") from error


def load_document(path: Path = DEFAULT_CORPUS) -> dict:
    path = path.resolve()
    require(path.is_relative_to(ROOT), "path", "must stay inside this workspace")
    return parse_document(path.read_text(encoding="utf-8"))


def validate_offer(offer: object, where: str, now: datetime) -> None:
    exact_keys(
        offer,
        {"offer_id", "service_id", "resource_id", "person_id", "start_at", "end_at"},
        where,
    )
    require(offer["offer_id"] in ("offer_A", "offer_B"), where, "use fictional offer IDs")
    for field, value in (
        ("service_id", "service_A"),
        ("resource_id", "resource_A"),
        ("person_id", "person_example"),
    ):
        require(offer[field] == value, where, f"{field} must use the fictional ID")
    start = timestamp(offer["start_at"], f"{where}.start_at")
    end = timestamp(offer["end_at"], f"{where}.end_at")
    require(now < start < end, where, "fixture offers must be future, positive intervals")


def fixture_action_from_annotations(case: dict, policy: dict) -> Action:
    """Check fixture consistency, never infer intent from Georgian/English text.

    Called after structural checks. All evidence and interpretation annotations
    are author-supplied synthetic premises, not model outputs or runtime proof.
    Unknown or completed writes take precedence over a new conversational turn.
    """
    state = case["state"]
    evidence = case["evidence"]
    annotation = evidence["utterance_annotation"]
    offer = state["current_offer"]
    status = state["write_status"]
    if status == "uncertain":
        return EXPECTED_ACTIONS["uncertain_write"]
    if status == "confirmed":
        return EXPECTED_ACTIONS["existing_booking"]
    if status == "failed_no_write":
        return EXPECTED_ACTIONS["known_safe_failure"]
    if state["caller_cancelled"] or annotation["intent"] == "cancel":
        return EXPECTED_ACTIONS["cancelled_before_submit"]
    if annotation["intent"] == "correct_time":
        return EXPECTED_ACTIONS["corrected_time"]
    if offer is None or annotation["intent"] == "request_booking":
        return EXPECTED_ACTIONS["ambiguous_time"]
    if (
        annotation["speaker"] != "caller"
        or annotation["form"] != "direct"
        or annotation["intent"] != "confirm"
    ):
        return EXPECTED_ACTIONS["quoted_yes"]
    if annotation["offer_id"] != offer["offer_id"]:
        return EXPECTED_ACTIONS["superseded_offer_consent"]
    availability = evidence["availability"]
    if availability is None or availability["offer_id"] != offer["offer_id"]:
        return EXPECTED_ACTIONS["missing_availability"]
    if availability["status"] != "available":
        return Action("no_write", "offer_an_alternative_after_availability_check")
    age = (
        timestamp(state["now"], "now")
        - timestamp(availability["observed_at"], "observed_at")
    ).total_seconds()
    if not 0 <= age <= policy["availability_max_age_seconds"]:
        return EXPECTED_ACTIONS["stale_availability"]
    if not all(state["write_guards"].values()):
        return Action("handoff", "handoff_unavailable_write_guards")
    return EXPECTED_ACTIONS["current_offer_confirmed"]


def validate_case(case: object, index: int, policy: dict) -> None:
    where = f"cases[{index}]"
    exact_keys(
        case,
        {
            "case_id", "scenario", "synthetic", "timezone", "state",
            "utterance_ka", "translation_en", "evidence", "expected",
            "prohibited_actions", "rationale",
        },
        where,
    )
    require(case["case_id"] == f"BS-{index + 1:02d}", where, "unstable or duplicate case ID")
    require(case["scenario"] == SCENARIOS[index], where, "missing, duplicated or reordered coverage")
    require(case["synthetic"] is True, where, "synthetic label must be true")
    require(case["timezone"] == TIMEZONE, where, "timezone must be Asia/Tbilisi")
    for field in ("utterance_ka", "translation_en", "rationale"):
        text(case[field], f"{where}.{field}")
    # Script presence only: this is NOT a fluency, translation or NLU evaluator.
    require(
        any("\u10d0" <= char <= "\u10ff" for char in case["utterance_ka"]),
        where,
        "utterance_ka must contain Georgian script (presence check only)",
    )

    state = case["state"]
    exact_keys(
        state,
        {
            "now", "current_offer", "prior_offers", "caller_cancelled",
            "idempotency_key", "write_status", "create_attempts", "write_guards",
        },
        f"{where}.state",
    )
    now = timestamp(state["now"], f"{where}.state.now")
    require(type(state["caller_cancelled"]) is bool, where, "caller_cancelled must be boolean")
    require(
        state["idempotency_key"] == f"idempotency_example_{index + 1:02d}",
        where,
        "idempotency_key must be the stable fictional operation key",
    )
    statuses = {"not_started", "confirmed", "uncertain", "failed_no_write"}
    require(
        isinstance(state["write_status"], str) and state["write_status"] in statuses,
        where,
        "unknown write_status",
    )
    require(type(state["create_attempts"]) is int, where, "create_attempts must be integer")
    require(
        state["create_attempts"] == (0 if state["write_status"] == "not_started" else 1),
        where,
        "attempt history must match write_status",
    )
    guards = state["write_guards"]
    exact_keys(guards, {"conditional_slot_write", "durable_idempotency"}, f"{where}.write_guards")
    require(all(type(v) is bool for v in guards.values()), where, "guards must be booleans")
    require(type(state["prior_offers"]) is list, where, "prior_offers must be an array")
    offers = {}
    for offer in state["prior_offers"] + (
        [] if state["current_offer"] is None else [state["current_offer"]]
    ):
        validate_offer(offer, f"{where}.offer", now)
        require(offer["offer_id"] not in offers, where, "offer IDs must be immutable and unique")
        offers[offer["offer_id"]] = offer
    if case["scenario"] != "ambiguous_time":
        require(state["current_offer"] is not None, where, "this scenario requires a current offer")

    evidence = case["evidence"]
    exact_keys(
        evidence,
        {"initial_request", "utterance_annotation", "availability", "destination_result"},
        f"{where}.evidence",
    )
    initial = evidence["initial_request"]
    if initial is not None:
        exact_keys(initial, {"utterance_ka", "translation_en", "received_at"}, f"{where}.initial_request")
        for field in ("utterance_ka", "translation_en"):
            text(initial[field], f"{where}.initial_request.{field}")
        require(timestamp(initial["received_at"], where) <= now, where, "request is in the future")
    require(
        (initial is not None) == (case["scenario"] == "current_offer_confirmed"),
        where,
        "the valid-request fixture must include its initial synthetic request",
    )

    annotation = evidence["utterance_annotation"]
    exact_keys(
        annotation,
        {"speaker", "intent", "form", "offer_id", "requested_start_at"},
        f"{where}.utterance_annotation",
    )
    require(annotation["speaker"] in ("caller", "background"), where, "unknown speaker label")
    require(
        annotation["intent"] in (
            "confirm", "request_booking", "correct_time", "quote", "cancel", "status", "handoff"
        ),
        where,
        "unknown intent annotation",
    )
    require(annotation["form"] in ("direct", "quoted", "hypothetical", "none"), where, "unknown form")
    require(
        annotation["offer_id"] is None or (
            isinstance(annotation["offer_id"], str) and annotation["offer_id"] in offers
        ),
        where,
        "utterance references an unknown offer",
    )
    if annotation["intent"] == "correct_time":
        corrected = timestamp(annotation["requested_start_at"], f"{where}.requested_start_at")
        require(state["current_offer"] is not None, where, "correction requires an earlier offer")
        require(
            corrected > now
            and corrected != timestamp(state["current_offer"]["start_at"], where),
            where,
            "correction must request a different future time",
        )
    else:
        require(annotation["requested_start_at"] is None, where, "unexpected time correction")

    availability = evidence["availability"]
    if availability is not None:
        exact_keys(
            availability, {"source", "offer_id", "observed_at", "status"},
            f"{where}.availability",
        )
        require(availability["source"] == "synthetic_destination", where, "availability must be synthetic")
        require(
            isinstance(availability["offer_id"], str) and availability["offer_id"] in offers,
            where,
            "availability references an unknown offer",
        )
        require(availability["status"] in ("available", "unavailable"), where, "unknown slot status")
        require(timestamp(availability["observed_at"], where) <= now, where, "future availability evidence")

    result = evidence["destination_result"]
    if state["write_status"] == "not_started":
        require(result is None, where, "unstarted writes must not have destination results")
    else:
        exact_keys(
            result,
            {
                "source", "status", "observed_at", "idempotency_key",
                "offer_id", "booking_id", "reason_code",
            },
            f"{where}.destination_result",
        )
        require(result["source"] == "synthetic_destination", where, "result must be synthetic")
        require(timestamp(result["observed_at"], where) <= now, where, "future destination result")
        require(result["idempotency_key"] == state["idempotency_key"], where, "result key mismatch")
        require(
            state["current_offer"] is not None
            and result["offer_id"] == state["current_offer"]["offer_id"],
            where,
            "result must match the exact immutable current offer",
        )
        result_contract = {
            "confirmed": ("confirmed", "idempotency_match", "booking_example_10"),
            "uncertain": ("unknown", "response_lost_after_submission", None),
            "failed_no_write": ("rejected_no_write", "policy_rejection_before_write", None),
        }
        expected_status, reason, booking_id = result_contract[state["write_status"]]
        require(
            (result["status"], result["reason_code"], result["booking_id"])
            == (expected_status, reason, booking_id),
            where,
            "destination evidence does not establish the declared write outcome",
        )

    # Coverage is checked against evidence, not just the scenario's title.
    scenario = case["scenario"]
    if scenario == "ambiguous_time":
        require(state["current_offer"] is None, where, "ambiguous time must not be pre-resolved")
        require(annotation["intent"] == "request_booking", where, "missing ambiguous request")
    if scenario == "superseded_offer_consent":
        require(
            annotation["offer_id"] in {offer["offer_id"] for offer in state["prior_offers"]},
            where,
            "consent must refer to a documented prior offer",
        )
    if scenario == "quoted_yes":
        require(annotation["form"] in ("quoted", "hypothetical"), where, "missing non-direct affirmation")
    if scenario == "background_yes":
        require(annotation["speaker"] == "background", where, "missing background speaker")
    if scenario == "cancelled_before_submit":
        require(
            state["caller_cancelled"] and state["write_status"] == "not_started"
            and annotation["intent"] == "cancel",
            where,
            "cancellation must occur before submission",
        )

    expected = case["expected"]
    exact_keys(expected, set(asdict(Action("", ""))), f"{where}.expected")
    require(type(expected["max_create_calls"]) is int, where, "create budget must be integer, not boolean")
    require(type(expected["may_claim_booking_confirmed"]) is bool, where, "completion flag must be boolean")
    require(expected == asdict(EXPECTED_ACTIONS[scenario]), where, "incorrect scenario expectation")
    derived = fixture_action_from_annotations(case, policy)
    require(expected == asdict(derived), where, "expectation is unsafe or inconsistent with the evidence")
    prohibited = case["prohibited_actions"]
    require(type(prohibited) is list and all(isinstance(p, str) and p for p in prohibited), where, "invalid prohibitions")
    require(len(set(prohibited)) == len(prohibited), where, "duplicate prohibited action")
    required = COMMON_PROHIBITIONS | (
        {"repeat_create"} if derived.mode == "create_once" else {"create_booking"}
    )
    if scenario == "uncertain_write":
        required |= {"treat_timeout_as_definite_failure", "retry_with_new_idempotency_key"}
    require(required.issubset(prohibited), where, "missing a required safety prohibition")
    if derived.mode == "create_once":
        require("create_booking" not in prohibited, where, "contradictory create permission")
    require(derived.permitted_next_action not in prohibited, where, "permitted action is also prohibited")


def validate_document(document: object) -> dict:
    exact_keys(
        document,
        {
            "schema_version", "title", "synthetic", "prepared_for", "timezone",
            "publication_status", "source_urls", "attribution", "disclaimer", "policy", "cases",
        },
        "corpus",
    )
    require(document["schema_version"] == "1.1", "corpus", "unsupported schema version")
    text(document["title"], "corpus.title")
    require(document["synthetic"] is True, "corpus", "synthetic label must be true")
    require(document["prepared_for"] == "OMO / OMO AI", "corpus", "missing preparation disclosure")
    require(document["timezone"] == TIMEZONE, "corpus", "timezone must be Asia/Tbilisi")
    require(document["publication_status"] == "educational_resource", "corpus", "must remain an educational resource")
    require(document["source_urls"] == list(SOURCE_URLS), "corpus", "only supplied source URLs are allowed")
    text(document["attribution"], "corpus.attribution")
    require(
        "OMO AI" in document["attribution"] and "CC BY 4.0" in document["attribution"]
        and "Changes:" in document["attribution"],
        "corpus",
        "preserve source author, source license and a change notice",
    )
    require(document["disclaimer"] == DISCLAIMER, "corpus", "missing synthetic/no-runtime disclaimer")
    policy = document["policy"]
    exact_keys(policy, {"availability_max_age_seconds", "description"}, "policy")
    require(
        type(policy["availability_max_age_seconds"]) is int
        and policy["availability_max_age_seconds"] == 120,
        "policy",
        "this corpus uses a fixed illustrative 120-second freshness window",
    )
    text(policy["description"], "policy.description")
    require(
        "synthetic" in policy["description"].lower()
        and "not an OMO" in policy["description"],
        "policy",
        "the illustrative policy must not be presented as an OMO rule",
    )
    require(type(document["cases"]) is list and len(document["cases"]) == 12, "cases", "exactly 12 cases required")
    for index, case in enumerate(document["cases"]):
        validate_case(case, index, policy)
    modes = Counter(case["expected"]["mode"] for case in document["cases"])
    require(set(modes) == {"no_write", "create_once", "reconcile", "handoff"}, "cases", "missing action mode")
    return {
        "status": "passed",
        "cases_checked": len(document["cases"]),
        "mode_counts": dict(sorted(modes.items())),
        "scope": "local synthetic structure and annotated safety expectations only",
        "runtime_validated": False,
        "disclaimer": DISCLAIMER,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(DEFAULT_CORPUS))
    arguments = parser.parse_args(argv)
    candidate = Path(arguments.path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        report = validate_document(load_document(candidate))
    except (ValidationError, OSError, UnicodeError) as error:
        print(json.dumps({"status": "failed", "error": str(error), "runtime_validated": False}))
        return 1
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
