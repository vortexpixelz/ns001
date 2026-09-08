"""Pure H2A0 declaration-schema validation for NS-001 E0.

H2A0 fixes declaration shapes and expected anchor values. It does not
authenticate authority, provenance, custody, retained bytes, verifier identity,
rule results, Git state, external artifacts, gate passage, readiness, or E0
authorization. Those are later-H2 responsibilities and every substantive gate
remains unresolved.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Sequence


H1_CHECKPOINT_COMMIT = "6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff"
SCIENTIFIC_BASE_COMMIT = "0393315223df8ed90f20f0c821508cc98bea08d1"
FROZEN_PREREGISTRATION_SHA256 = (
    "a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78"
)
H1_AUDIT_BUNDLE_SHA256 = (
    "a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f"
)

CONTRACT_SCHEMA = "ns001.h2.declaration-contract.v1"
EVIDENCE_DECLARATION_SCHEMA = "ns001.h2.evidence-declaration.v1"
GATE_DECLARATION_SUBMISSION_SCHEMA = "ns001.h2.gate-declaration-submission.v1"
CONTRACT_PHASE = "DRAFT_H2A0_DECLARATIONS_ONLY"
TERMINAL_STATUS = "HOLD"

AUTHORITATIVE_PRIMARY = "authoritative_primary"
RETAINED_ACQUISITION_PROVENANCE = "retained_acquisition_provenance"
SYNTHETIC_TEST = "synthetic_test"
REPORTED_NOT_REPRODUCED = "reported_not_reproduced"
UNRESOLVED_ASSERTION = "unresolved_assertion"

DECLARED_EVIDENCE_CATEGORIES = frozenset(
    {
        AUTHORITATIVE_PRIMARY,
        RETAINED_ACQUISITION_PROVENANCE,
        SYNTHETIC_TEST,
        REPORTED_NOT_REPRODUCED,
        UNRESOLVED_ASSERTION,
    }
)
DECLARED_RESOLUTION_STATES = frozenset(
    {"resolved", "unresolved", "ambiguous", "contradictory"}
)

EXPECTED_ANCHOR_DECLARATIONS: Mapping[str, str] = MappingProxyType(
    {
        "h1_checkpoint_commit": H1_CHECKPOINT_COMMIT,
        "scientific_base_commit": SCIENTIFIC_BASE_COMMIT,
        "frozen_preregistration_sha256": FROZEN_PREREGISTRATION_SHA256,
        "h1_audit_bundle_sha256": H1_AUDIT_BUNDLE_SHA256,
    }
)

LATER_H2_VERIFIER_BY_CATEGORY: Mapping[str, str] = MappingProxyType(
    {
        AUTHORITATIVE_PRIMARY: "later_h2.authority_and_content_verifier",
        RETAINED_ACQUISITION_PROVENANCE: (
            "later_h2.origin_custody_and_retained_bytes_verifier"
        ),
        SYNTHETIC_TEST: "later_h2.synthetic_execution_verifier",
        REPORTED_NOT_REPRODUCED: "later_h2.report_attribution_verifier",
        UNRESOLVED_ASSERTION: "later_h2.claim_resolution_verifier",
    }
)

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


class EvidenceContractRefusal(RuntimeError):
    """A declaration or declaration submission failed closed structurally."""


def _fail(message: str) -> None:
    raise EvidenceContractRefusal(message)


def _exact_mapping(value: object, fields: Sequence[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(f"{label} must be an exact mapping")
    mapping = value
    if any(type(key) is not str for key in mapping):
        _fail(f"{label} keys must be exact strings")
    expected = set(fields)
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        _fail(f"{label} fields mismatch; missing={missing}, extra={extra}")
    return mapping


def _exact_list(value: object, label: str) -> list[Any]:
    if type(value) is not list:
        _fail(f"{label} must be an exact list")
    return value


def _exact_string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        _fail(f"{label} must be an exact nonempty string")
    return value


def _exact_bool(value: object, label: str) -> bool:
    if type(value) is not bool:
        _fail(f"{label} must be an exact boolean")
    return value


def _exact_nonnegative_int(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        _fail(f"{label} must be an exact nonnegative integer")
    return value


def _sha256(value: object, label: str) -> str:
    digest = _exact_string(value, label)
    if _SHA256_PATTERN.fullmatch(digest) is None:
        _fail(f"{label} must be a lowercase SHA-256 digest")
    return digest


def _immutable_items(value: object, label: str) -> tuple:
    """Copy supported input containers without retaining caller-owned lists."""
    if type(value) not in (list, tuple):
        _fail(f"{label} must be an exact list or tuple")
    return tuple(item for item in value)


def _factory_value(cls: type, **fields: object):
    """Internal construction only after the calling validator has succeeded."""
    result = object.__new__(cls)
    for name, value in fields.items():
        object.__setattr__(result, name, value)
    return result


@dataclass(frozen=True, slots=True)
class EvidenceRequirement:
    requirement_id: str
    declared_category: str
    later_h2_verifier: str
    required_rule_declarations: tuple[str, ...]

    def __post_init__(self) -> None:
        _exact_string(self.requirement_id, "requirement_id")
        category = _exact_string(self.declared_category, "declared_category")
        if category not in DECLARED_EVIDENCE_CATEGORIES:
            _fail("unknown declared evidence category")
        if _exact_string(self.later_h2_verifier, "later_h2_verifier") != (
            LATER_H2_VERIFIER_BY_CATEGORY[category]
        ):
            _fail("later verifier does not match declared category")
        rules = _immutable_items(self.required_rule_declarations, "rule declarations")
        for rule in rules:
            _exact_string(rule, "rule_id")
        if rules != tuple(sorted(set(rules))):
            _fail("rule declarations must be unique and sorted")
        object.__setattr__(self, "required_rule_declarations", rules)


@dataclass(frozen=True, slots=True)
class GateRequirement:
    gate_id: str
    evidence_declarations: tuple[EvidenceRequirement, ...]

    def __post_init__(self) -> None:
        _exact_string(self.gate_id, "gate_id")
        items = _immutable_items(self.evidence_declarations, "evidence declarations")
        if any(type(item) is not EvidenceRequirement for item in items):
            _fail("evidence declarations must contain exact EvidenceRequirement values")
        copied = tuple(
            EvidenceRequirement(
                item.requirement_id, item.declared_category,
                item.later_h2_verifier, item.required_rule_declarations,
            )
            for item in items
        )
        if len({item.requirement_id for item in copied}) != len(copied):
            _fail("duplicate requirement declaration")
        object.__setattr__(self, "evidence_declarations", copied)


@dataclass(frozen=True, slots=True, init=False)
class ValidatedEvidenceContract:
    """Deeply immutable H2A0 contract declaration."""

    expected_anchor_declarations: tuple[tuple[str, str], ...]
    gates: tuple[GateRequirement, ...]

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("use validate_evidence_contract()")

    @property
    def schema(self) -> str:
        return CONTRACT_SCHEMA

    @property
    def contract_phase(self) -> str:
        return CONTRACT_PHASE

    @property
    def overall_status(self) -> str:
        return "HOLD"

    def to_json_value(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "contract_phase": self.contract_phase,
            "overall_status": self.overall_status,
            "expected_anchor_declarations": dict(self.expected_anchor_declarations),
            "gates": [_gate_dict(gate) for gate in self.gates],
        }


@dataclass(frozen=True, slots=True)
class ProvenanceDeclarations:
    origin: str
    authority: str
    custody: str
    verifier: str

    def __post_init__(self) -> None:
        for name in ("origin", "authority", "custody", "verifier"):
            _exact_string(getattr(self, name), f"declared {name}")


@dataclass(frozen=True, slots=True)
class EvidenceIdentityDeclaration:
    algorithm: str
    artifact_name: str
    declared_expected_sha256: str
    declared_observed_sha256: str
    declared_byte_count: int

    def __post_init__(self) -> None:
        if _exact_string(self.algorithm, "declared algorithm") != "sha256":
            _fail("declared identity algorithm must be sha256")
        _exact_string(self.artifact_name, "declared artifact_name")
        _sha256(self.declared_expected_sha256, "declared_expected_sha256")
        _sha256(self.declared_observed_sha256, "declared_observed_sha256")
        _exact_nonnegative_int(self.declared_byte_count, "declared_byte_count")

    @property
    def canonical_identity_tuple(self) -> tuple[str, str, int]:
        """Canonical declared byte identity used for within-gate reuse checks."""

        return (
            self.algorithm,
            self.declared_observed_sha256,
            self.declared_byte_count,
        )


@dataclass(frozen=True, slots=True)
class RuleResultDeclaration:
    rule_id: str
    declared_passed: bool

    def __post_init__(self) -> None:
        _exact_string(self.rule_id, "rule_id")
        _exact_bool(self.declared_passed, "declared_passed")


@dataclass(frozen=True, slots=True)
class EvidenceRecordDeclaration:
    schema: str
    evidence_id: str
    requirement_id: str
    declared_category: str
    declared_subject: str
    identity_declaration: EvidenceIdentityDeclaration
    provenance_declarations: ProvenanceDeclarations
    declared_resolution: str
    rule_result_declarations: tuple[RuleResultDeclaration, ...]

    def __post_init__(self) -> None:
        if _exact_string(self.schema, "schema") != EVIDENCE_DECLARATION_SCHEMA:
            _fail("unknown evidence declaration schema")
        for name in ("evidence_id", "requirement_id", "declared_subject"):
            _exact_string(getattr(self, name), name)
        if _exact_string(self.declared_category, "declared category") not in (
            DECLARED_EVIDENCE_CATEGORIES
        ):
            _fail("unknown declared evidence category")
        if _exact_string(self.declared_resolution, "declared resolution") not in (
            DECLARED_RESOLUTION_STATES
        ):
            _fail("unknown declared resolution")
        identity = self.identity_declaration
        if type(identity) is not EvidenceIdentityDeclaration:
            _fail("identity must be an exact EvidenceIdentityDeclaration")
        provenance = self.provenance_declarations
        if type(provenance) is not ProvenanceDeclarations:
            _fail("provenance must be exact ProvenanceDeclarations")
        rules = _immutable_items(self.rule_result_declarations, "rule results")
        if any(type(rule) is not RuleResultDeclaration for rule in rules):
            _fail("rule results must contain exact RuleResultDeclaration values")
        copied_rules = tuple(
            RuleResultDeclaration(rule.rule_id, rule.declared_passed) for rule in rules
        )
        ids = tuple(rule.rule_id for rule in copied_rules)
        if ids != tuple(sorted(set(ids))):
            _fail("rule-result declaration ids must be unique and sorted")
        object.__setattr__(self, "identity_declaration", EvidenceIdentityDeclaration(
            identity.algorithm, identity.artifact_name,
            identity.declared_expected_sha256, identity.declared_observed_sha256,
            identity.declared_byte_count,
        ))
        object.__setattr__(self, "provenance_declarations", ProvenanceDeclarations(
            provenance.origin, provenance.authority, provenance.custody,
            provenance.verifier,
        ))
        object.__setattr__(self, "rule_result_declarations", copied_rules)


@dataclass(frozen=True, slots=True, init=False)
class SuppliedBytesIdentityCheck:
    """Successful consistency check scoped only to the exact supplied bytes."""

    sha256: str
    byte_count: int

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("use check_supplied_bytes_against_identity_declaration()")


@dataclass(frozen=True, slots=True, init=False)
class GateDeclarationSubmissionCoverage:
    """Schema coverage only; never evidence verification or gate passage."""

    gate_id: str
    contract_sha256: str
    evidence_ids: tuple[str, ...]

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("use validate_gate_declaration_submission()")

    @property
    def declaration_schema_covered(self) -> bool:
        return True

    @property
    def evidence_verified(self) -> bool:
        return False

    @property
    def substantive_gate_resolved(self) -> bool:
        return False

    @property
    def overall_status(self) -> str:
        return "HOLD"


def _requirement(
    requirement_id: str, declared_category: str, rules: tuple[str, ...]
) -> EvidenceRequirement:
    return EvidenceRequirement(
        requirement_id=requirement_id,
        declared_category=declared_category,
        later_h2_verifier=LATER_H2_VERIFIER_BY_CATEGORY[declared_category],
        required_rule_declarations=rules,
    )


GATE_REQUIREMENTS: tuple[GateRequirement, ...] = (
    GateRequirement(
        "external_trust_root",
        (
            _requirement(
                "trust_root_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "bytecode_substitution_blocked",
                    "exact_verified_bytes_executed",
                    "source_substitution_blocked",
                ),
            ),
            _requirement(
                "trust_root_provenance",
                RETAINED_ACQUISITION_PROVENANCE,
                ("immutable_identity_recorded", "source_origin_recorded"),
            ),
            _requirement(
                "trust_root_offline_acceptance",
                SYNTHETIC_TEST,
                (
                    "ambient_import_refused",
                    "hash_to_load_substitution_refused",
                    "stale_pyc_refused",
                ),
            ),
        ),
    ),
    GateRequirement(
        "client_source",
        (
            _requirement(
                "client_source_primary",
                AUTHORITATIVE_PRIMARY,
                ("client_commit_pinned", "exact_source_selected", "license_recorded"),
            ),
            _requirement(
                "client_source_acquisition",
                RETAINED_ACQUISITION_PROVENANCE,
                ("acquisition_bytes_retained", "digest_verified", "origin_recorded"),
            ),
        ),
    ),
    GateRequirement(
        "response_contract",
        (
            _requirement(
                "response_contract_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "dtype_shape_variants_bounded",
                    "gradient_order_proven",
                    "nine_columns_proven",
                    "result_extraction_proven",
                ),
            ),
            _requirement(
                "response_contract_offline_acceptance",
                SYNTHETIC_TEST,
                ("fixture_mapping_explicit", "malformed_responses_refused"),
            ),
        ),
    ),
    GateRequirement(
        "transport_accounting",
        (
            _requirement(
                "transport_call_graph_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "hidden_calls_excluded",
                    "initialization_calls_enumerated",
                    "internal_retries_bounded",
                ),
            ),
            _requirement(
                "transport_accounting_offline_acceptance",
                SYNTHETIC_TEST,
                ("all_egress_observed", "redirects_counted", "retry_owner_unique"),
            ),
        ),
    ),
    GateRequirement(
        "dependency_runtime_lock",
        (
            _requirement(
                "dependency_closure",
                RETAINED_ACQUISITION_PROVENANCE,
                ("all_transitive_dependencies_pinned", "artifact_hashes_verified"),
            ),
            _requirement(
                "runtime_identity_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "immutable_runtime_verified",
                    "interpreter_platform_native_identity_pinned",
                ),
            ),
            _requirement(
                "offline_runtime_acceptance",
                SYNTHETIC_TEST,
                ("dependency_closure_complete", "network_blocked_install_succeeds"),
            ),
        ),
    ),
    GateRequirement(
        "maximum_partition_memory",
        (
            _requirement(
                "memory_policy_primary",
                AUTHORITATIVE_PRIMARY,
                ("measurement_environment_fixed", "prospective_ceiling_declared"),
            ),
            _requirement(
                "maximum_partition_memory_acceptance",
                SYNTHETIC_TEST,
                (
                    "ceiling_met",
                    "full_two_million_point_path_measured",
                    "process_tree_covered",
                    "swap_policy_enforced",
                ),
            ),
        ),
    ),
    GateRequirement(
        "amendment_freeze",
        (
            _requirement(
                "frozen_amendment_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "amendment_hash_frozen",
                    "original_preregistration_unchanged",
                    "prospective_review_approved",
                    "sidecar_consistent",
                ),
            ),
            _requirement(
                "amendment_review_provenance",
                RETAINED_ACQUISITION_PROVENANCE,
                ("approval_record_retained", "review_identity_recorded"),
            ),
        ),
    ),
    GateRequirement(
        "final_manifest_package_audit",
        (
            _requirement(
                "final_manifest_primary",
                AUTHORITATIVE_PRIMARY,
                (
                    "all_artifacts_bound",
                    "no_e0_authorization_embedded",
                    "self_reference_avoided",
                    "twelve_operations_exact",
                ),
            ),
            _requirement(
                "independent_package_audit",
                AUTHORITATIVE_PRIMARY,
                (
                    "exclusions_verified",
                    "independent_review_completed",
                    "package_hash_verified",
                ),
            ),
            _requirement(
                "package_audit_provenance",
                RETAINED_ACQUISITION_PROVENANCE,
                ("audit_inputs_retained", "audit_receipt_retained"),
            ),
        ),
    ),
)

_GATES_BY_ID = MappingProxyType({gate.gate_id: gate for gate in GATE_REQUIREMENTS})
_FIXED_VALIDATED_CONTRACT = _factory_value(
    ValidatedEvidenceContract,
    expected_anchor_declarations=tuple(EXPECTED_ANCHOR_DECLARATIONS.items()),
    gates=GATE_REQUIREMENTS,
)


def _validate_json_value(value: object, label: str = "value") -> None:
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is list:
        for index, item in enumerate(value):
            _validate_json_value(item, f"{label}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                _fail(f"{label} contains a non-string key")
            _validate_json_value(item, f"{label}.{key}")
        return
    _fail(f"{label} contains a non-canonical JSON type")


def canonical_json_bytes(value: object) -> bytes:
    """Return the deterministic representation used for H2A0 declarations."""

    _validate_json_value(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def parse_json_bytes(data: object) -> object:
    """Parse UTF-8 JSON while rejecting duplicate fields and malformed input."""

    if type(data) is not bytes:
        _fail("JSON input must be exact bytes")

    def reject_duplicate_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"duplicate JSON field: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        _fail(f"non-finite JSON number is forbidden: {value}")

    try:
        parsed = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=reject_duplicate_fields,
            parse_constant=reject_constant,
        )
    except EvidenceContractRefusal:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceContractRefusal("malformed UTF-8 JSON") from exc
    _validate_json_value(parsed)
    return parsed


def _requirement_dict(requirement: EvidenceRequirement) -> dict[str, object]:
    return {
        "requirement_id": requirement.requirement_id,
        "declared_category": requirement.declared_category,
        "later_h2_verifier": requirement.later_h2_verifier,
        "required_rule_declarations": list(requirement.required_rule_declarations),
    }


def _gate_dict(gate: GateRequirement) -> dict[str, object]:
    return {
        "gate_id": gate.gate_id,
        "required_evidence_declarations": [
            _requirement_dict(item) for item in gate.evidence_declarations
        ],
    }


def build_evidence_contract() -> dict[str, object]:
    """Build a fresh JSON-compatible copy of the fixed H2A0 declarations."""

    return _FIXED_VALIDATED_CONTRACT.to_json_value()


def validate_evidence_contract(contract: object) -> ValidatedEvidenceContract:
    """Validate exact declarations and return a deeply immutable value."""

    root = _exact_mapping(
        contract,
        (
            "schema",
            "contract_phase",
            "overall_status",
            "expected_anchor_declarations",
            "gates",
        ),
        "evidence declaration contract",
    )
    _exact_string(root["schema"], "contract schema")
    _exact_string(root["contract_phase"], "contract phase")
    _exact_string(root["overall_status"], "contract overall status")

    anchors = _exact_mapping(
        root["expected_anchor_declarations"],
        tuple(EXPECTED_ANCHOR_DECLARATIONS),
        "expected anchor declarations",
    )
    for name, expected in EXPECTED_ANCHOR_DECLARATIONS.items():
        declared = _exact_string(anchors[name], f"expected anchor declaration {name}")
        if declared != expected:
            _fail(f"expected anchor declaration mismatch: {name}")

    gates = _exact_list(root["gates"], "gates")
    seen_gate_ids: set[str] = set()
    for index, gate_value in enumerate(gates):
        gate = _exact_mapping(
            gate_value,
            ("gate_id", "required_evidence_declarations"),
            f"gate[{index}]",
        )
        gate_id = _exact_string(gate["gate_id"], f"gate[{index}].gate_id")
        if gate_id in seen_gate_ids:
            _fail(f"duplicate gate declaration: {gate_id}")
        seen_gate_ids.add(gate_id)
        if gate_id not in _GATES_BY_ID:
            _fail(f"unknown gate declaration: {gate_id}")
        evidence = _exact_list(
            gate["required_evidence_declarations"],
            f"gate {gate_id} required evidence declarations",
        )
        seen_requirements: set[str] = set()
        for requirement_index, requirement_value in enumerate(evidence):
            label = f"gate {gate_id} declaration[{requirement_index}]"
            requirement = _exact_mapping(
                requirement_value,
                (
                    "requirement_id",
                    "declared_category",
                    "later_h2_verifier",
                    "required_rule_declarations",
                ),
                label,
            )
            requirement_id = _exact_string(
                requirement["requirement_id"], f"{label}.requirement_id"
            )
            if requirement_id in seen_requirements:
                _fail(f"duplicate requirement declaration: {requirement_id}")
            seen_requirements.add(requirement_id)
            category = _exact_string(
                requirement["declared_category"], f"{label}.declared_category"
            )
            if category not in DECLARED_EVIDENCE_CATEGORIES:
                _fail(f"unknown declared evidence category: {category}")
            _exact_string(
                requirement["later_h2_verifier"], f"{label}.later_h2_verifier"
            )
            rules = _exact_list(
                requirement["required_rule_declarations"],
                f"{label}.required_rule_declarations",
            )
            rule_names = [
                _exact_string(rule, f"{label}.required_rule_declarations[{rule_index}]")
                for rule_index, rule in enumerate(rules)
            ]
            if rule_names != sorted(set(rule_names)):
                _fail(f"{label} rule declarations must be unique and sorted")

    if root != build_evidence_contract():
        _fail("contract differs from the fixed H2A0 declaration contract")
    return _FIXED_VALIDATED_CONTRACT


def evidence_contract_sha256(contract: object) -> str:
    validated = validate_evidence_contract(contract)
    return canonical_sha256(validated.to_json_value())


def validate_evidence_record_declaration(
    record: object,
) -> EvidenceRecordDeclaration:
    """Validate declaration shape without authenticating any declaration."""

    root = _exact_mapping(
        record,
        (
            "schema",
            "evidence_id",
            "requirement_id",
            "declared_category",
            "declared_subject",
            "identity_declaration",
            "provenance_declarations",
            "declared_resolution",
            "rule_result_declarations",
        ),
        "evidence record declaration",
    )
    schema = _exact_string(root["schema"], "evidence declaration schema")
    if schema != EVIDENCE_DECLARATION_SCHEMA:
        _fail("unknown evidence declaration schema")
    evidence_id = _exact_string(root["evidence_id"], "evidence_id")
    requirement_id = _exact_string(root["requirement_id"], "requirement_id")
    category = _exact_string(root["declared_category"], "declared category")
    if category not in DECLARED_EVIDENCE_CATEGORIES:
        _fail(f"unknown declared evidence category: {category}")
    subject = _exact_string(root["declared_subject"], "declared subject")
    resolution = _exact_string(root["declared_resolution"], "declared resolution")
    if resolution not in DECLARED_RESOLUTION_STATES:
        _fail(f"unknown declared resolution: {resolution}")

    identity_value = _exact_mapping(
        root["identity_declaration"],
        (
            "algorithm",
            "artifact_name",
            "declared_expected_sha256",
            "declared_observed_sha256",
            "declared_byte_count",
        ),
        "identity declaration",
    )
    algorithm = _exact_string(identity_value["algorithm"], "declared algorithm")
    if algorithm != "sha256":
        _fail("declared identity algorithm must be sha256")
    identity = EvidenceIdentityDeclaration(
        algorithm=algorithm,
        artifact_name=_exact_string(
            identity_value["artifact_name"], "declared artifact_name"
        ),
        declared_expected_sha256=_sha256(
            identity_value["declared_expected_sha256"],
            "declared_expected_sha256",
        ),
        declared_observed_sha256=_sha256(
            identity_value["declared_observed_sha256"],
            "declared_observed_sha256",
        ),
        declared_byte_count=_exact_nonnegative_int(
            identity_value["declared_byte_count"], "declared_byte_count"
        ),
    )

    provenance_value = _exact_mapping(
        root["provenance_declarations"],
        ("origin", "authority", "custody", "verifier"),
        "provenance declarations",
    )
    provenance = ProvenanceDeclarations(
        origin=_exact_string(provenance_value["origin"], "declared origin"),
        authority=_exact_string(
            provenance_value["authority"], "declared authority"
        ),
        custody=_exact_string(provenance_value["custody"], "declared custody"),
        verifier=_exact_string(
            provenance_value["verifier"], "declared verifier"
        ),
    )

    rule_values = _exact_list(
        root["rule_result_declarations"], "rule-result declarations"
    )
    rules: list[RuleResultDeclaration] = []
    for index, rule_value in enumerate(rule_values):
        rule = _exact_mapping(
            rule_value,
            ("rule_id", "declared_passed"),
            f"rule-result declaration[{index}]",
        )
        rules.append(
            RuleResultDeclaration(
                rule_id=_exact_string(
                    rule["rule_id"], f"rule-result declaration[{index}].rule_id"
                ),
                declared_passed=_exact_bool(
                    rule["declared_passed"],
                    f"rule-result declaration[{index}].declared_passed",
                ),
            )
        )
    rule_ids = [item.rule_id for item in rules]
    if rule_ids != sorted(set(rule_ids)):
        _fail("rule-result declaration ids must be unique and sorted")

    return EvidenceRecordDeclaration(
        schema=schema,
        evidence_id=evidence_id,
        requirement_id=requirement_id,
        declared_category=category,
        declared_subject=subject,
        identity_declaration=identity,
        provenance_declarations=provenance,
        declared_resolution=resolution,
        rule_result_declarations=tuple(rules),
    )


def check_supplied_bytes_against_identity_declaration(
    identity: object, artifact_bytes: object
) -> SuppliedBytesIdentityCheck:
    """Check only supplied-byte hash/length consistency, never provenance."""

    if type(identity) is not EvidenceIdentityDeclaration:
        _fail("identity must be an immutable EvidenceIdentityDeclaration")
    if type(artifact_bytes) is not bytes:
        _fail("artifact_bytes must be exact bytes")
    actual_count = len(artifact_bytes)
    if actual_count != identity.declared_byte_count:
        _fail("supplied bytes do not match declared byte count")
    actual_digest = hashlib.sha256(artifact_bytes).hexdigest()
    if actual_digest != identity.declared_expected_sha256:
        _fail("supplied bytes do not match declared expected SHA-256")
    if actual_digest != identity.declared_observed_sha256:
        _fail("supplied bytes do not match declared observed SHA-256")
    return _factory_value(
        SuppliedBytesIdentityCheck, sha256=actual_digest, byte_count=actual_count
    )


def validate_gate_declaration_submission(
    contract: object, gate_submission: object
) -> GateDeclarationSubmissionCoverage:
    """Validate declaration-schema coverage while every substantive gate stays unresolved."""

    contract_digest = evidence_contract_sha256(contract)
    submission = _exact_mapping(
        gate_submission,
        ("schema", "gate_id", "contract_sha256", "evidence_declarations"),
        "gate declaration submission",
    )
    if (
        _exact_string(submission["schema"], "gate declaration submission schema")
        != GATE_DECLARATION_SUBMISSION_SCHEMA
    ):
        _fail("unknown gate declaration submission schema")
    gate_id = _exact_string(submission["gate_id"], "gate declaration gate_id")
    if gate_id not in _GATES_BY_ID:
        _fail(f"unknown gate declaration: {gate_id}")
    if _sha256(submission["contract_sha256"], "contract_sha256") != contract_digest:
        _fail("gate declaration submission is not bound to this contract")

    evidence_values = _exact_list(
        submission["evidence_declarations"], "evidence declarations"
    )
    gate = _GATES_BY_ID[gate_id]
    if len(evidence_values) != len(gate.evidence_declarations):
        _fail(f"gate {gate_id} has missing or extra evidence declarations")

    evidence_ids: list[str] = []
    seen_ids: set[str] = set()
    seen_identities: dict[tuple[str, str, int], str] = {}
    for record_value, requirement in zip(
        evidence_values, gate.evidence_declarations, strict=True
    ):
        record = validate_evidence_record_declaration(record_value)
        evidence_id = record.evidence_id
        if evidence_id in seen_ids:
            _fail(f"duplicate evidence_id declaration: {evidence_id}")
        seen_ids.add(evidence_id)
        evidence_ids.append(evidence_id)

        identity_key = record.identity_declaration.canonical_identity_tuple
        if identity_key in seen_identities:
            _fail(
                "canonical declared byte identity reused within gate: "
                f"{seen_identities[identity_key]} and {evidence_id}"
            )
        seen_identities[identity_key] = evidence_id

        if record.requirement_id != requirement.requirement_id:
            _fail(
                f"gate {gate_id} requirement declarations are missing, unknown, "
                "duplicated, or out of order"
            )
        if record.declared_category != requirement.declared_category:
            _fail(
                f"declared category cannot occupy {requirement.requirement_id}: "
                f"required declaration {requirement.declared_category}"
            )
        actual_rules = tuple(
            item.rule_id for item in record.rule_result_declarations
        )
        if actual_rules != requirement.required_rule_declarations:
            _fail(f"rule declarations mismatch for {requirement.requirement_id}")

    return _factory_value(
        GateDeclarationSubmissionCoverage,
        gate_id=gate_id,
        contract_sha256=contract_digest,
        evidence_ids=tuple(evidence_ids),
    )


__all__ = (
    "AUTHORITATIVE_PRIMARY",
    "CONTRACT_SCHEMA",
    "CONTRACT_PHASE",
    "DECLARED_EVIDENCE_CATEGORIES",
    "EVIDENCE_DECLARATION_SCHEMA",
    "EXPECTED_ANCHOR_DECLARATIONS",
    "EvidenceContractRefusal",
    "EvidenceIdentityDeclaration",
    "EvidenceRecordDeclaration",
    "FROZEN_PREREGISTRATION_SHA256",
    "GATE_DECLARATION_SUBMISSION_SCHEMA",
    "GATE_REQUIREMENTS",
    "GateDeclarationSubmissionCoverage",
    "H1_AUDIT_BUNDLE_SHA256",
    "H1_CHECKPOINT_COMMIT",
    "LATER_H2_VERIFIER_BY_CATEGORY",
    "REPORTED_NOT_REPRODUCED",
    "RETAINED_ACQUISITION_PROVENANCE",
    "SCIENTIFIC_BASE_COMMIT",
    "SYNTHETIC_TEST",
    "SuppliedBytesIdentityCheck",
    "TERMINAL_STATUS",
    "UNRESOLVED_ASSERTION",
    "ValidatedEvidenceContract",
    "build_evidence_contract",
    "canonical_json_bytes",
    "canonical_sha256",
    "check_supplied_bytes_against_identity_declaration",
    "evidence_contract_sha256",
    "parse_json_bytes",
    "validate_evidence_contract",
    "validate_evidence_record_declaration",
    "validate_gate_declaration_submission",
)
