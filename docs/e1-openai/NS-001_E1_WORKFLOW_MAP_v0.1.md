# NS-001 / E1 Workflow Map v0.1

Proposed navigation map, not a change to approval criteria. E0 is an independent frozen track.

## 1. Recovered position

**Verified local state.** Both Gate 1 receipts are complete Markdown files, including their closing status statements. v0.2 persisted despite the interrupted chat handoff. No incomplete save or unexpected local modification was found. HEAD is `711b6c7f0cfd1c69694bff8a3fd134b585e633df`, branch `codex/e0-h2-preparation`. Entry tracked diff is empty; the two receipts are untracked, not absent or committed.

| Preserved artifact | SHA-256 checked at entry |
|---|---|
| Derivation receipt v0.1 | `7925644db2b6aba2a8239714b3bfdc8e084d4c8afc9ff22d392f985c9f0dd6fb` |
| Derivation receipt v0.2 | `a0dffb46343beb7cc226cffb49c742619281675af80992a6314639f8a3137ee3` |
| Frozen E0 preregistration | `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78` — matches its sidecar |

Applicable ancestor and `docs`-subtree `AGENTS.md` locations were checked; none were found. The governing review's operating decision and §§6–8 were reread. The local receipts, README status warning, frozen E0 rules, interface draft and H2 declaration-only boundary were inspected as text. Repository code was not executed.

**Verified scientific position:** Gate 1 PARTIAL. The circulation lower bound survives as a mathematical result about the construction, not a DNS primary. `(U,L)` is a candidate operator, not a validated measurement of geometric contraction. Its source-core correspondence and finite-scale validity remain unproved. E0 stays FROZEN / HOLD.

**Evidence limit:** the receipts and visible session record report no experiment or JHTDB-query execution in these review rounds. A clean tracked diff alone cannot prove that nothing ran elsewhere. No external execution audit, remote refresh or empirical-output inspection was undertaken. This round performed no runs, queries, commit or push.

## 2. Navigation vocabulary and current circuit

- **Phase:** a major purpose; it is not an approval gate.
- **Round:** one bounded attempt at one question, with an identified receipt and stopping point.
- **Circuit:** question → authorized work → evidence receipt → decision → stop or separately authorized next round.

| Round | Question and completed work | Receipt / decision |
|---|---|---|
| R1 — derivation | What does the paper imply, and which observable bridges are defensible? Source reconstruction and candidate audit completed. | Derivation receipt v0.1; Gate 1 PARTIAL. Completion of work did not close the gate. |
| R2 — closure attempt | Can the circulation argument, reduced operator and resolving-power conditions close Gate 1? Definitions and conditional bounds completed. | Derivation receipt v0.2; Gate 1 PARTIAL. |
| R3 — this analytical circuit | Can relative component amplitudes produce U↑ and L↓ without narrowing? Explicit counterexample and exactly two options assessed. | [Operator Confounding Audit v0.1](NS-001_E1_OPERATOR_CONFOUNDING_AUDIT_v0.1.md); RETAIN CONDITIONALLY for further source-side bridge work only. Gate 1 PARTIAL. |

**Current position:** Phase 1, R3 closed. No next round begins automatically. The counterexample rules out using the unrestricted U–L sign pair to identify contraction of underlying components.

## 3. Four phases: proposed organization

| Phase | Entry condition | Allowed work and authorization boundary | Exit condition / next decision |
|---|---|---|---|
| **1. Scientific basis** | A bounded source/measurand question and permission for analytical review. Current phase. | Read sources; derive implications and counterexamples; define and assess candidate operators. This round authorizes only this map and one audit. No data, scientific code execution, implementation or controls. | A source-to-observable bridge satisfying Gate 1's unchanged criteria, or a documented rejection. Next: determine whether independently bounded contamination is achievable for the source operator. |
| **2. Measurement readiness** | A scientifically defensible candidate and a separately authorized, bounded readiness task. | Verify response contracts, provenance, estimator implementation and resolving power. Static inspection, coding, synthetic checks and live interface checks are distinct scopes; none is automatically authorized by this roadmap. | Gate 3's required receipt and the relevant Gate 2 separation evidence are satisfied; estimator errors support a stated operating range. Otherwise repair within scope or stop. |
| **3. Experiment design** | A justified measurement route and explicit permission for a design round. No target-outcome selection. | Specify selection, controls, outcomes, costs, preregistration and custody. Gate 4 implementation/smoke tests need authorized scope and may require a return to Phase 2. No target run. | All six gates demonstrably pass; preregistration is frozen/hashed and verified; explicit run authorization is obtained separately. |
| **4. Execution and decision** | All six gates pass, frozen package verified, and explicit authorization binds the exact bounded run. | Execute only that run; retain receipts; apply the frozen outcome map; stop on its budget/failure rule. | Report the authorized result and stop. Any extension requires new prospective authorization. |

Phases are not a permission ladder: finishing a round or entering a phase does not grant its listed capabilities. Preparatory work may cross phases when separately authorized; the gates below remain the approval criteria. E0 is not Phase 0 or an E1 prerequisite run.

## 4. Existing six gates, unchanged

The following pass conditions are transcribed from the [governing review, §7](https://docs.google.com/document/d/1kKgrebodatjIedFp_sCiJ43C8vhKQPEZ-1jaV57usDM/edit?tab=t.0). The placement column is organization only.

| Existing gate / receipt | Governing pass condition | Proposed phase placement |
|---|---|---|
| **1 · Derivation** / Paper-to-observable note | Every E1 quantity has a directional prediction traced to the construction, plus a stated break in the analogy. | Phase 1; unresolved cross-phase evidence is not waived. |
| **2 · Estimand separation** / E0/E1 boundary note | E1 has separate files, code path, outputs, hypothesis, and hash; no E0 threshold or frozen field changes. | Starts in Phase 1; demonstrable implementation separation in Phase 2; final package in Phase 3. Two review files alone do not pass it. |
| **3 · Data feasibility** / Cadence / field / resolution receipt | The chosen dataset exposes the fields, temporal cadence, spatial neighborhood, and argmax tracking needed for every primary observable. | Phase 2. |
| **4 · Controls** / Executable control plan | Random-anchor and time-mirror controls are implemented and smoke-tested without inspecting target-event outcomes. | Scientific specification in Phase 3; authorized implementation/verification work in Phase 2 or a bounded return to it. |
| **5 · Outcome map** / Frozen decision table | Supporting, nonsupporting, null/underpowered, and implementation-failure outcomes are distinguished before results. | Phase 3, applied in Phase 4. |
| **6 · Custody and stop** / Manifest + hashes + mandatory stop | Code, source paper version, dataset identity, selected windows, thresholds, receipts, retry rules, and stop-after-pilot are frozen. | Phase 3, enforced in Phase 4. |

The governing sequence after all six gates pass remains: freeze and hash E1 preregistration; verify its hash; obtain explicit run authorization; execute the smallest pilot; stop before extension. No gate is renumbered, declared passed, or removed here.

## 5. Scope drift and unresolved governance tensions

**Observed scope drift.** R2 combined two questions: whether the operator measures the source geometry at all, and whether a particular DNS/API resolves it. Its §7 classified both source inheritance and a native-DNS-compatible finite-scale envelope as fatal to Gate 1. The governing review separately places cadence/field/resolution evidence in Gate 3. The R2 assignment explicitly requested that combined closure attempt; its receipt was not an unauthorized excursion, but the combined scope obscures which question should be answered next.

**Proposed separation, not an amendment:** keep generic identifiability, source-field contamination and mathematical error dependencies in Phase 1; place concrete grid/cadence/client constants and verified operating range in Phase 2/Gate 3. Retain a cross-reference wherever a Gate 1 claim depends on Phase 2 evidence. Do not retroactively erase R2's blockers or mark Gate 1 passed by relabeling them. Any change to approval requirements needs an explicit later governing decision, not this map.

Two additional tensions are preserved for later review:

1. Gate 3 explicitly mentions argmax tracking, while the reduced primary uses a centroid and does not track argmax as a particle. The reduced design does not automatically satisfy that wording. A later receipt must address the stated requirement or obtain an explicit governing revision.
2. Gate 4 explicitly requires random-anchor and time-mirror controls. v0.1 warns that mirrored trend reversal is not independent mechanism evidence. That scientific warning does not waive implementation/smoke-test requirements or authorize redesign now.

The earlier README contains runnable legacy examples below an explicit superseded/not-authorized warning. The warning governs. The draft GetData amendment and H2 declaration schema do not replace the frozen E0 protocol or grant execution authority.

## 6. Stop and one recommended next round

**Recommended R4, not started:** “Can the paper's source-field bounds establish a noncircular bound on the zeroth and second moments of contamination for the unchanged relative-threshold operator?” Limit work to the existing source and restriction 2 in the audit. The output would be one analytical receipt with either a sufficient bound and explicit remaining assumptions, or a failure to justify this restriction. Do not fit a DNS profile, tune α, choose windows, code an estimator, or expand the candidate search.

R4 requires **new explicit authorization for that bounded analytical round and its document**, because this assignment ends after the map and R3. It requires no live data, simulation or run authorization. No authorizations are bundled into this recommendation.

## 7. Completion state

All 22 pre-existing tracked files and both derivation receipts retain their entry hashes. The only additions in this circuit are this map and the companion audit. Tracked diff is empty. Actual short status with all untracked files is:

```text
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.1.md
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.2.md
?? docs/e1-openai/NS-001_E1_OPERATOR_CONFOUNDING_AUDIT_v0.1.md
?? docs/e1-openai/NS-001_E1_WORKFLOW_MAP_v0.1.md
```

The two derivation receipts were already untracked at entry; the map and audit are new this round. No commit or push. This circuit is closed.

E0: FROZEN / HOLD.

Gate 1: PARTIAL.

Run authorization: NOT GRANTED.
