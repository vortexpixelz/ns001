# NS-001 / E1–OpenAI Gate 1 Derivation Receipt v0.1

Review date: 16 September 2026. Scientific-design review only. E0 remains frozen and on HOLD. This document is separate from the governing v0.2 review and is neither an E1 preregistration nor an execution authorization.

## 1. Executive verdict

**PARTIAL.** A conditional, falsifiable test of **leading-core kinematic resemblance** can be derived. A mechanism-specific test of the completed construction is not yet operationally justified. No observable is promoted to an executable primary endpoint in this receipt.

The smallest defensible candidate family is a colocated velocity amplitude and a three-dimensional core-width tensor, reduced to radial width, axial width, and their ratio. Its validity depends on identifying the same core through time, resolving it, and proving that the chosen segmentation recovers the paper's similarity region. These conditions are unresolved. Global vorticity maxima, generic scale lead–lag, and visual slenderness cannot substitute for them. The stress-correction mechanism requires substantially more than these kinematics.

The governing review's proposed joint signature therefore needs narrowing. A positive result could support finite-window resemblance to the leading geometry; it would not identify the special forcing, reconstruct the pulse covariance, establish a singularity, empirically validate the theorem, or show that stationary turbulence follows this construction. A negative result could reject a prespecified resemblance signature in the sampled population, not the theorem.

**Scope and custody.** The complete governing review, including its galaxy addendum, was read first [G]. Repository documentation and the complete frozen E0 preregistration were then read. No target-event results, empirical arrays, simulations, experiment runners, or JHTDB data-query endpoints were used. Public paper and interface documentation were retrieved. No tests were executed. SPARC/S₃ remains a governance precedent only; its physical claims were neither adopted nor investigated.

The live local repository was clean at entry, on `codex/e0-h2-preparation`, HEAD `711b6c7f0cfd1c69694bff8a3fd134b585e633df`. The frozen preregistration's recomputed SHA-256 matched its sidecar:

`a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`.

The paper PDF retrieved through the official announcement has 166 pages and SHA-256:

`0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.

This is a source-specific design audit, not an independent proof verification or Lean audit. Paper page references below are printed pages, which match PDF page numbers when counted from one. Repository statements refer to the inspected local commit, not an independently refreshed remote branch.

## 2. Mechanism reconstruction and mathematical bridge

### Source premises

Theorem 1.1 states forced, finite-energy velocity blowup from rest; the final field has fixed compact support. Its concentrating core is a different object. Sections 2.1 and 3.1 give radial scale τ^(1/2), axial scale τ^(1/2−h), and tangential speed τ^(−1/2−h), with τ=1−t and 0<h<0.01. Theorem 3.1(iv), equation (3.6), preserves growth along an inner path in the completed field. [P, pp. 1, 3–8, 16]

Background momentum balance alone fails in an annulus. Two amplified pulse families supply a prescribed mean stress; successive corrections make the residual smoothly extendible. The relevant covariance averages include an auxiliary torus before physical evaluation. Small external seeds initiate pulses; shear amplifies them before viscous decay. Spatial localization and startup are also part of the designed force. [P, §2.2 p. 6; §§3.2–3.5, pp. 9–17; Proposition 7.5; equation (7.22); Proposition 9.9; Lemma 10.3]

### Receipt derivation D1: geometry is Eulerian, not material

Write a leading-core representation schematically as

`x = c + R diag(lr, lr, lz) y`, with `lr ∝ τ^(1/2)`, `lz ∝ τ^(1/2−h)`.

Here `c` is the concentration center, `R` a fixed spatial rotation, and `y` ranges over a fixed similarity region. In the paper that region is expressed using `(X, η)`, not an arbitrary box or threshold set [P, §3.1, p. 8; equations (3.2), (4.1)–(4.3)]. The schematic coordinate change is a bridge assumption for the proposed estimator, not an assertion that every velocity component has an identical separable profile.

An Eulerian high-intensity region can contract in all directions while fluid exits axially. Incompressibility instead preserves the volume of a transported material region. Thus **axial outflow does not predict increasing axial core width**. Both widths must contract for this particular resemblance hypothesis. A Lagrangian particle cloud's volume is the wrong observable.

The complete field's support need not shrink. A fixed spatial cutoff and an exterior coexist with a concentrating core. A shrinking threshold volume is at most a proxy for that core, never a measurement of the support of the whole solution.

### Receipt derivation D2: when a width tensor would inherit the scaling

Let `Cα(t)` be one identified connected core, selected using a fixed fraction `α∈(0,1)` of a **local** amplitude `Uc(t)` in a prospectively fixed search neighborhood. Define, using unwrapped periodic coordinates,

`w(x,t)=|u(x,t)|² 1{x∈Cα(t)}`,

`c_w = Σ w x / Σ w`,

`Q = Σ w (x−c_w)(x−c_w)^T / Σ w`.

The tensor is centered at its weighted centroid, not at a single argmax point. A swirl maximum can lie on a ring; centering moments on one member of that ring would create spurious asymmetry. The argmax may initialize component selection but is not the core axis or a material tracer.

**Conditional inference:** if, in similarity coordinates, `Cα` and normalized weights approach a fixed, bounded, nondegenerate axisymmetric shape, the common velocity-amplitude factor cancels in `Q`. Then two transverse eigenvalues scale as `lr²`, and the axial eigenvalue as `lz²`. The condition is load-bearing: the paper's designated inner similarity region is not proved here to equal a component of a fixed speed superlevel set of the completed field.

After the axis is identifiable, define `lr_hat=(λr1 λr2)^(1/4)`, `lz_hat=λz^(1/2)`, and `rho_hat=lr_hat/lz_hat`. Axial assignment must use a frozen identification rule and an eigengap adequacy check. Blindly calling the largest eigenvalue “axial” before that check is unjustified. Sign-free axial orientation uses `|e_z(t)·e_z(t0)|`; the two radial eigenvectors are indeterminate in an axisymmetric cross-section.

For an adequate estimator, the candidate directions are `Uc ↑`, `lr_hat ↓`, `lz_hat ↓`, `rho_hat ↓`. These concern net trends in a predeclared window, not strict pointwise monotonicity of the complete solution at every frame. Neither bounded-comparability notation nor a leading asymptotic alone licenses a universal finite-window monotonicity claim.

### Receipt derivation D3: vorticity, with the missing distinction retained

For an axisymmetric leading field,

`ωr=−∂z uθ`, `ωθ=∂z ur−∂r uz`, `ωz=(1/r)∂r(r uθ)`.

Applying the spatial scales to equation (4.3) gives characteristic inner-profile orders `ωr=O(τ^−1)` and radial-derivative contributions of order `τ^(−1−h)` to `ωθ` and `ωz`, where the relevant profile derivatives are nonzero. These are component/profile estimates, not a formula for the global maximum of the completed field. Cancellation, a vanishing coefficient, and pulse gradients must be kept separate.

A stronger but still limited inference is possible from circulation. In the inner axisymmetric region, annular corrections vanish and the growth relation holds on the circle `rτ=√(2 Xin τ), z=0` [P, equation (3.6); Proposition 9.9, Step 5, p. 116; equations (10.20)–(10.21)]. Stokes' theorem gives

`(π rτ²)^−1 ∫disk ωz dS = 2 uθ(rτ,0,t)/rτ ≍ τ^(−1−h)`.

Consequently the maximum vorticity magnitude somewhere on that disk, and hence globally, is at least this large asymptotically. **This receipt's inference establishes a lower bound, not equality, a shared argmax, a finite-window trend, or a velocity–vorticity lead–lag.** It does not require importing an unforced BKM statement into a forced problem.

For the annular waves, dividing the characteristic wave amplitude by its wavelength gives the same nominal derivative order `q^(−1−h)` before logarithmic/support factors [P, §3.3, p. 11; §7.2, p. 81]. Thus a perturbation small in velocity need not be negligible in vorticity. An extreme-vorticity anchor may select the annulus or another DNS structure rather than the inner velocity core.

### Receipt derivation D4: finite-window identifiability

Eliminating τ from the leading scale relations yields conditional diagnostics:

`Uc ∝ lr^(−1−2h)`, `lz ∝ lr^(1−2h)`, `rho ∝ lr^(2h)`.

These are possible analytical consistency checks after an estimator bridge exists; they are not fitted laws or extra primary endpoints here. A fitted terminal time is unnecessary for a directional test and must not be selected after seeing an event.

If remaining time decreases by a factor `S>1`, radial-to-axial width ratio changes by `S^−h`, and its squared-eigenvalue counterpart by `S^−2h`. Even at the upper bound on h, `S=100` produces less than about a 4.5% width-ratio decrease, while the radial scale contracts tenfold. There is no positive lower bound on h supplied for a DNS design. A visibly large increase in elongation over a short window is therefore not automatically closer to the construction.

For width-ratio log-error allowance `εrho`, a necessary design condition is `h log S > εrho`. For spatial adequacy require `lr_min/Δx ≥ nr`, `lz_min/Δx ≥ nz`, with `nr,nz` established by an estimator-error receipt, not invented as theorem constants. For temporal adequacy require stored `δt` much smaller than both amplitude and width change times and, if studied, pulse lifetime. Define those times prospectively through bounds on `|d log Uc/dt|`, `|d log lr/dt|`, and `|d log lz/dt|`.

No universal physical window length follows from the normalized terminal time 1. Rescaling and unknown event scales prevent translating it into “N JHTDB frames” without additional choices. Cadence adequacy cannot be established using a mean Kolmogorov time alone.

## 3. Complete source-to-observable tables

The following two tables are one joined specification, keyed by ID. Every candidate has a source/quantity/direction entry and a fields/neighborhood/cadence/resolution/confounder/break entry. “No prediction” is a rejection or unresolved derivation, not permission to select a favorable direction later. Paper locators reference [P]. All DNS estimators below are proposals, not implemented measurements.

### 3A. Construction, quantity, estimator, and direction

| ID / disposition | Construction feature and exact source | Mathematical quantity | Proposed DNS estimator | Predicted direction or absence |
|---|---|---|---|---|
| O1 / replace global with conditional local candidate | Inner speed growth: §3.1 p. 8; Theorem 3.1(iv), (3.6) p. 16; (10.21) p. 124 | `A(t)=supΩ |u|`; separate `Uc=supC |u|` | Native-sample local speed maximum in the same tracked component; global sampled maximum only if domain coverage is actually obtained | `Uc` rises under D2; theorem guarantees asymptotic unbounded global speed, not every finite-frame increment |
| O2 / secondary only | Curl of (4.3), (4.2); inner-circle growth (3.6); pulse derivative caveat §3.3 p. 11 | `M=supΩ |curl u|`; disk-mean axial curl in D3 | Curl from a verified nine-component gradient; distinguish global sampled maximum from local maximum and circulation-based average | Asymptotic lower bound in D3; no source-derived universal finite-window direction of global `M`, or lead–lag relative to `A` |
| O3 / tracking metadata | Fixed origin and shrinking growth circle: §2.1 p. 3; (10.20) p. 124 | Set-valued `argmax`, component identity, center trajectory | Deterministic tie policy; periodic connected-component labels; unwrapped centroid and retained wrapped coordinates | Same structure should remain identifiable; no predicted DNS center speed, no requirement that argmax be a fluid trajectory |
| O4 / conditional primary candidate | Similarity core: §3.1 p. 8; (3.2), (4.1)–(4.3) | Weighted covariance `Q`; `lr,lz` | Tensor D2 over one complete, nontruncated component | Both radial and axial widths decrease if D2 assumptions hold |
| O5 / derived part of O4, not independent endpoint | Unequal contraction rates: §2.1 p. 4; §3.1 p. 8 | `rho=lr/lz`; transverse/axial eigenvalue ratio | `rho_hat` or its square, declared in advance; not both counted as independent evidence | Decrease; transverse equality only an ideal axisymmetry check; slow effect D4 |
| O6 / reject as primary | Core volume versus fixed final support: §2.1 p. 4; §3.1 p. 8; Proposition 10.1 | Global `Vα=vol{|u|≥α A}` versus local component volume | Count voxels in a declared superlevel set; preserve distinction between whole-domain and one component | Contraction only if the chosen level set follows the similarity core; global frame-normalized volume has no necessary finite-window direction |
| O7 / quality/supporting check | Leading fixed axis: §2.1 pp. 3–4; §3.1 p. 7; nonaxisymmetric waves §3.3 | Axial projector `ez ez^T` | Sign-free axial alignment after eigengap check | Stability in the fixed-frame leading-profile limit; not a theorem about total-field DNS orientation |
| O8 / reject generic lead–lag; retain research question | Waves on finer scales: §3.3 pp. 11–12; dyadic charts (6.1)–(6.6) pp. 62–63; pulse (7.21)–(7.22) pp. 80–81 | Wave amplitude, wavevector, local shear production and damping | Would require spatially localized, directional band analysis and pulse identity; generic band-energy cross-correlation is insufficient | Individual pulse growth then decay and shortening radial wavelength; no derived universal coarse-band/fine-band lag or shell-energy ordering |
| O9 / proposed comparator | No theorem prediction; review §6 control proposal [G], evaluated against O1–O5 | Conditional distribution of joint trends at matched anchors | Disjoint random windows matched on anchor speed and prespecified nuisance variables | No theorem-derived effect size; “events exceed controls” is a new statistical hypothesis requiring separate preregistration |
| O10 / diagnostic, not primary null | No time-reversal claim in paper; dissipative pulse equation (7.22) | Same estimator on reversed time indices | Reverse stored sequence without reselecting anchor or redefining its peak | Trend signs reverse algebraically; superiority to a mirrored window is not independent evidence |
| O11 / reject from minimal design | No phase-randomized null in paper; covariance dependence §3.3 and Proposition 7.5 | Fourier amplitudes versus phase-dependent localization | Common phase rotation of the vector coefficient at each wavevector; conjugate phases at `−k`; retain zero mode | Spectrum preserved by construction, but no predicted DNS significance, marginal preservation, or dynamically valid time ordering |
| O12 / mechanism bridge unresolved | Annular residual and two fluxes: §3.2 pp. 9–10; §3.3 pp. 11–12; (7.24)–(7.26), Proposition 7.5 pp. 82–83; (9.11) | Background residual plus divergence of pulse covariance | Would require a justified background/wave separation, cylindrical stress components, and a residual budget | Leading pulse-stress divergence opposes background residual; generic positive transfer or a broadband burst is insufficient |

### 3B. Measurement requirements and explicit failure of analogy

`W` denotes a prespecified physical window and `δt` actual stored cadence. D4's inequalities are the minimum requirements; numerical W, shape-error tolerances, and adequate sample counts are unresolved. No interpolation creates missing time information.

| ID | Necessary fields | Spatial neighborhood | Cadence and window requirement | Resolution sensitivity | Principal confounders | Explicit point where analogy fails |
|---|---|---|---|---|---|---|
| O1 | Three velocity components in a fixed declared frame | Full domain for global A; tracked core plus exterior margin for Uc | W must contain a resolvable net rise in the same component; δt ≪ amplitude change time | Missed off-grid peaks; spatial interpolation bias | Bulk sweeping, Galilean frame, switching maxima, conditioning on a peak | Local maximum called global; changing frame or component to manufacture growth |
| O2 | Nine ordered velocity derivatives, or adequately padded raw velocity; velocity on a loop for circulation check | Whole domain for global M; inner disk/loop plus core and annulus for comparison | δt must resolve curl changes, potentially faster than O1; no justified fixed W yet | Differentiation amplifies short scales; pulses may be unresolved | Strain/shear layers, unrelated vortex tubes, cancellation, FD versus spectral derivative | Assigning the global maximum the inner-profile exponent or assuming it is colocated with A |
| O3 | Velocity, sample coordinates, timestamps, component labels | Core plus search margin; periodic connectivity | Interframe travel must be below the unambiguous association range; W cannot silently bridge splits | Grid ties and unresolved maxima cause jumps | Equal maxima around rings; births/mergers; boundary crossings | Treating argmax jumps as fluid acceleration or losing identity across a wrap |
| O4 | Dense three-component velocity | Entire selected core and outside margin; no contact with crop boundary | W must resolve contraction in both dimensions; δt ≪ both contraction times | Width bias near grid scale; threshold connectivity; truncation | Background velocity, multiple cores, ring bias, threshold erosion | Selected high-speed component does not map to a nondegenerate similarity region |
| O5 | O4 tensor, axis assignment and errors | Same O4 region | W must yield `h log S` above ratio error; same actual frames as O1/O4 | Tiny anisotropy change may be below tensor error even when widths are resolved | Eigenvalue crossing; isotropic or sheet-like structures | Calling any slender object the required increasingly slender contracting core |
| O6 | Velocity magnitude; global A if global normalization used | All superlevel components for global volume, or explicitly local component | Same W and δt as geometry; constant α | Voxel quantization and moving threshold dominate small sets | Rising threshold alone removes stationary background; disjoint peaks | Threshold-volume loss interpreted as material compression or total-support shrinkage |
| O7 | O4 tensor | Same complete component | Same W; enough frames to distinguish a stable axis from association errors | Orientation ill-conditioned when eigengap is small | Rigid rotation, sweeping, degenerate radial eigenvectors | Radial basis rotation or sign flips classified as physical instability |
| O8 | Dense vector velocity; gradients; pressure/force if a transfer budget is claimed | Complete annulus and filter padding, not a peak alone | δt ≪ pulse growth/decay duration, not merely core lifetime; W spans identifiable pulses | Wavelength can be much smaller than core; derivative/filter errors | Ordinary cascade, sweeping, filter leakage, overlapping structures | A band correlation is substituted for the arranged covariance or assumed to reveal causal transfer |
| O9 | Same fields as primary, anchor covariates | Identical coverage and geometry for events and controls | Same W/δt; nonoverlap or dependence model; independent anchors adequate for desired precision | Must match sampling error as well as amplitude | Regression to mean, peak-selection bias, overlap, unequal baseline geometry | Arbitrary random times compared to selected peaks and called mechanism specificity |
| O10 | Already obtained window fields; no new physics | Identical region sequence and tracking treatment | Exact same W and frames, reversed; cannot count as an independent sample | Same as parent window | Irreversibility common to turbulence; algebraic sign reversal | A guaranteed change of score sign becomes a statistical discovery |
| O11 | Full periodic vector velocity for each selected frame | Whole periodic domain for exact global spectral preservation | A prospective across-time phase rule is required; independent phases destroy temporal coherence, fixed phases preserve more of it | Cropped windows and discrete derivatives complicate spectral claims | Altered one-point distribution, loss of nonlinear dynamics | Claiming spectrum preservation also preserves amplitude marginals, extremes, or Navier–Stokes evolution |
| O12 | Velocity, time derivative, gradients/Laplacian, pressure gradient; force for closure | Inner core, full annulus, exterior, derivative and averaging support | δt and W must resolve wave stresses and residual terms simultaneously | Cancellation of large terms is especially error-sensitive | Arbitrary filtering, unobserved forces, finite difference residual | Identifying a DNS spatial/filter average with the proof's auxiliary-torus average without a derivation |

## 4. Minimal recommended primary family

**Conditional design candidate only:** `(Uc(t), Q(t))`, reduced to `(Uc, lr_hat, lz_hat, rho_hat)` on one prospectively selected and tracked core. This is two measurement objects, not four independent pieces of evidence. Test a joint conjunction of directional changes, retaining each component and its uncertainty; do not let one strong trend compensate for failure of another in an unrestricted sum score.

Use the DNS laboratory frame as the explicit initial convention. Raw speed is frame-dependent. Subtracting a time-varying local mean might reduce sweeping but would change the estimand and introduce another moving-background definition; it requires a separate derivation. Retain background contamination as an exclusion/adequacy issue until that decision is frozen.

No global-max search or target-window selection is approved. The E1 event population, anchor definition, α, connectivity, crop dimensions, tracking rule, axis assignment, window length, trend estimator, error allowance, and dependence treatment must be specified separately. Selecting rising speed as an eligibility criterion cannot then be counted as independent evidence for rising speed. E0's single-frame strides and 1.03 threshold provide none of these choices.

**Promotion decision:** withheld. Velocity fields are documented, but core-identification validity and adequate spatial/temporal resolving power are not demonstrated. This candidate could become a limited resemblance test; it cannot yet be labelled a completed mechanism test.

## 5. Rejected or demoted candidates

- **Global A and M as co-primary scalars:** missing colocation and identity; global coverage is not established; M is particularly sensitive to annular waves. Keep distinct sampled/local names if subsequently obtained.
- **Global frame-fraction concentration volume:** moving threshold and disconnected structures can manufacture contraction. Even a valid local version is substantially redundant with the width tensor and more threshold-sensitive.
- **Aspect ratios as extra independent outcomes:** derived from the same tensor. Preserve their diagnostic role without multiplying evidence counts.
- **Stable radial eigenvectors:** mathematically unidentifiable in an axisymmetric cross-section. Only an adequately separated axial projector has meaning.
- **Generic ordered multiscale amplification:** the paper's scale arrangement is not a universal lag theorem for DNS Fourier-band energies. Do not promote a free choice of bands or lag signs.
- **Time mirror as a significance null:** trend reversal is largely built in. Useful for software/selection diagnosis only, subject to separate authorization for any later check.
- **Spectrum-preserving surrogates:** omitted from the minimal design. They do not automatically preserve speed marginals, extrema, temporal coherence, or governing dynamics, and require expensive complete fields for the stated global spectrum property.
- **Pulse covariance closure:** scientifically closer to the mechanism but currently non-identifiable from an arbitrary DNS filter. Retain as an unresolved bridge, not as a surrogate positive finding.
- **EVT shape, fitted terminal time, continuum blowup exponent, or event frequency:** no justified prediction supplied by this paper-to-estimator derivation. None becomes an E1 endpoint here.

## 6. Directional predictions with paired failure conditions

“Necessary” below means necessary for the specifically defined leading-core resemblance model under an adequate estimator, not necessary for every Navier–Stokes extreme event. Finite-window signs remain a proposed hypothesis; asymptotic statements alone do not force them in every preterminal interval.

| Class | Candidate prediction | Paired failure condition / interpretation |
|---|---|---|
| Necessary to the proposed joint model | Colocated Uc increases over the frozen window | Adequately resolved nonincrease beyond the error allowance rejects that window's joint signature; uncertain slope is null/underpowered |
| Necessary | Both lr and lz decrease | Adequately resolved expansion or noncontraction of either dimension rejects the joint signature; axial outflow is not an excuse |
| Necessary but potentially unresolvable | lr/lz decreases while axis assignment remains valid | A resolved opposite trend is nonsupport; a change smaller than ratio error is null, not evidence of invariance or rejection |
| Necessary measurement condition | The same isolated component remains identifiable | Merger, switching maxima, ambiguous wrapping, or crop truncation makes the window ineligible/unresolved under a frozen rule; a tracking-code defect is implementation failure |
| Supporting, not independent | Near-axisymmetric cross-section and stable axial projector in a fixed frame | Resolved absence limits resemblance; eigengap failure makes orientation undefined, not physically unstable |
| Supporting conditional check | Rescaled profile/width relations in D2–D4 are compatible | Systematic incompatibility with adequate resolution weakens or invalidates the estimator bridge; do not refit the region or exponent to rescue it |
| Mathematical necessity asymptotically, not primary DNS endpoint | D3's inner circulation implies diverging vorticity somewhere on the disk | Failure of a verified analytical derivation on the actual inner field invalidates that bridge; a finite stationary-DNS M plateau does not refute the theorem |
| Mechanism-level, currently unmeasurable as specified | Identified pulses extract shear energy, then damp; their mean stress cancels the required residual | Wrong sign/closure under a justified decomposition would oppose pulse-mechanism resemblance; lack of such a decomposition is unresolved, not a negative data result |
| Generic turbulence only | High vorticity, slender structures, bursts, smaller active scales | Their presence alone supplies no construction-specific support; absence may limit a chosen population but says nothing about the theorem |
| Cannot be inferred | A-to-M lag; shell-energy lag; exact DNS h; universal event rate; EVT tail sign; superiority over controls | No directional test until independently derived and frozen; do not treat an observed sign as a prediction |

Random anchors should be selected under the same eligibility and anchoring convention as events, matched on the declared amplitude covariate, with windows disjoint or their dependence modeled. Matching alone does not remove conditioning on a future peak. A mirrored window is a paired diagnostic, not another independent control event. No expected comparator effect size is derived here.

## 7. Falsification and analogy-break boundary

| Outcome | Prospective interpretation |
|---|---|
| Supporting | All required joint directions pass frozen tolerances in adequate, identity-preserved windows; a separately justified comparator supports an excess over ordinary matched episodes. This supports leading-core resemblance only. Without the comparator, report descriptive compatibility, not specificity. |
| Nonsupporting | Adequate measurements contradict at least one required direction, or a well-powered prespecified comparison excludes the meaningful excess sought. Restrict the conclusion to the declared population, window and resolution. |
| Null / underpowered | Directions/comparator differences remain inside uncertainty, insufficient independent windows exist, the tiny anisotropy effect is undetectable, or native sampling cannot resolve the candidate core. Failure to reject is not mechanism absence. |
| Implementation failure | Wrong component order, missing/nonfinite data, unexpected timestamps, wrong axis units, periodic-coordinate defects, response-count mismatch, corrupt hashes, or failed provenance. Stop before interpretation. A small FD divergence residual alone is not automatically corruption; JHTDB documents derivative inconsistency [J2, p. 4]. |
| Invalid observable bridge | Analytical or separately authorized calibration work shows that the chosen threshold/weight does not recover the similarity core; argmax selection systematically changes structures; the axis is non-identifiable; or the proposed averaging cannot represent the proof's covariance. Redesign or reject the observable before target outcomes, rather than labelling this a physical null. |

The analogy breaks at four distinct transitions: specially engineered smooth forcing → stationary low-wavenumber energy injection; velocity-core geometry → vorticity-selected structures; exact continuum/asymptotic solution → a finite grid and finite time window; and generic extremes → mechanism-specific stress cancellation. A periodic construction in Corollary 10.6 removes a boundary-topology objection only. It does not remove any of those transitions.

The scientific claim ceiling is fixed: **finite-resolution, finite-window resemblance**. No E1 outcome establishes blowup, validates the theorem empirically, settles unforced regularity, or establishes genericity. No E1 outcome changes E0.

## 8. Preliminary read-only data-feasibility matrix

“Demonstrably available” below means explicitly documented by the authoritative provider, not successfully retrieved in this review. “Apparently available but unverified” means the function exists but this proposed path has not been pinned and verified. No credentials were consulted and no data queries were sent.

| Requirement | Evidence / status | Consequence and missing receipt |
|---|---|---|
| Periodic vector velocity | **Demonstrably available in documentation.** Isotropic page describes 1024³ DNS with velocity and pressure [J1]. | Promising for O1/O4; actual client output, units and spatial ordering still need an E1 interface receipt. |
| Native spacing and stored cadence | **Demonstrably documented:** domain 2π cubed, δt=0.002, integration step 0.0002 [J2, p. 1]. | Derived Δx≈0.006135923; δt/τη≈0.0472 using documented mean τη. Neither ratio proves extreme-core or pulse resolution. |
| Exact time index set | **Unknown pending metadata/interface receipt.** Documentation combines 5028 frames with [0,10.056] and δt=0.002 [J1,J2]. | Inclusive arithmetic would yield 5029 timestamps. Do not silently choose an endpoint convention; pin valid indices, padding and returned times. |
| Higher temporal cadence | Fine dataset **documented**, but only t=0.0002–0.0198 [J1]. | Does not supply high cadence around an arbitrary coarse-record event. Such missing stored frames are **unavailable from the documented coarse record**; interpolation is not a remedy. |
| Velocity gradients and curl | Gradient functionality **demonstrably documented** [J3,J4]. Exact proposed GetData extraction **apparently available but unverified** [R2]. | Pin client, request/response layout and differentiation semantics. Do not import the frozen E0 operator into E1 by implication. |
| Component ordering | Legacy C/Fortran examples explicitly show velocity `(ux,uy,uz)` and gradient `(ux,x; ux,y; ux,z; uy,x; uy,y; uy,z; uz,x; uz,y; uz,z)` [J4]. | This supports that interface only. It does not verify an unselected GetData client's nesting, flattening or numerical equivalence. |
| Dense local neighborhood and margin | Gridded cutout service **documented**; actual account/path, boundary assembly and proposed volume budget **unverified** [J5]. | Require coverage, halo, grid-index order, periodic stitching and truncation receipt. Point-query availability does not establish affordable complete cores. |
| Global A/M and global superlevel volume | Raw/point access is documented; complete per-frame domain coverage for this design **unverified** [J3,J5]. | No local crop or sparse net may be renamed global. A global frame has 1024³ points before temporal replication. No query budget is approved. |
| Full-field Fourier surrogate | Fields exist in principle; full-domain repeated-frame access and budget **unverified** [J1,J5]. | Reject from minimum family; local-crop FFT does not preserve the global periodic spectrum. |
| Event-specific width/pulse resolution | **Unknown** without a scale/error bridge; subgrid detail and unstored temporal detail **unavailable**. | Do not promote O4/O5/O8 based on mean turbulence scales. No continuum convergence can be established by densifying samples of one native DNS. |
| Pressure/force/residual closure | Pressure storage and force/derivative functions are documented [J1,J3]; complete colocated residual budget **unverified**. Proof's auxiliary variable is **not a DNS field**. | O12 remains unresolved even if individual fields are obtainable. A physical averaging-equivalence derivation is required. |
| Provenance and transport | Repository H2A0 is declaration-only HOLD [R3]; provider warns of legacy access problems [J6]. | Existing shape-only reports do not prove ordering or executed-byte identity. E1 needs its own source, transport, extraction and receipt chain. |
| Effective event count and power | **Unknown**, deliberately not inspected. | Later prospective population and precision design required; no empirical sufficiency claim follows from record duration. |

Provider provenance distinguishes a mean full-record Reynolds number near 418 from an early-segment value near 433 [J2, pp. 1–2]. This receipt does not adopt an observed target-event statistic from that documentation. Its use is limited to dataset metadata and instrument constraints.

## 9. Proposed evidence-ledger changes

These are proposed changes for a later review revision; the governing v0.2 document is untouched. Do not mechanically increase evidence counts for correlated formulas or repeated source descriptions.

| Ledger | Proposed disposition |
|---|---|
| Supporting | Retain the paper as motivation for a distinct design track. Replace “supplies mechanism-level observables” with “permits conditional leading-core kinematic candidates; estimator and pulse-stress bridges remain unresolved.” Add D1's distinction between Eulerian core contraction and material transport. |
| Supporting | Retain location/identity recording as a measurement requirement, with set-valued argmax and periodic topology caveats. Do not count tracking infrastructure as physical evidence. |
| Nonsupporting | Add fixed total support versus shrinking core; weak finite-window anisotropy; velocity-small but gradient-relevant pulses; laboratory-frame sensitivity; and auxiliary-average versus DNS-filter mismatch. Retain forcing, continuum and genericity barriers. |
| Null / orthogonal | Keep agent counts, formalization-process facts, priority debate and SPARC/S₃ outside physical support. Classify mirrored-score reversal as an algebraic diagnostic, not positive mechanism evidence. |
| Unresolved | Replace the broad “which quantities?” entry with specific D2 segmentation/shape, D3 curl-estimator, D4 resolving-power and O12 averaging receipts. Retain event-count and prior-art questions for later gates; neither is answered by this document. |
| Unresolved | Correct the surrogate aspiration: spectrum preservation does not establish marginal preservation. A joint-preserving null needs its own definition and validation; no such null has been implemented here. |

## 10. Exact missing receipts before Gate 1 can close

1. **Estimator inheritance receipt.** For one fully specified core definition, weight, α, axis rule and frame convention, analytically establish which properties of the completed construction it recovers. Bound contamination from exterior/pulses and cutoff effects, show how ties and periodic centering are handled, and identify nondegeneracy conditions. If that cannot be established, reject the proposed primary geometry. The candidate formulas in this receipt do not complete that proof.
2. **Finite-window prediction receipt.** Specify a bounded resemblance hypothesis with window, trend functional and failure tolerances justified before target data. Distinguish asymptotic comparability from finite-window signs. Show a detectability bound for the permitted h/effect range and explicit native-grid/cadence limits; supply no fitted terminal time or outcome-chosen window. If all admissible effects are below resolving power, close the design negatively rather than promising a pilot.
3. **Claim-scope disposition receipt.** Decide explicitly whether E1 tests only leading-core kinematics. If it retains a mechanism-specific claim, derive a physically observable background/pulse decomposition and justify the averaging and stress-cancellation measurement in O12. Generic multiscale lag cannot fill this slot. A kinematic-only scope may reject O12, but must say so in the separate hypothesis and source-to-observable contract.

Before promotion, a minimal metadata/interface receipt must also pin the dataset/time-index identity, velocity/gradient shapes and ordering, grid and periodic assembly, actual stored cadence, neighborhood/halo feasibility, and source/runtime provenance. This overlaps Gate 3 and is not supplied by an eight-point historical shape report. No live receipt is authorized by this document; static authoritative source/schema inspection can precede a separately authorized bounded interface check.

Gate 1 closure would still leave Gates 2–6 separate: E1 namespace and authorization separation; verified access and resolving power; implemented controls; frozen outcome map; and custody/stop package. No source review, repository hash match, or declaration-schema success supplies run authority.

## 11. Next actions, ordered by information value

1. Resolve the analytical core-estimator and claim-scope bridge on paper. If the chosen superlevel geometry cannot inherit the required directions, or mechanism specificity remains essential but O12 is not identifiable, reject this E1 design before acquiring data.
2. Produce a static metadata/interface and resolving-power receipt for the surviving minimal family. Pin the client and time-index convention, then determine whether any defensible finite window can resolve the expected width-ratio change. No JHTDB query is included in this action without separate authorization.
3. Only if those receipts succeed, draft a separate E1 preregistration with prospective population, matched-anchor handling, outcome map, namespace, hashes, budget and stop rule; submit it through the remaining review gates and obtain explicit run authorization before execution.

## 12. Source register

**[G] Governing review.** [NS-001 / E1–OpenAI Evidence Review, living v0.2](https://docs.google.com/document/d/1kKgrebodatjIedFp_sCiJ43C8vhKQPEZ-1jaV57usDM/edit?tab=t.0). Complete readable content inspected, §§1–11 including addendum. Source for operating boundaries, candidate controls and six gates; its technical paraphrases were not treated as primary proof evidence. The retained footer says v0.1; the header and addendum identify v0.2.

**[P] Primary technical source.** OpenAI, [Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), official-linked 166-page PDF, hash in §1. Technical locators: Theorem 1.1 p. 1; §§2.1–2.3 pp. 3–6; §3.1 pp. 7–8; §§3.2–3.4 pp. 9–16; Theorem 3.1 and (3.3)–(3.6) pp. 15–16; (4.1)–(4.4), Lemma 4.1 pp. 24–25; Theorem 4.6; Proposition 5.5 and (5.41); (6.1)–(6.6) pp. 62–63; Lemma 7.4 and (7.21)–(7.22) pp. 80–81; Proposition 7.5 and (7.24)–(7.26) pp. 82–83; Proposition 9.9 pp. 114–116, especially Step 5; Proposition 10.1 and Lemmas 10.3–10.4; §10.4 and (10.20)–(10.23) pp. 123–124; Corollary 10.6 pp. 125–126. These are source anchors for original estimator analysis D1–D4, not a claim to have independently verified every proof step.

**[A] Publication provenance.** [OpenAI announcement](https://openai.com/index/navier-stokes-solution/), “The result” and its paper link. Used to locate the primary PDF, not to infer DNS predictions.

**[C] Mathematical formulation.** C. Fefferman, [Existence and Smoothness of the Navier–Stokes Equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), alternatives (A)–(D), pp. 2–3. The paper claims the forced alternatives; this receipt does not convert them into an unforced or generic-turbulence claim.

**[J1] Dataset and forcing.** [JHTDB Forced Isotropic Turbulence](https://turbulence.idies.jhu.edu/datasets/homogeneousTurbulence/isotropic), “Simulation data provenance” and coarse/fine bullets. Documents low-wavenumber energy injection, fields, coarse interval and short fine interval. Linked empirical time-history and spectrum files were not opened.

**[J2] Dataset resolution and derivative caveat.** [JHTDB extended isotropic README](https://turbulence.pha.jhu.edu/docs/README-isotropic.pdf), simulation parameters and full-record statistics p. 1, early-segment statistics p. 2, derivative note 3 p. 4. Used only for instrument metadata, not target-event outcomes.

**[J3] Functions and interpolation.** [JHTDB Analysis Tools](https://turbulence.pha.jhu.edu/analysisdoc.aspx), Database Functions, Time Interpolation Options, Spatial Filtering Options and Threshold Options. Documents velocity/gradient/force availability and nearest-stored-time versus interpolated returns. Function listing alone does not establish a valid pinned client.

**[J4] Legacy component convention.** [JHTDB C/Fortran help](https://turbulence.pha.jhu.edu/help/c-fortran/), GetVelocity and GetVelocityGradient examples; Interpolation Flags. Exact named component sequence, not proof of GetData extraction equivalence.

**[J5] Access surface.** [JHTDB Database Access](https://turbulence.idies.jhu.edu/database), Python Local and Cutout Service sections. Documents pointwise and gridded access routes, not a task-specific entitlement or tested budget.

**[J6] Transport caveat.** [JHTDB legacy home page](https://turbulence.pha.jhu.edu/), opening notice concerning HTTP/HTTPS redirects and replacement access tools. Availability caveat only; no live service operation was attempted.

**[R1] Frozen E0.** [Preregistration at the inspected commit](https://github.com/vortexpixelz/ns001/blob/711b6c7f0cfd1c69694bff8a3fd134b585e633df/preregistrations/e0/NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md), §§2–6, 10–13; sidecar verified locally. [README at that commit](https://github.com/vortexpixelz/ns001/blob/711b6c7f0cfd1c69694bff8a3fd134b585e633df/README.md), opening status warning. Repository code was not executed.

**[R2] Interface limitations.** [Interface decision draft](https://github.com/vortexpixelz/ns001/blob/711b6c7f0cfd1c69694bff8a3fd134b585e633df/preregistrations/e0/NS-001_E0_INTERFACE_DECISION_DRAFT.md), Proposed decision and Unresolved evidence; [GetData amendment draft](https://github.com/vortexpixelz/ns001/blob/711b6c7f0cfd1c69694bff8a3fd134b585e633df/preregistrations/e0/NS-001_E0_GETDATA_AMENDMENT_DRAFT.md), Proposed interface change and structural controls. Historical shape-only evidence is reported there, not reproduced here.

**[R3] Declaration-only boundary.** [H2 evidence contract draft](https://github.com/vortexpixelz/ns001/blob/711b6c7f0cfd1c69694bff8a3fd134b585e633df/docs/e0/h2/H2_EVIDENCE_CONTRACT_DRAFT.md), Pure H2A0 scope, Eight unresolved substantive gates, and capability boundary. Schema coverage is not verified evidence or execution permission.

**Preservation receipt.** After authoring, SHA-256 comparison confirmed all 22 pre-existing tracked files unchanged, including the E0 preregistration and sidecar. The only repository addition is this separate E1 review document. No commit, push, experiment, empirical test, or governing-review edit was performed.

Gate 1 status: PARTIAL.

Run authorization: NOT GRANTED.
