# NS-001 — E0 Stride Refinement Pre-Registration

**Status:** FROZEN before E0 execution  
**Freeze date:** 2026-09-02  
**Experiment:** E0 — single-frame instrument characterization  
**Execution condition:** Operative only after the file’s SHA-256 sidecar verifies successfully.

Before this freeze, only the earlier public-token access test and the eight-point authorization sanity check had run. E0 has not run. No `hat M_s` values have been observed. No 32³ volume has been pulled.

---

## 1. Purpose

E0 measures how much peak vorticity is lost when the full domain is sampled on progressively finer spatial lattices.

This is an instrument-characterization experiment, not a blowup experiment or a temporal extreme-value analysis. Its result determines whether a sparse whole-domain temporal route remains technically plausible.

E0 cannot establish or exclude Navier–Stokes blowup.

## 2. Observables

| Symbol | Definition | Status |
|---|---|---|
| `M_Ω(t)` | Continuum maximum of `||ω(x,t)||` over the complete domain `Ω` | Scientific target; not directly obtainable |
| `hat M_s(t)` | Maximum reconstructed vorticity magnitude returned at the on-grid points of the full-domain stride-`s` lattice | E0 observable |
| `M_V(t)` | Maximum vorticity magnitude over one fixed subvolume `V` | Separate local proxy; not measured in E0 |

For every stride, `hat M_s` is a sampled lower bound on `M_Ω`. No E0 result may be reported as a direct measurement of `M_Ω`.

Because the lattices are exactly nested, the required implementation invariant is:

`hat M_16 <= hat M_8 <= hat M_4`

Any violation is an implementation or data-handling failure and terminates E0 without interpretation.

## 3. Dataset

| Quantity | Frozen value |
|---|---|
| Dataset | `isotropic1024coarse` |
| Simulation | Forced, statistically stationary isotropic DNS |
| Domain | `[0, 2π)^3` |
| Native grid | `1024³` |
| Queryable time window | `[0, 10.056]` |
| Stored cadence | `0.002` |
| E0 frame | `t = 5.028` |
| Frame-selection rule | Exact temporal midpoint, selected before observing E0 values |
| Large-eddy time `T_L` | approximately `1.99` |
| Record span | approximately `5.05 T_L` |
| Kolmogorov time `τ_η` | approximately `0.0424` |
| Full-record `R_λ` | approximately `418` |
| Early-segment `R_λ` | approximately `433` |
| Reference Kolmogorov length `η_ref` | `0.00280` |
| Native spacing `Δx` | `2π/1024 ≈ 0.006135923 ≈ 2.19 η_ref` |
| Kinematic viscosity `ν` | `0.000185` |

The full-record value `η_ref = 0.00280` is used consistently for the E0 spacing ratios. The early-segment value near `0.00287` is not used in those ratios.

## 4. Frozen lattice geometry

For stride `s`, define the native-grid index set:

`I_s = {0, s, 2s, ..., 1024-s}`

and the lattice:

`L_s = {(iΔx, jΔx, kΔx) : i, j, k ∈ I_s}`

Frozen choices:

- strides execute in the order `16 → 8 → 4`;
- origin is `(0,0,0)`;
- all coordinates are native-grid coordinates;
- all three lattices span the complete periodic domain;
- the lattices are exactly nested;
- no translated origins or alternative frames may be added after results are observed.

## 5. Frozen query operator

| Field | Frozen choice |
|---|---|
| SOAP operation | `GetVelocityGradient` |
| Spatial differentiation | `None_Fd8` |
| Giverny-equivalent label | `fd8noint` |
| Temporal interpolation | `None` |
| Frame | `t = 5.028` |
| Execution | Sequential only; no concurrent requests |

The returned velocity-gradient components are interpreted in this order:

`du/dx, du/dy, du/dz, dv/dx, dv/dy, dv/dz, dw/dx, dw/dy, dw/dz`

Vorticity is reconstructed as:

`ω_x = dw/dy - dv/dz`

`ω_y = du/dz - dw/dx`

`ω_z = dv/dx - du/dy`

and:

`||ω|| = sqrt(ω_x² + ω_y² + ω_z²)`

For each stride:

`hat M_s = max_{x ∈ L_s} ||ω(x, 5.028)||`

The execution code must verify the SOAP response-field ordering against the service schema before calculating vorticity. A mismatch or ambiguity terminates the run.

## 6. Ladder and deterministic partitions

The service limit is treated as 2,000,000 points per request.

Points are flattened deterministically with the `i` index varying fastest, followed by `j`, then `k`. Each request receives the next contiguous, non-overlapping slice of that ordering.

| Stride | Points | Spacing / `η_ref` | Frozen partitions | Queries |
|---|---:|---:|---|---:|
| 16 | 262,144 | 35.1 | `262,144` | 1 |
| 8 | 2,097,152 | 17.5 | `2,000,000 + 97,152` | 2 |
| 4 | 16,777,216 | 8.8 | eight requests of `2,000,000`, then `777,216` | 9 |

Total: 12 sequential E0 queries.

Each partition must be fully received, validated, reduced to its partition maximum, and receipted before the next request begins.

No partition may overlap another. The union of the partitions must equal the complete lattice exactly.

An identical request may be retried at most twice following a transport or server failure. Retries must retain the same payload and be recorded. Returned numerical values are never grounds for a retry.

## 7. Output paths and receipts

The execution root is:

`/workspace/ns-001/e0/`

Required files:

- `/workspace/ns-001/e0/PREREGISTRATION.md`
- `/workspace/ns-001/e0/PREREGISTRATION.sha256`
- `/workspace/ns-001/e0/e0_query.py`
- `/workspace/ns-001/e0/execution_manifest.json`
- `/workspace/ns-001/e0/partition_receipts.jsonl`
- `/workspace/ns-001/e0/e0_results.json`
- `/workspace/ns-001/e0/E0_REPORT.md`
- `/workspace/ns-001/e0/SHA256SUMS.txt`

Each partition receipt must record:

- preregistration SHA-256;
- code SHA-256;
- dataset and frame;
- stride;
- partition number;
- first and final flattened index;
- requested and returned point counts;
- operator and interpolation settings;
- partition maximum;
- start and finish timestamps;
- retry count;
- success or failure status.

The authorization token must never appear in scripts, manifests, logs, reports, results, hashes, or `/workspace`.

## 8. Prospective prediction

Vorticity extrema are dissipative-scale objects. Every E0 lattice remains substantially coarser than `η_ref`, while the native DNS grid itself has spacing approximately `2.19 η_ref`.

**Predicted outcome:** `hat M_s` will still be climbing materially at stride 4.

Flattening by stride 4 would be a genuine surprise. It would require explanation before any temporal work could be considered.

## 9. Primary quantities

The refinement ratios are:

`r(16) = hat M_8 / hat M_16`

`r(8) = hat M_4 / hat M_8`

The decision quantity is `r(8)`.

For descriptive purposes only, report:

`α(16) = log₂(r(16))`

`α(8) = log₂(r(8))`

These are two interval-specific effective exponents, not an asymptotic scaling law. With only three lattice spacings, E0 will not report a formal fitted slope, slope uncertainty, convergence order, or extrapolated continuum maximum.

Plot `hat M_s` against physical lattice spacing on log-log axes.

## 10. Frozen decision rule

| Observation | Required action |
|---|---|
| `r(8) > 1.03` | Sparse whole-domain temporal route is rejected. Freeze the coarse-net limitation with `r(16)`, `r(8)`, `α(16)`, and `α(8)` attached. Any dense local-prism study requires separate authorization. |
| `r(8) <= 1.03` | Stop after E0 and explain the unexpected flattening. This does not automatically authorize a temporal sweep; costs and interpretation require a separate decision. |
| Nested-lattice monotonicity fails | Declare implementation failure. Do not interpret the values. |
| Missing, malformed, nonfinite, or ambiguously ordered gradient data | Halt and audit. Do not substitute or silently discard values. |

No decision threshold may be revised after observing E0.

## 11. Mandatory stop

After the 12 planned queries—or immediately following any terminal failure—Terby must stop.

E0 authorization does not authorize:

- another frame;
- another lattice origin;
- a temporal sweep;
- the 32³ local prism;
- a full-field cutout;
- a cross-`R_λ` comparison;
- spatial block-maxima EVT;
- fitting `ξ`;
- rerunning E0 because its result is inconvenient.

Terby returns the manifest, receipts, results, report, and hashes. Any subsequent experiment requires a new prospective authorization.

## 12. Instrument limits

Three nested limitations remain:

1. the E0 sampling lattice, measured here;
2. JHTDB access limits and targeted-subset policy;
3. the native DNS grid, approximately `2.19 η_ref`.

E0 characterizes only the first limitation. It cannot repair or remove the other two.

## 13. Standing scientific caveats

### Governor

The dataset is forced and statistically stationary. It cannot resolve the intrinsic unforced Navier–Stokes question. A bounded observed tail may reflect the forcing or finite numerical system.

### Estimand separation

Temporal EVT of a time series of maxima and spatial block maxima within one snapshot are different estimands. Results from the higher-`R_λ` single-snapshot datasets may not be substituted into a temporal fit.

### Local-volume separation

The 32³ fixed volume has side length approximately `0.14L`. Its maximum is `M_V`, not `M_Ω` or `hat M_s`. It is not part of E0.

### Native-grid limitation

The source DNS was designed for turbulence analysis, not continuum extreme recovery. Even a converged E0 lattice cannot establish convergence beyond the native DNS grid.

### Novelty

The prior-art audit remains unresolved, including Yeung et al. on this dataset and the Nemoto, Alexakis, Seshasayanan, and Tsuzuki lines of work. E0 does not establish novelty.

## 14. Acceptable negative result

If accessible JHTDB data cannot support an informative temporal tail-shape estimate, the acceptable output is an honest instrument and information-limit characterization:

*Here is what the accessible JHTDB spatial and temporal information can and cannot support about sampled vorticity-extreme behavior.*

That is a valid result. It is not evidence for or against finite-time blowup.
