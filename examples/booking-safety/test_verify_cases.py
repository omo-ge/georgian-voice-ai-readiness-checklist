"""Local mutation/regression tests of synthetic fixtures, not of OMO or an LLM."""

from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import asdict
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import verify_cases as verifier


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = verifier.load_document()

    def setUp(self):
        self.document = deepcopy(self.original)

    def case(self, case_number):
        return self.document["cases"][case_number - 1]

    def assert_invalid(self):
        with self.assertRaises(verifier.ValidationError):
            verifier.validate_document(self.document)

    def test_original_corpus_passes(self):
        report = verifier.validate_document(self.document)
        self.assertEqual(report["cases_checked"], 12)
        self.assertEqual(
            report["mode_counts"],
            {"create_once": 1, "handoff": 1, "no_write": 9, "reconcile": 1},
        )
        self.assertIs(report["runtime_validated"], False)

    def test_every_required_scenario_has_the_declared_action(self):
        for case in self.document["cases"]:
            with self.subTest(case=case["case_id"]):
                action = verifier.fixture_action_from_annotations(case, self.document["policy"])
                self.assertEqual(case["expected"], asdict(action))

    def test_removed_case_is_rejected(self):
        self.document["cases"].pop()
        self.assert_invalid()

    def test_extra_case_is_rejected(self):
        self.document["cases"].append(deepcopy(self.case(1)))
        self.assert_invalid()

    def test_duplicate_id_is_rejected(self):
        self.case(2)["case_id"] = self.case(1)["case_id"]
        self.assert_invalid()

    def test_duplicate_scenario_is_rejected(self):
        self.case(2)["scenario"] = self.case(1)["scenario"]
        self.assert_invalid()

    def test_unknown_fields_are_rejected(self):
        self.case(1)["unexpected_field"] = "not part of the contract"
        self.assert_invalid()

    def test_wrong_container_type_is_rejected(self):
        self.case(1)["state"] = []
        self.assert_invalid()

    def test_synthetic_label_is_required_at_both_levels(self):
        for target in ("corpus", "case"):
            with self.subTest(target=target):
                self.document = deepcopy(self.original)
                record = self.document if target == "corpus" else self.case(1)
                record["synthetic"] = False
                self.assert_invalid()

    def test_timezone_is_required_on_each_case(self):
        self.case(1)["timezone"] = "UTC"
        self.assert_invalid()

    def test_naive_timestamp_is_rejected(self):
        self.case(1)["state"]["now"] = "2030-05-14T10:00:00"
        self.assert_invalid()

    def test_wrong_offset_is_rejected(self):
        self.case(1)["state"]["now"] = "2030-05-14T10:00:00+03:00"
        self.assert_invalid()

    def test_invalid_calendar_date_is_rejected(self):
        self.case(1)["state"]["now"] = "2030-02-30T10:00:00+04:00"
        self.assert_invalid()

    def test_reversed_slot_is_rejected(self):
        self.case(1)["state"]["current_offer"]["end_at"] = "2030-05-15T14:30:00+04:00"
        self.assert_invalid()

    def test_past_offer_is_rejected(self):
        self.case(1)["state"]["current_offer"]["start_at"] = "2030-05-13T15:00:00+04:00"
        self.assert_invalid()

    def test_nonfictional_person_id_is_rejected(self):
        self.case(1)["state"]["current_offer"]["person_id"] = "not_an_allowed_fixture_id"
        self.assert_invalid()

    def test_empty_translation_is_rejected(self):
        self.case(1)["translation_en"] = " "
        self.assert_invalid()

    def test_georgian_script_presence_not_language_quality(self):
        self.case(1)["utterance_ka"] = "This field has no Georgian script."
        self.assert_invalid()

    def test_text_is_not_used_as_a_consent_evaluator(self):
        # Deliberately nonsensical text still passes when the annotation is intact.
        # This proves the LIMITATION, not Georgian understanding or safety of NLU.
        self.case(1)["utterance_ka"] = "სინთეზური"
        self.case(1)["translation_en"] = "Deliberately unrelated synthetic test text."
        self.assertEqual(verifier.validate_document(self.document)["status"], "passed")

    def test_current_request_evidence_is_required(self):
        self.case(1)["evidence"]["initial_request"] = None
        self.assert_invalid()

    def test_unknown_offer_reference_is_rejected(self):
        self.case(1)["evidence"]["utterance_annotation"]["offer_id"] = "offer_unknown"
        self.assert_invalid()

    def test_reusing_an_offer_id_for_changed_details_is_rejected(self):
        self.case(6)["state"]["prior_offers"][0]["offer_id"] = "offer_B"
        self.assert_invalid()

    def test_create_without_availability_is_rejected(self):
        self.case(1)["evidence"]["availability"] = None
        self.assert_invalid()

    def test_stale_availability_cannot_authorize_create(self):
        self.case(1)["evidence"]["availability"]["observed_at"] = "2030-05-14T09:57:59+04:00"
        self.assert_invalid()

    def test_freshness_at_exact_boundary_is_accepted(self):
        self.case(1)["evidence"]["availability"]["observed_at"] = "2030-05-14T09:58:00+04:00"
        self.assertEqual(verifier.validate_document(self.document)["status"], "passed")

    def test_freshness_one_second_over_boundary_is_rejected(self):
        self.case(1)["evidence"]["availability"]["observed_at"] = "2030-05-14T09:57:59+04:00"
        self.assert_invalid()

    def test_future_availability_is_rejected(self):
        self.case(1)["evidence"]["availability"]["observed_at"] = "2030-05-14T10:00:01+04:00"
        self.assert_invalid()

    def test_unavailable_slot_cannot_authorize_create(self):
        self.case(1)["evidence"]["availability"]["status"] = "unavailable"
        self.assert_invalid()

    def test_availability_for_another_offer_cannot_authorize_create(self):
        other_offer = deepcopy(self.case(1)["state"]["current_offer"])
        other_offer["offer_id"] = "offer_B"
        other_offer["start_at"] = "2030-05-15T16:00:00+04:00"
        other_offer["end_at"] = "2030-05-15T16:30:00+04:00"
        self.case(1)["state"]["prior_offers"] = [other_offer]
        self.case(1)["evidence"]["availability"]["offer_id"] = "offer_B"
        self.assert_invalid()

    def test_nondestination_availability_is_rejected(self):
        self.case(1)["evidence"]["availability"]["source"] = "model_memory"
        self.assert_invalid()

    def test_missing_each_write_guard_blocks_create(self):
        for guard in ("conditional_slot_write", "durable_idempotency"):
            with self.subTest(guard=guard):
                self.document = deepcopy(self.original)
                self.case(1)["state"]["write_guards"][guard] = False
                self.assert_invalid()

    def test_string_write_guard_is_rejected(self):
        self.case(1)["state"]["write_guards"]["durable_idempotency"] = "true"
        self.assert_invalid()

    def test_correction_cannot_preserve_create_permission(self):
        annotation = self.case(1)["evidence"]["utterance_annotation"]
        annotation["intent"] = "correct_time"
        annotation["requested_start_at"] = "2030-05-15T16:00:00+04:00"
        self.assert_invalid()

    def test_ambiguous_time_cannot_be_silently_resolved(self):
        self.case(2)["state"]["current_offer"] = deepcopy(self.case(1)["state"]["current_offer"])
        self.assert_invalid()

    def test_previous_offer_consent_cannot_be_relabelled_current(self):
        self.case(6)["evidence"]["utterance_annotation"]["offer_id"] = "offer_B"
        self.assert_invalid()

    def test_quoted_and_hypothetical_affirmations_do_not_authorize_create(self):
        for form in ("quoted", "hypothetical"):
            with self.subTest(form=form):
                self.document = deepcopy(self.original)
                self.case(1)["evidence"]["utterance_annotation"]["form"] = form
                self.assert_invalid()

    def test_hypothetical_form_is_supported_by_the_nonconsent_fixture(self):
        self.case(7)["evidence"]["utterance_annotation"]["form"] = "hypothetical"
        self.assertEqual(verifier.validate_document(self.document)["status"], "passed")

    def test_background_affirmation_cannot_authorize_create(self):
        self.case(1)["evidence"]["utterance_annotation"]["speaker"] = "background"
        self.assert_invalid()

    def test_cancellation_cannot_authorize_create(self):
        self.case(1)["state"]["caller_cancelled"] = True
        self.assert_invalid()

    def test_cancellation_intent_alone_blocks_create(self):
        self.case(1)["evidence"]["utterance_annotation"]["intent"] = "cancel"
        self.assert_invalid()

    def test_existing_booking_cannot_be_created_again(self):
        self.case(10)["expected"] = asdict(verifier.EXPECTED_ACTIONS["current_offer_confirmed"])
        self.assert_invalid()

    def test_existing_result_requires_matching_operation_key(self):
        self.case(10)["evidence"]["destination_result"]["idempotency_key"] = "different_operation"
        self.assert_invalid()

    def test_existing_result_requires_matching_offer(self):
        self.case(10)["evidence"]["destination_result"]["offer_id"] = "offer_B"
        self.assert_invalid()

    def test_existing_result_requires_booking_identifier(self):
        self.case(10)["evidence"]["destination_result"]["booking_id"] = None
        self.assert_invalid()

    def test_uncertain_result_cannot_claim_completion(self):
        self.case(11)["expected"]["may_claim_booking_confirmed"] = True
        self.assert_invalid()

    def test_uncertain_result_cannot_authorize_retry(self):
        self.case(11)["expected"]["max_create_calls"] = 1
        self.assert_invalid()

    def test_uncertain_result_cannot_be_treated_as_definite_failure(self):
        self.case(11)["evidence"]["destination_result"]["status"] = "rejected_no_write"
        self.assert_invalid()

    def test_uncertainty_requires_reconciliation_even_after_cancellation(self):
        self.case(11)["state"]["caller_cancelled"] = True
        annotation = self.case(11)["evidence"]["utterance_annotation"]
        annotation["intent"] = "cancel"
        action = verifier.fixture_action_from_annotations(self.case(11), self.document["policy"])
        self.assertEqual(action.mode, "reconcile")
        self.assertEqual(verifier.validate_document(self.document)["status"], "passed")

    def test_known_failure_requires_definitive_no_write_evidence(self):
        self.case(12)["evidence"]["destination_result"]["reason_code"] = "timeout"
        self.assert_invalid()

    def test_unstarted_write_cannot_have_a_result(self):
        self.case(1)["evidence"]["destination_result"] = deepcopy(
            self.case(10)["evidence"]["destination_result"]
        )
        self.assert_invalid()

    def test_attempt_history_must_match_write_state(self):
        self.case(11)["state"]["create_attempts"] = 0
        self.assert_invalid()

    def test_create_permission_is_not_completion(self):
        self.case(1)["expected"]["may_claim_booking_confirmed"] = True
        self.assert_invalid()

    def test_boolean_cannot_masquerade_as_create_budget(self):
        self.case(1)["expected"]["max_create_calls"] = True
        self.assert_invalid()

    def test_missing_prohibition_is_rejected(self):
        self.case(11)["prohibited_actions"].remove("retry_with_new_idempotency_key")
        self.assert_invalid()

    def test_contradictory_permission_is_rejected(self):
        self.case(1)["prohibited_actions"].append("create_booking")
        self.assert_invalid()

    def test_policy_window_is_an_explicit_fixture_constant(self):
        self.document["policy"]["availability_max_age_seconds"] = 86400
        self.assert_invalid()

    def test_no_runtime_warning_cannot_be_removed(self):
        self.document["disclaimer"] = "A product benchmark."
        self.assert_invalid()

    def test_attribution_requires_a_change_notice(self):
        self.document["attribution"] = "OMO AI, CC BY 4.0."
        self.assert_invalid()

    def test_only_supplied_source_urls_are_allowed(self):
        self.document["source_urls"].append("https://example.invalid/unapproved")
        self.assert_invalid()

    def test_generic_publication_label_is_rejected(self):
        self.document["publication_status"] = "published"
        self.assert_invalid()


    def test_educational_release_does_not_claim_runtime_validation(self):
        self.assertEqual(self.document["schema_version"], "1.1")
        self.assertEqual(self.document["publication_status"], "educational_resource")
        report = verifier.validate_document(self.document)
        self.assertIs(report["runtime_validated"], False)
        self.assertIn("No runtime validation has occurred.", report["disclaimer"])

    def test_metadata_cannot_claim_a_runtime_evaluation(self):
        self.document["publication_status"] = "runtime_validated"
        self.assert_invalid()


class ParserAndCliTests(unittest.TestCase):
    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(verifier.ValidationError, "duplicate key"):
            verifier.parse_document('{"synthetic": true, "synthetic": false}')

    def test_nested_duplicate_keys_are_rejected(self):
        with self.assertRaisesRegex(verifier.ValidationError, "duplicate key"):
            verifier.parse_document('{"state": {"status": "a", "status": "b"}}')

    def test_nonfinite_json_numbers_are_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                with self.assertRaises(verifier.ValidationError):
                    verifier.parse_document('{"value": ' + value + "}")

    def test_invalid_json_is_rejected(self):
        with self.assertRaisesRegex(verifier.ValidationError, "JSON"):
            verifier.parse_document("{")

    def test_path_outside_workspace_is_rejected_before_read(self):
        outside = verifier.ROOT.parent / "do_not_read_fixture.json"
        with patch.object(Path, "read_text") as reader:
            with self.assertRaisesRegex(verifier.ValidationError, "inside this workspace"):
                verifier.load_document(outside)
            reader.assert_not_called()

    def test_cli_success_is_local_and_explicit(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = verifier.main([])
        report = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(report["cases_checked"], 12)
        self.assertIs(report["runtime_validated"], False)

    def test_cli_returns_nonzero_for_validation_failure(self):
        output = io.StringIO()
        with patch.object(verifier, "load_document", return_value={}):
            with redirect_stdout(output):
                code = verifier.main([])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["status"], "failed")

    def test_cli_returns_nonzero_for_missing_file(self):
        output = io.StringIO()
        with patch.object(verifier, "load_document", side_effect=FileNotFoundError("synthetic missing file")):
            with redirect_stdout(output):
                code = verifier.main([])
        self.assertEqual(code, 1)
        self.assertIs(json.loads(output.getvalue())["runtime_validated"], False)


if __name__ == "__main__":
    unittest.main()
