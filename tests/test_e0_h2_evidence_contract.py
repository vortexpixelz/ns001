from __future__ import annotations

import builtins
import contextlib
import copy
import getpass
import hashlib
import importlib
import io
import netrc
import os
import pathlib
import socket
import subprocess
import sys
import types
import unittest
import urllib.request
from dataclasses import FrozenInstanceError, fields, replace
from unittest import mock

import e0.h2.evidence_contract as evidence_module
from e0.h2.evidence_contract import (
    AUTHORITATIVE_PRIMARY,
    CONTRACT_PHASE,
    DECLARED_EVIDENCE_CATEGORIES,
    EVIDENCE_DECLARATION_SCHEMA,
    EXPECTED_ANCHOR_DECLARATIONS,
    EvidenceContractRefusal,
    EvidenceIdentityDeclaration,
    EvidenceRecordDeclaration,
    SuppliedBytesIdentityCheck,
    ValidatedEvidenceContract,
    FROZEN_PREREGISTRATION_SHA256,
    GATE_DECLARATION_SUBMISSION_SCHEMA,
    GATE_REQUIREMENTS,
    GateDeclarationSubmissionCoverage,
    H1_AUDIT_BUNDLE_SHA256,
    H1_CHECKPOINT_COMMIT,
    LATER_H2_VERIFIER_BY_CATEGORY,
    REPORTED_NOT_REPRODUCED,
    RETAINED_ACQUISITION_PROVENANCE,
    SCIENTIFIC_BASE_COMMIT,
    SYNTHETIC_TEST,
    TERMINAL_STATUS,
    UNRESOLVED_ASSERTION,
    build_evidence_contract,
    canonical_json_bytes,
    canonical_sha256,
    check_supplied_bytes_against_identity_declaration,
    evidence_contract_sha256,
    parse_json_bytes,
    validate_evidence_contract,
    validate_evidence_record_declaration,
    validate_gate_declaration_submission,
)


class IntSubclass(int):
    pass


class DictSubclass(dict):
    pass


class H2A0EvidenceDeclarationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        forbidden = AssertionError("network or credential access forbidden in H2A0 tests")
        self.blockers = [
            mock.patch("socket.socket", side_effect=forbidden),
            mock.patch("socket.create_connection", side_effect=forbidden),
            mock.patch("socket.getaddrinfo", side_effect=forbidden),
            mock.patch("socket.gethostbyname", side_effect=forbidden),
            mock.patch("socket.gethostbyname_ex", side_effect=forbidden),
            mock.patch("socket.gethostbyaddr", side_effect=forbidden),
            mock.patch("socket.getnameinfo", side_effect=forbidden),
            mock.patch("urllib.request.urlopen", side_effect=forbidden),
            mock.patch("getpass.getpass", side_effect=forbidden),
            mock.patch("netrc.netrc", side_effect=forbidden),
        ]
        for blocker in self.blockers:
            blocker.start()
        self.contract = build_evidence_contract()

    def tearDown(self) -> None:
        for blocker in reversed(self.blockers):
            blocker.stop()

    def record_for(
        self,
        requirement,
        index: int = 0,
        *,
        content: bytes | None = None,
    ):
        supplied = (
            content
            if content is not None
            else f"fixture-declaration:{requirement.requirement_id}:{index}".encode(
                "utf-8"
            )
        )
        digest = hashlib.sha256(supplied).hexdigest()
        return {
            "schema": EVIDENCE_DECLARATION_SCHEMA,
            "evidence_id": f"declaration-{requirement.requirement_id}-{index}",
            "requirement_id": requirement.requirement_id,
            "declared_category": requirement.declared_category,
            "declared_subject": (
                "unauthenticated H2A0 fixture declaration for "
                f"{requirement.requirement_id}"
            ),
            "identity_declaration": {
                "algorithm": "sha256",
                "artifact_name": f"fixture-{requirement.requirement_id}-{index}.json",
                "declared_expected_sha256": digest,
                "declared_observed_sha256": digest,
                "declared_byte_count": len(supplied),
            },
            "provenance_declarations": {
                "origin": "fixture origin declaration; not authenticated",
                "authority": "fixture authority declaration; not authenticated",
                "custody": "fixture custody declaration; not authenticated",
                "verifier": "future later-H2 verifier declaration",
            },
            "declared_resolution": "resolved",
            "rule_result_declarations": [
                {"rule_id": rule, "declared_passed": True}
                for rule in requirement.required_rule_declarations
            ],
        }

    def submission_for(self, gate):
        return {
            "schema": GATE_DECLARATION_SUBMISSION_SCHEMA,
            "gate_id": gate.gate_id,
            "contract_sha256": evidence_contract_sha256(self.contract),
            "evidence_declarations": [
                self.record_for(item, index)
                for index, item in enumerate(gate.evidence_declarations)
            ],
        }

    def assert_refuses(self, callback, pattern: str | None = None):
        context = (
            self.assertRaisesRegex(EvidenceContractRefusal, pattern)
            if pattern
            else self.assertRaises(EvidenceContractRefusal)
        )
        with context:
            callback()

    def test_contract_contains_exact_expected_anchor_declarations(self) -> None:
        self.assertEqual(
            dict(EXPECTED_ANCHOR_DECLARATIONS),
            {
                "h1_checkpoint_commit": H1_CHECKPOINT_COMMIT,
                "scientific_base_commit": SCIENTIFIC_BASE_COMMIT,
                "frozen_preregistration_sha256": FROZEN_PREREGISTRATION_SHA256,
                "h1_audit_bundle_sha256": H1_AUDIT_BUNDLE_SHA256,
            },
        )
        self.assertEqual(
            self.contract["expected_anchor_declarations"],
            dict(EXPECTED_ANCHOR_DECLARATIONS),
        )
        validated = validate_evidence_contract(self.contract)
        self.assertEqual(
            dict(validated.expected_anchor_declarations),
            dict(EXPECTED_ANCHOR_DECLARATIONS),
        )
        self.assertFalse(hasattr(validated, "anchors_verified"))
        self.assertEqual(validated.overall_status, TERMINAL_STATUS)

    def test_contract_validation_performs_no_live_anchor_verification(self) -> None:
        forbidden = AssertionError("external anchor verification belongs to later H2")
        with (
            mock.patch.object(subprocess, "run", side_effect=forbidden),
            mock.patch.object(subprocess, "check_output", side_effect=forbidden),
            mock.patch.object(pathlib.Path, "read_bytes", side_effect=forbidden),
        ):
            validated = validate_evidence_contract(self.contract)
            self.assertEqual(validated.overall_status, "HOLD")

    def test_expected_anchor_declaration_mismatch_refuses(self) -> None:
        for anchor in EXPECTED_ANCHOR_DECLARATIONS:
            with self.subTest(anchor=anchor):
                malformed = copy.deepcopy(self.contract)
                malformed["expected_anchor_declarations"][anchor] = "0" * 64
                self.assert_refuses(
                    lambda malformed=malformed: validate_evidence_contract(malformed),
                    "expected anchor declaration mismatch",
                )

    def test_contract_rejects_missing_extra_unknown_and_wrong_types(self) -> None:
        missing = copy.deepcopy(self.contract)
        del missing["overall_status"]
        extra = copy.deepcopy(self.contract)
        extra["ready"] = False
        unknown_gate = copy.deepcopy(self.contract)
        unknown_gate["gates"][0]["gate_id"] = "unknown"
        wrong_type = copy.deepcopy(self.contract)
        wrong_type["gates"] = True
        root_subclass = DictSubclass(self.contract)
        for malformed in (missing, extra, unknown_gate, wrong_type, root_subclass):
            with self.subTest(malformed=malformed):
                self.assert_refuses(
                    lambda malformed=malformed: validate_evidence_contract(malformed)
                )

    def test_contract_rejects_duplicate_gate_requirement_and_rule_declarations(self) -> None:
        duplicate_gate = copy.deepcopy(self.contract)
        duplicate_gate["gates"][1] = copy.deepcopy(duplicate_gate["gates"][0])
        duplicate_requirement = copy.deepcopy(self.contract)
        declarations = duplicate_requirement["gates"][0][
            "required_evidence_declarations"
        ]
        declarations[1]["requirement_id"] = declarations[0]["requirement_id"]
        duplicate_rule = copy.deepcopy(self.contract)
        rules = duplicate_rule["gates"][0]["required_evidence_declarations"][0][
            "required_rule_declarations"
        ]
        rules[1] = rules[0]
        for malformed in (duplicate_gate, duplicate_requirement, duplicate_rule):
            with self.subTest(malformed=malformed):
                self.assert_refuses(
                    lambda malformed=malformed: validate_evidence_contract(malformed)
                )

    def test_canonical_representation_is_deterministic_and_non_self_referential(self) -> None:
        first = {"z": [3, 2, 1], "a": {"b": True, "a": None}}
        second = {"a": {"a": None, "b": True}, "z": [3, 2, 1]}
        self.assertEqual(canonical_json_bytes(first), canonical_json_bytes(second))
        self.assertEqual(canonical_sha256(first), canonical_sha256(second))
        self.assertEqual(
            canonical_json_bytes(first), b'{"a":{"a":null,"b":true},"z":[3,2,1]}'
        )
        self.assertNotIn("contract_sha256", self.contract)

    def test_canonical_representation_rejects_non_exact_types(self) -> None:
        for value in (
            {"n": 1.0},
            {"n": IntSubclass(1)},
            {1: "non-string key"},
            (1, 2),
        ):
            with self.subTest(value=value):
                self.assert_refuses(lambda value=value: canonical_json_bytes(value))

    def test_json_parser_rejects_duplicates_malformed_and_nonfinite_values(self) -> None:
        for value in (
            b'{"a":1,"a":2}',
            b'{"a":',
            b'\xff',
            b'{"a":NaN}',
        ):
            with self.subTest(value=value):
                self.assert_refuses(lambda value=value: parse_json_bytes(value))
        self.assert_refuses(lambda: parse_json_bytes('{"a":1}'))

    def test_json_parser_round_trip_preserves_contract_identity(self) -> None:
        encoded = canonical_json_bytes(self.contract)
        parsed = parse_json_bytes(encoded)
        validated = validate_evidence_contract(parsed)
        self.assertEqual(validated.to_json_value(), self.contract)
        self.assertEqual(canonical_json_bytes(validated.to_json_value()), encoded)

    def test_all_declared_categories_have_explicit_later_h2_verifiers(self) -> None:
        self.assertEqual(
            DECLARED_EVIDENCE_CATEGORIES,
            {
                AUTHORITATIVE_PRIMARY,
                RETAINED_ACQUISITION_PROVENANCE,
                SYNTHETIC_TEST,
                REPORTED_NOT_REPRODUCED,
                UNRESOLVED_ASSERTION,
            },
        )
        self.assertEqual(
            set(LATER_H2_VERIFIER_BY_CATEGORY), DECLARED_EVIDENCE_CATEGORIES
        )
        for gate in GATE_REQUIREMENTS:
            for requirement in gate.evidence_declarations:
                self.assertEqual(
                    requirement.later_h2_verifier,
                    LATER_H2_VERIFIER_BY_CATEGORY[requirement.declared_category],
                )

    def test_draft_uses_exact_category_verifier_identifiers(self) -> None:
        draft_path = pathlib.Path(evidence_module.__file__).parents[2] / (
            "docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md"
        )
        draft = draft_path.read_text(encoding="utf-8")
        for identifier in LATER_H2_VERIFIER_BY_CATEGORY.values():
            self.assertIn(f"`{identifier}`", draft)
            self.assertNotIn(f"`{identifier.removeprefix('later_h2.')}`", draft)

    def test_evidence_record_returns_deeply_immutable_reconstruction(self) -> None:
        source = self.record_for(GATE_REQUIREMENTS[0].evidence_declarations[0])
        validated = validate_evidence_record_declaration(source)
        original_subject = validated.declared_subject
        original_digest = validated.identity_declaration.declared_observed_sha256
        original_rule = validated.rule_result_declarations[0].rule_id

        source["declared_subject"] = "mutated"
        source["identity_declaration"]["declared_observed_sha256"] = "0" * 64
        source["rule_result_declarations"][0]["rule_id"] = "mutated"

        self.assertEqual(validated.declared_subject, original_subject)
        self.assertEqual(
            validated.identity_declaration.declared_observed_sha256,
            original_digest,
        )
        self.assertEqual(validated.rule_result_declarations[0].rule_id, original_rule)
        with self.assertRaises(FrozenInstanceError):
            validated.declared_subject = "mutated"
        with self.assertRaises(FrozenInstanceError):
            validated.identity_declaration.artifact_name = "mutated"

    def test_contract_validation_returns_deeply_immutable_reconstruction(self) -> None:
        validated = validate_evidence_contract(self.contract)
        original_anchor = validated.expected_anchor_declarations[0]
        self.contract["expected_anchor_declarations"].clear()
        self.contract["gates"][0]["required_evidence_declarations"].clear()
        self.assertEqual(validated.expected_anchor_declarations[0], original_anchor)
        self.assertGreater(len(validated.gates[0].evidence_declarations), 0)
        with self.assertRaises(FrozenInstanceError):
            validated.gates[0].gate_id = "mutated"
        self.contract = build_evidence_contract()

    def test_evidence_declarations_do_not_treat_pass_or_resolution_as_proof(self) -> None:
        requirement = GATE_REQUIREMENTS[0].evidence_declarations[0]
        for declared_passed in (True, False):
            for resolution in (
                "resolved",
                "unresolved",
                "ambiguous",
                "contradictory",
            ):
                with self.subTest(
                    declared_passed=declared_passed, resolution=resolution
                ):
                    record = self.record_for(requirement)
                    record["rule_result_declarations"][0][
                        "declared_passed"
                    ] = declared_passed
                    record["declared_resolution"] = resolution
                    validated = validate_evidence_record_declaration(record)
                    self.assertEqual(validated.declared_resolution, resolution)
                    self.assertEqual(
                        validated.rule_result_declarations[0].declared_passed,
                        declared_passed,
                    )

    def test_evidence_record_rejects_schema_field_and_exact_type_errors(self) -> None:
        requirement = GATE_REQUIREMENTS[0].evidence_declarations[0]
        missing = self.record_for(requirement)
        del missing["declared_subject"]
        extra = self.record_for(requirement)
        extra["source_url"] = "https://example.invalid"
        unknown_category = self.record_for(requirement)
        unknown_category["declared_category"] = "conversation_summary"
        duplicate_rule = self.record_for(requirement)
        duplicate_rule["rule_result_declarations"][1]["rule_id"] = (
            duplicate_rule["rule_result_declarations"][0]["rule_id"]
        )
        for malformed in (missing, extra, unknown_category, duplicate_rule):
            with self.subTest(malformed=malformed):
                self.assert_refuses(
                    lambda malformed=malformed: validate_evidence_record_declaration(
                        malformed
                    )
                )

        for value in (True, 1.0, IntSubclass(1), "1", None):
            with self.subTest(byte_count=value):
                record = self.record_for(requirement)
                record["identity_declaration"]["declared_byte_count"] = value
                self.assert_refuses(
                    lambda record=record: validate_evidence_record_declaration(record)
                )
        for value in (1, 1.0, "true", None):
            with self.subTest(declared_passed=value):
                record = self.record_for(requirement)
                record["rule_result_declarations"][0]["declared_passed"] = value
                self.assert_refuses(
                    lambda record=record: validate_evidence_record_declaration(record)
                )

    def test_supplied_byte_identity_check_uses_real_bytes_hash_and_length(self) -> None:
        content = b"actual supplied fixture bytes"
        requirement = GATE_REQUIREMENTS[0].evidence_declarations[0]
        record = self.record_for(requirement, content=content)
        declaration = validate_evidence_record_declaration(record)
        checked = check_supplied_bytes_against_identity_declaration(
            declaration.identity_declaration, content
        )
        self.assertEqual(checked.sha256, hashlib.sha256(content).hexdigest())
        self.assertEqual(checked.byte_count, len(content))

        same_length_wrong_bytes = b"x" * len(content)
        self.assert_refuses(
            lambda: check_supplied_bytes_against_identity_declaration(
                declaration.identity_declaration, same_length_wrong_bytes
            ),
            "declared expected SHA-256",
        )
        self.assert_refuses(
            lambda: check_supplied_bytes_against_identity_declaration(
                declaration.identity_declaration, content + b"x"
            ),
            "declared byte count",
        )

        observed_mismatch = self.record_for(requirement, content=content)
        observed_mismatch["identity_declaration"]["declared_observed_sha256"] = (
            "0" * 64
        )
        mismatch_declaration = validate_evidence_record_declaration(observed_mismatch)
        self.assert_refuses(
            lambda: check_supplied_bytes_against_identity_declaration(
                mismatch_declaration.identity_declaration, content
            ),
            "declared observed SHA-256",
        )

    def test_every_gate_has_declaration_schema_coverage_only_and_remains_unresolved(self) -> None:
        for gate in GATE_REQUIREMENTS:
            with self.subTest(gate=gate.gate_id):
                coverage = validate_gate_declaration_submission(
                    self.contract, self.submission_for(gate)
                )
                self.assertTrue(coverage.declaration_schema_covered)
                self.assertFalse(coverage.evidence_verified)
                self.assertFalse(coverage.substantive_gate_resolved)
                self.assertEqual(coverage.overall_status, "HOLD")
                self.assertFalse(hasattr(coverage, "structure_complete"))
                self.assertFalse(hasattr(coverage, "gate_passed"))

    def test_success_result_constructors_are_factory_only(self) -> None:
        for cls, kwargs in (
            (GateDeclarationSubmissionCoverage, {
                "gate_id": "external_trust_root",
                "contract_sha256": "0" * 64,
                "evidence_ids": ("a", "b", "c"),
            }),
            (SuppliedBytesIdentityCheck, {
                "sha256": "0" * 64, "byte_count": 0,
            }),
            (ValidatedEvidenceContract, {
                "expected_anchor_declarations": [], "gates": [],
            }),
        ):
            with self.subTest(result=cls.__name__):
                with self.assertRaisesRegex(TypeError, "use "):
                    cls(**kwargs)
                with self.assertRaisesRegex(TypeError, "use "):
                    cls()

        coverage = validate_gate_declaration_submission(
            self.contract, self.submission_for(GATE_REQUIREMENTS[0])
        )
        self.assertEqual(coverage.overall_status, "HOLD")
        self.assertFalse(coverage.evidence_verified)
        self.assertFalse(coverage.substantive_gate_resolved)
        with self.assertRaises(TypeError):
            GateDeclarationSubmissionCoverage(overall_status="READY")
        with self.assertRaisesRegex(TypeError, "use "):
            replace(coverage, contract_sha256="0" * 64)
        with mock.patch.object(evidence_module, "TERMINAL_STATUS", "READY"):
            self.assertEqual(coverage.overall_status, "HOLD")

    def test_contract_phase_is_separate_from_execution_status(self) -> None:
        self.assertEqual(self.contract["contract_phase"], CONTRACT_PHASE)
        self.assertEqual(self.contract["overall_status"], "HOLD")
        self.assertNotIn("declaration_status", self.contract)
        validated = validate_evidence_contract(self.contract)
        self.assertEqual(validated.contract_phase, CONTRACT_PHASE)
        self.assertEqual(validated.overall_status, "HOLD")
        old_schema = copy.deepcopy(self.contract)
        old_schema["declaration_status"] = old_schema.pop("contract_phase")
        self.assert_refuses(
            lambda: validate_evidence_contract(old_schema), "fields mismatch"
        )

    def test_public_declaration_construction_copies_nested_lists(self) -> None:
        validated = validate_evidence_record_declaration(
            self.record_for(GATE_REQUIREMENTS[0].evidence_declarations[0])
        )
        rules = list(validated.rule_result_declarations)
        kwargs = {field.name: getattr(validated, field.name) for field in fields(validated)}
        kwargs["rule_result_declarations"] = rules
        constructed = EvidenceRecordDeclaration(**kwargs)
        rules.clear()
        self.assertEqual(constructed, validated)
        self.assertIsNot(constructed.identity_declaration, validated.identity_declaration)
        self.assertIsNot(constructed.provenance_declarations, validated.provenance_declarations)
        self.assertIs(type(constructed.rule_result_declarations), tuple)
        with self.assertRaises(FrozenInstanceError):
            constructed.identity_declaration.declared_byte_count = 99

        source_requirement = GATE_REQUIREMENTS[0].evidence_declarations[0]
        rule_names = list(source_requirement.required_rule_declarations)
        requirement = evidence_module.EvidenceRequirement(
            source_requirement.requirement_id, source_requirement.declared_category,
            source_requirement.later_h2_verifier, rule_names,
        )
        declarations = [requirement]
        gate = evidence_module.GateRequirement("example-declaration", declarations)
        rule_names.clear()
        declarations.clear()
        self.assertEqual(
            gate.evidence_declarations[0].required_rule_declarations,
            source_requirement.required_rule_declarations,
        )
        self.assertIs(type(gate.evidence_declarations), tuple)

    def test_public_identity_constructor_enforces_schema_before_byte_check(self) -> None:
        digest = hashlib.sha256(b"x").hexdigest()
        valid = dict(
            algorithm="sha256", artifact_name="fixture",
            declared_expected_sha256=digest, declared_observed_sha256=digest,
            declared_byte_count=1,
        )
        for field, value, pattern in (
            ("algorithm", "md5", "algorithm must be sha256"),
            ("artifact_name", [], "exact nonempty string"),
            ("declared_expected_sha256", "invalid", "lowercase SHA-256"),
            ("declared_byte_count", True, "exact nonnegative integer"),
            ("declared_byte_count", -1, "exact nonnegative integer"),
        ):
            with self.subTest(field=field, value=value):
                self.assert_refuses(
                    lambda: EvidenceIdentityDeclaration(**{**valid, field: value}),
                    pattern,
                )
        identity = EvidenceIdentityDeclaration(**valid)
        checked = check_supplied_bytes_against_identity_declaration(identity, b"x")
        self.assertEqual((checked.sha256, checked.byte_count), (digest, 1))
        with self.assertRaisesRegex(TypeError, "use "):
            replace(checked, sha256="0" * 64)

    def test_public_nested_declaration_constructors_reject_invalid_values(self) -> None:
        record = validate_evidence_record_declaration(
            self.record_for(GATE_REQUIREMENTS[0].evidence_declarations[0])
        )
        for field, value, pattern in (
            ("schema", "unknown", "unknown evidence declaration schema"),
            ("declared_category", "unknown", "unknown declared evidence category"),
            ("declared_resolution", "unknown", "unknown declared resolution"),
            ("identity_declaration", {}, "exact EvidenceIdentityDeclaration"),
            ("provenance_declarations", {}, "exact ProvenanceDeclarations"),
            ("rule_result_declarations", [{}], "exact RuleResultDeclaration"),
        ):
            with self.subTest(field=field):
                self.assert_refuses(
                    lambda: replace(record, **{field: value}), pattern
                )
        self.assert_refuses(
            lambda: evidence_module.ProvenanceDeclarations([], "a", "c", "v"),
            "exact nonempty string",
        )
        self.assert_refuses(
            lambda: evidence_module.RuleResultDeclaration("rule", 1),
            "exact boolean",
        )

    def test_missing_and_extra_declarations_reach_cardinality_layer(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        missing = self.submission_for(gate)
        missing["evidence_declarations"].pop()
        extra = self.submission_for(gate)
        extra["evidence_declarations"].append(
            self.record_for(gate.evidence_declarations[0], 99)
        )
        for submission in (missing, extra):
            with self.subTest(submission=submission):
                self.assert_refuses(
                    lambda submission=submission: validate_gate_declaration_submission(
                        self.contract, submission
                    ),
                    "missing or extra evidence declarations",
                )

    def test_duplicate_free_form_id_reaches_id_layer_with_distinct_identities(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        submission = self.submission_for(gate)
        submission["evidence_declarations"][1]["evidence_id"] = submission[
            "evidence_declarations"
        ][0]["evidence_id"]
        self.assertNotEqual(
            submission["evidence_declarations"][0]["identity_declaration"],
            submission["evidence_declarations"][1]["identity_declaration"],
        )
        self.assert_refuses(
            lambda: validate_gate_declaration_submission(self.contract, submission),
            "duplicate evidence_id declaration",
        )

    def test_repeated_canonical_identity_reaches_identity_layer_with_distinct_ids(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        submission = self.submission_for(gate)
        first, second = submission["evidence_declarations"][:2]
        self.assertNotEqual(first["evidence_id"], second["evidence_id"])
        second["identity_declaration"] = copy.deepcopy(first["identity_declaration"])
        self.assert_refuses(
            lambda: validate_gate_declaration_submission(self.contract, submission),
            "canonical declared byte identity reused within gate",
        )

    def test_repeated_unknown_and_out_of_order_requirements_reach_requirement_layer(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        repeated = self.submission_for(gate)
        repeated["evidence_declarations"][1]["requirement_id"] = repeated[
            "evidence_declarations"
        ][0]["requirement_id"]
        unknown = self.submission_for(gate)
        unknown["evidence_declarations"][0]["requirement_id"] = "unknown_requirement"
        out_of_order = self.submission_for(gate)
        out_of_order["evidence_declarations"][0], out_of_order[
            "evidence_declarations"
        ][1] = (
            out_of_order["evidence_declarations"][1],
            out_of_order["evidence_declarations"][0],
        )
        for submission in (repeated, unknown, out_of_order):
            with self.subTest(submission=submission):
                self.assert_refuses(
                    lambda submission=submission: validate_gate_declaration_submission(
                        self.contract, submission
                    ),
                    "requirement declarations are missing, unknown, duplicated, or out of order",
                )

    def test_authoritative_and_provenance_slot_substitutions_reach_category_layer(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        substitutions = (
            (0, SYNTHETIC_TEST),
            (0, REPORTED_NOT_REPRODUCED),
            (1, AUTHORITATIVE_PRIMARY),
            (1, SYNTHETIC_TEST),
            (1, REPORTED_NOT_REPRODUCED),
        )
        for index, declared_category in substitutions:
            with self.subTest(index=index, declared_category=declared_category):
                submission = self.submission_for(gate)
                submission["evidence_declarations"][index][
                    "declared_category"
                ] = declared_category
                self.assert_refuses(
                    lambda submission=submission: validate_gate_declaration_submission(
                        self.contract, submission
                    ),
                    "declared category cannot occupy",
                )

    def test_relabelled_synthetic_or_reported_content_never_becomes_proof(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        for description in ("synthetic fixture", "reported-only summary"):
            with self.subTest(description=description):
                submission = self.submission_for(gate)
                record = submission["evidence_declarations"][0]
                record["declared_subject"] = description
                record["provenance_declarations"]["origin"] = description
                record["declared_category"] = AUTHORITATIVE_PRIMARY
                coverage = validate_gate_declaration_submission(
                    self.contract, submission
                )
                self.assertTrue(coverage.declaration_schema_covered)
                self.assertFalse(coverage.evidence_verified)
                self.assertFalse(coverage.substantive_gate_resolved)
                self.assertEqual(coverage.overall_status, "HOLD")

    def test_wrong_and_incomplete_rule_sets_reach_rule_layer(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        missing = self.submission_for(gate)
        missing["evidence_declarations"][0]["rule_result_declarations"].pop()
        unknown = self.submission_for(gate)
        unknown["evidence_declarations"][0]["rule_result_declarations"][0][
            "rule_id"
        ] = "unknown_rule"
        unknown["evidence_declarations"][0]["rule_result_declarations"].sort(
            key=lambda item: item["rule_id"]
        )
        for submission in (missing, unknown):
            with self.subTest(submission=submission):
                self.assert_refuses(
                    lambda submission=submission: validate_gate_declaration_submission(
                        self.contract, submission
                    ),
                    "rule declarations mismatch",
                )

    def test_submission_contract_hash_binding_is_structural_only(self) -> None:
        submission = self.submission_for(GATE_REQUIREMENTS[0])
        submission["contract_sha256"] = "0" * 64
        self.assert_refuses(
            lambda: validate_gate_declaration_submission(self.contract, submission),
            "not bound to this contract",
        )

    def test_gate_submission_rejects_schema_field_and_type_errors(self) -> None:
        gate = GATE_REQUIREMENTS[0]
        missing = self.submission_for(gate)
        del missing["schema"]
        extra = self.submission_for(gate)
        extra["ready"] = True
        boolean_evidence = self.submission_for(gate)
        boolean_evidence["evidence_declarations"] = True
        for submission in (missing, extra, boolean_evidence):
            with self.subTest(submission=submission):
                self.assert_refuses(
                    lambda submission=submission: validate_gate_declaration_submission(
                        self.contract, submission
                    )
                )

    def test_contract_and_exports_expose_hold_only_structural_paths(self) -> None:
        self.assertEqual(self.contract["contract_phase"], CONTRACT_PHASE)
        self.assertEqual(self.contract["overall_status"], TERMINAL_STATUS)
        for forbidden_field in (
            "credential",
            "transport",
            "production_adapter",
            "e0_authorization",
            "ready",
            "execution",
            "gate_passed",
            "evidence_verified",
        ):
            self.assertNotIn(forbidden_field, self.contract)

        exported_callables = {
            name
            for name in evidence_module.__all__
            if callable(getattr(evidence_module, name, None))
        }
        for forbidden_fragment in (
            "credential",
            "transport",
            "adapter",
            "freeze",
            "manifest",
            "package",
            "ready",
            "authorization",
            "execute",
        ):
            self.assertFalse(
                any(forbidden_fragment in name.lower() for name in exported_callables)
            )

    def test_import_time_boundary_installs_blockers_before_source_execution(self) -> None:
        source_path = pathlib.Path(evidence_module.__file__)
        source_bytes = source_path.read_bytes()
        code = compile(source_bytes, str(source_path), "exec")
        credential_probe_path = pathlib.Path("h2a0-inert-credential-probe")
        allowed_import_roots = {
            "__future__",
            "hashlib",
            "json",
            "re",
            "dataclasses",
            "types",
            "typing",
        }
        real_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            root = name.split(".", 1)[0]
            if level == 0 and root not in allowed_import_roots:
                raise AssertionError(f"forbidden dynamic import during module execution: {name}")
            return real_import(name, globals, locals, fromlist, level)

        def guarded_open(file, mode="r", *args, **kwargs):
            if any(flag in mode for flag in "wax+"):
                raise AssertionError("filesystem write forbidden during module execution")
            raise AssertionError(
                "direct file read forbidden during module execution, including credentials"
            )

        def forbidden(*args, **kwargs):
            raise AssertionError("forbidden capability used during module execution")

        class ForbiddenEnvironment(dict):
            def __getitem__(self, key):
                return forbidden(key)

            def get(self, key, default=None):
                return forbidden(key, default)

        probe_name = "_ns001_h2a0_import_boundary_probe"
        probe = types.ModuleType(probe_name)
        probe.__file__ = str(source_path)
        probe.__package__ = "e0.h2"
        sys.modules[probe_name] = probe
        try:
            with contextlib.ExitStack() as stack:
                for target in (
                    (socket, "socket"),
                    (socket, "create_connection"),
                    (socket, "getaddrinfo"),
                    (urllib.request, "urlopen"),
                    (getpass, "getpass"),
                    (netrc, "netrc"),
                    (subprocess, "Popen"),
                    (subprocess, "run"),
                    (subprocess, "call"),
                    (subprocess, "check_call"),
                    (subprocess, "check_output"),
                    (importlib, "import_module"),
                ):
                    stack.enter_context(mock.patch.object(*target, side_effect=forbidden))
                stack.enter_context(
                    mock.patch.object(os, "environ", ForbiddenEnvironment())
                )
                # Source and stdlib dependencies are already read/loaded. Block
                # application file reads without intercepting Python's loader.
                stack.enter_context(mock.patch.object(builtins, "open", guarded_open))
                stack.enter_context(mock.patch.object(io, "open", guarded_open))
                stack.enter_context(mock.patch.object(builtins, "input", side_effect=forbidden))
                stack.enter_context(
                    mock.patch.object(builtins, "__import__", guarded_import)
                )
                exec(code, probe.__dict__, probe.__dict__)
                # Inert names: these probes must fail before any file access or prompt.
                for expression, pattern in (
                    ("open('h2a0-inert-credential-probe', 'r')", "direct file read forbidden"),
                    ("input('h2a0-inert-prompt')", "forbidden capability"),
                    ("open('h2a0-inert-write-probe', 'w')", "filesystem write forbidden"),
                ):
                    with self.subTest(expression=expression):
                        with self.assertRaisesRegex(AssertionError, pattern):
                            exec(expression, probe.__dict__, probe.__dict__)
                with self.assertRaisesRegex(AssertionError, "direct file read forbidden"):
                    credential_probe_path.read_bytes()
        finally:
            del sys.modules[probe_name]

        self.assertEqual(probe.TERMINAL_STATUS, "HOLD")
        self.assertNotIn("os", probe.__dict__)
        self.assertNotIn("subprocess", probe.__dict__)
        self.assertNotIn("socket", probe.__dict__)
        self.assertNotIn("importlib", probe.__dict__)

    def test_network_and_credential_blockade_catches_direct_attempts(self) -> None:
        attempts = (
            lambda: socket.socket(),
            lambda: socket.create_connection(("127.0.0.1", 9)),
            lambda: socket.getaddrinfo("example.invalid", 443),
            lambda: urllib.request.urlopen("https://example.invalid"),
            lambda: getpass.getpass("secret: "),
            lambda: netrc.netrc(),
        )
        for attempt in attempts:
            with self.subTest(attempt=attempt):
                with self.assertRaisesRegex(AssertionError, "forbidden"):
                    attempt()


if __name__ == "__main__":
    unittest.main()
