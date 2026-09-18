# NS-001 / E1–OpenAI Gate 1 Derivation Receipt v0.2

Bounded closure attempt · 16 September 2026 · E0 frozen and HOLD

## 1. Decision and changes from v0.1

**Gate 1 remains PARTIAL.** The circulation-to-vorticity lower bound survives an explicit audit. The provisional primary family can be reduced to local speed amplitude and a scalar spatial moment size, avoiding both vorticity anchoring and the weak anisotropy signal. A fully specified candidate measurement operator is given below. However, its correspondence to the constructed core and its finite-scale error envelope have not been established over an identified DNS-resolvable range. Operator definability is not sufficient evidence of that correspondence.

This is a closure attempt, not a preregistration. No frozen preregistration text is supplied because Gate 1 does not pass. No controls were designed, no target outcomes were inspected, and no experiments, simulations or JHTDB calls were made in this continuation. Provider-documentation facts below reuse the sources inspected for v0.1; they were not refreshed through a live service call. The retained primary PDF was reread at the cited technical locations and its hash rechecked.

Changes from v0.1:

| Item | v0.2 disposition |
|---|---|
| Circulation argument | Gives the loop, orientation, Stokes identity, signed average, constants, inequality and finite-time qualification. Retains a local lower bound, not global scaling. |
| Primary geometry | Reduces the proposed joint observable to `(U,L)`, where L is the speed-weighted radius of gyration. Radial/axial widths and anisotropy are not primary. |
| Center | Uses the centroid of a complete local speed-weighted region, not a velocity or vorticity argmax and not an inferred circulation axis. |
| Moment operator | Replaces a hard component mask with a specified nonnegative excess-speed-squared weight in a fixed window. This is an estimator choice, not a theorem. |
| Resolution | Supplies explicit mathematical error conditions and clearly marked engineering numbers. No “eight cells suffice” scientific claim is made. |
| Closure | The scope question is resolved in favor of background-geometry resemblance only. Core inheritance and a nonempty certified finite-scale range remain fatal to a PASS. |

**Label key.** PAPER-DERIVED denotes content traceable to the primary paper. MATHEMATICAL CONSEQUENCE denotes a derivation here, with its assumptions. ESTIMATOR DESIGN CHOICE denotes a prospective measurement convention, not a physical fact. UNSUPPORTED / REJECTED denotes an inference not licensed by the sources. Every assertion in the circulation audit is explicitly assigned one of these labels. Labels elsewhere distinguish the same epistemic roles.

## 2. Circulation-to-vorticity audit

### 2.1 Source statement and exact loop

**PAPER-DERIVED.** In the viscosity-one construction put `τ=1−t`, `a=1/2+h`, and choose the fixed `Xin∈(0,Xa)` used in Theorem 3.1(iv). Equation (3.6) gives

`uθ(rτ,0,0,1−τ)=τ^(−a)[e0+R(τ)]`,

where `rτ=√(2 Xin τ)`, `e0>0`, and `R(τ)=O(τ^(2h))`. The arguments are cylindrical position and time. Proposition 9.9, Step 5, explains the inner-region preservation; equations (10.20)–(10.21) place the path inside the final cutoffs for sufficiently small τ. [P, pp. 16, 116, 124]

**PAPER-DERIVED.** The base is axisymmetric; annular corrections vanish in this inner region. These facts, rather than a single pointwise value alone, allow the stated value to extend around the circle. The construction is smooth in Cartesian coordinates for each `t<1`, including the axis. [P, (4.4)–(4.5), Proposition 5.5, Proposition 9.9 Steps 2 and 5]

**MATHEMATICAL CONSEQUENCE.** The relevant circulation is

`Γ(τ)=∮Cτ u(x,1−τ)·dℓ`,

`Cτ: x(θ)=(rτ cosθ,rτ sinθ,0), 0≤θ≤2π`,

with positive tangent `eθ` and disk normal `+ez`. This is a derived circulation functional on the paper's growth circle; the paper's blowup proof uses velocity on that circle, not a separately named circulation observable or a Kelvin-conservation argument.

**MATHEMATICAL CONSEQUENCE.** Because `dℓ=rτ eθ dθ`, the radial and axial velocity components contribute zero to this line integral. Axisymmetry and the preserved inner growth give the exact identity and asymptotic expression

`Γ(τ)=2π rτ uθ(rτ,0,1−τ)`

`=2π√(2 Xin) τ^(−h)[e0+R(τ)]`.

### 2.2 Stokes identity and bound

**MATHEMATICAL CONSEQUENCE.** Let `Dτ={z=0, x1²+x2²≤rτ²}`. Stokes' theorem applies to the instantaneous smooth field on this disk:

`Γ(τ)=∫Dτ (curl u)·ez dS`.

Define the **signed disk-average axial vorticity**

`Ωbar_z(τ)=Γ(τ)/(π rτ²)`

`=√(2/Xin) τ^(−1−h)[e0+R(τ)]`.

This is not the average of `|ω|`, and the disk is not a transported material surface. The derivation uses neither circulation conservation nor a vorticity evolution approximation.

**MATHEMATICAL CONSEQUENCE.** The norm inequality is

`|Ωbar_z| ≤ (area Dτ)^−1 ∫Dτ |ωz| dS ≤ supDτ |ωz| ≤ supDτ |ω| ≤ supΩ |ω|`.

If `|R(τ)|≤C τ^(2h)`, choose a positive `τ0` inside the inner/cutoff regime with `C τ0^(2h)≤e0/2`. For `0<τ≤τ0`,

`supDτ |ω| ≥ [e0/√(2 Xin)] τ^(−1−h)`.

Thus there is a local component-average scaling and a local supremum lower bound; the global supremum inherits the inequality only. The lower bound does not identify where on the disk the largest vorticity occurs.

### 2.3 Assumptions and localization ledger

| Label | Assumption or conclusion | Why it is needed |
|---|---|---|
| PAPER-DERIVED | `Xin` is fixed inside the protected inner radial interval; `z=0`, hence `q=τ`, `η=0`. | Keeps the loop out of the annular pulse supports. |
| PAPER-DERIVED | Axisymmetric base and absent annular corrections on the loop. | A value at one azimuth is otherwise insufficient to determine circulation. |
| PAPER-DERIVED | The final localization is identically one near the growth path at sufficiently small τ. | Prevents replacing the local field by an altered cutoff field on the loop. |
| MATHEMATICAL CONSEQUENCE | Cartesian `C1` regularity on a neighborhood of the disk and consistently oriented boundary suffice for Stokes; the paper supplies stronger smoothness. | Cylindrical coordinate singularity at the axis is not a physical singularity for `t<1`. |
| MATHEMATICAL CONSEQUENCE | Only the boundary growth formula and disk regularity are required for the average identity. No pointwise sign assumption about vorticity throughout the disk is required. | Avoids an unstated positivity assumption. |
| ESTIMATOR DESIGN CHOICE | In a hypothetical DNS circulation estimator, center, disk normal, radius and sign convention would have to be fixed by an independently justified operator. | Those objects are given by the construction but not supplied by DNS metadata. No such DNS estimator is promoted here. |
| UNSUPPORTED / REJECTED | A maximum of velocity or vorticity identifies this disk center, its plane or `Xin`. | The construction's center is its concentration origin; a swirl-speed maximum can be a ring. |

### 2.4 Finite-time content and nontransfer

**MATHEMATICAL CONSEQUENCE.** At any preterminal time at which the loop lies in the protected region, the Stokes identity is exact. The positive lower bound requires the additional error condition above. At larger τ the asymptotic remainder alone supplies no numerical lower bound. The source does not supply a numerical value for this receipt's `C`, `τ0`, or dimensional DNS correspondence.

**MATHEMATICAL CONSEQUENCE.** Let `τ2<τ1≤τ0`, `S=τ1/τ2`, and `|R(τi)|/e0≤εi<1`. A sufficient condition for the signed average to increase between these times is

`S^(1+h) (1−ε2)/(1+ε1)>1`.

An asymptotic formula without these error allowances is not a certified finite-window direction. Nor does an increasing average force the supremum to increase at every sampled time; the latter can already be larger for another reason.

**MATHEMATICAL CONSEQUENCE.** Under the paper's viscosity rescaling, the corresponding loop radius gains `√ν`, velocity gains `√ν`, circulation gains `ν`, and the disk-average vorticity is unchanged at corresponding coordinates and time. Additional Navier–Stokes space-time rescaling changes those coordinates and times again. These transformations do not determine a DNS event's radius or time-to-terminal parameter. [P, (10.22)–(10.23), Corollary 10.6]

**UNSUPPORTED / REJECTED.** Transfer to stationary DNS of a universal `M(t)∝τ^(−1−h)`, a common velocity/vorticity argmax, an inferred terminal time, a velocity–vorticity lag, or this specially located disk. The argument survives as mathematics of the constructed field, not as an operational primary signature for the dataset. It is not demoted mathematically; its DNS operational role is withheld.

## 3. Reduce the joint signature before defining an operator

**ESTIMATOR DESIGN CHOICE.** Retain only local speed amplitude `U` and speed-weighted radius of gyration `L=√tr Q`. Their proposed joint direction is `U increases AND L decreases`. No anisotropy ratio, vorticity amplitude, direction of an eigenvector, or multiscale lag is primary. The conjunction is weaker than all-axis contraction: it cannot exclude one dimension expanding while the total second moment decreases. This loss of specificity is explicit.

**MATHEMATICAL CONSEQUENCE.** For an ideal fixed-shape normalized intensity region with nondegenerate axisymmetric moments, write

`Qideal(τ)=R diag(cr τ, cr τ, cz τ^(1−2h)) Rᵀ`, with `cr,cz>0`.

Then

`Lideal²=2cr τ+cz τ^(1−2h)`.

Both terms decrease as physical time approaches the terminal time. Its logarithmic contraction exponent with respect to τ lies in `[1/2−h,1/2]`, unlike the much weaker exponent h for anisotropy. This reduction removes the need to resolve a tiny *difference* between contraction rates. It does not prove that the DNS operator below has these moments.

**MATHEMATICAL CONSEQUENCE.** The conditional fixed-shape representation can be seen directly from the source coordinates. Put `r=τ^(1/2)ρ`, `z=τ^D ζ`, `D=1/2−h`, and `q=τ Qs`. The equation for q becomes

`Qs−ζ² Qs^(2h)=1`,

so `Qs`, `η=ζ/Qs^D`, and `X=ρ²/(2Qs)` are τ-independent. For the leading tangential velocity, the normalized speed profile is therefore

`F(ρ,ζ)=Qs^(−a) √(E(X,η)²+Uprofile(X,η)²)`.

The normalized radial component is lower order on compact similarity regions. These are algebraic consequences of equations (3.2), (4.1) and (4.3), not an assumed isotropic similarity ansatz.

**MATHEMATICAL CONSEQUENCE — conditional bridge lemma.** If (i) the relevant normalized speed converges uniformly to F on a region containing its whole above-threshold mass, (ii) its normalized peak converges to a finite positive `Fmax`, (iii) the resulting positive-weight set is bounded in similarity coordinates with nonzero mass and positive-definite second moment, and (iv) omitted exterior/background weight has vanishing zeroth and second moments after normalization, then the operator below converges, after anisotropic rescaling, to a fixed moment tensor. The excess weight is continuous in speed, so no hard level-set topology theorem is needed merely to pass moments to the limit. Axisymmetry gives equal radial moments and zero radial–axial cross moments, even if the axial centroid is displaced. A dominated-convergence argument proves this conditional result.

**UNSUPPORTED / REJECTED — unresolved premise, not a proved conclusion.** Uniform asymptotics on selected profile rectangles do not by themselves establish all four conditions for the entire speed-selected region inside a fixed physical cube, including its tails and completed-field corrections. Proposition 5.5, equation (5.42), and the correction bounds are relevant inputs, but no explicit domination and finite-τ error certificate for this operator is established here. A theorem-specific limiting argument with unknown crossover scales also does not certify a usable range on a 1024³ DNS grid. This is the remaining estimator bridge blocker.

## 4. Complete candidate operator, not frozen

All conventions in this section are **ESTIMATOR DESIGN CHOICE** unless marked otherwise. They define one outcome-independent candidate for audit; their specificity does not grant approval. There is no search over thresholds, crops, centers or time windows to improve a result.

### 4.1 Field, fixed spatial window and periodic coordinates

Use native-frame vector velocity `(ux,uy,uz)` at actual stored times of `isotropic1024coarse`. Let `Δ=2π/1024`. Input window metadata `(a,k0,N)` must be fixed without looking at the joint trend. How events are selected is outside this closure attempt; the operator does not select them. Here `a` is a native-grid location marking a *search-window origin*, not an asserted vortex center.

For a concrete candidate, use the 65³ native nodes whose offsets from a are `jΔ`, `j∈{−32,…,32}` in each coordinate. Associate each node with its cube of side Δ. The union is a fixed physical cube of half-side `H=32.5Δ`; equal cell volumes enter every sum. Keep this same cube throughout the window. No recentering, expansion or peak following is allowed.

Wrap requested coordinates modulo `2π`, but do all moments in the single unwrapped chart `y∈[−H,H]³` around a. Here `2H<2π`, so each node has one copy. Do not average wrapped coordinates or unwrap separately around whichever peak happens to win. A support that reaches the edge fails the adequacy rule below; it is not stitched to an unobserved continuation.

Set `s_i=|u_i|`, `Uhat=max_i s_i`. No local-mean subtraction, filtering or interpolation is applied. Speed and U have velocity units; Q has length-squared units and L has length units in the dataset's nondimensional coordinates. Report endpoint ratios and log differences without fitting a terminal time. A Galilean boost changes s and the region: the laboratory-frame convention is part of the estimand.

### 4.2 Weight, normalization, center and covariance

Fix `α=1/2` for this candidate and set

`w_i=max(s_i²−α² Uhat²,0)`,

`mhat=Δ³ Σ_i w_i`, `p_i=w_i/Σ_j w_j`,

`chat=Σ_i p_i y_i`,

`Qhat=Σ_i p_i (y_i−chat)(y_i−chat)ᵀ`,

`Lhat=√tr Qhat`.

This is a covariance tensor, not the mechanical inertia tensor `tr(Q)I−Q`. The center in physical coordinates is `a+chat`, with a wrapped copy retained only for reporting. Use **all positive-weight nodes in the fixed cube**, without selecting the component that contracts best. Record connectivity as an adequacy diagnostic; separated positive-weight components make the candidate window unresolved rather than inviting a favorable component choice. On the lattice, use face connectivity (six neighbors), a specified engineering convention.

**MATHEMATICAL CONSEQUENCE.** For the ideal axisymmetric concentrating profile, the weighted centroid lies on the concentration axis and its axial offset scales with the axial length. It converges to the singular origin as the region contracts, though it need not equal the source's plane `z=0` at finite τ. This matches an intensity-region moment center, not the special circulation disk. It is why centroid-based geometry is preferable here to either argmax. The missing whole-region bridge in §3 remains explicit.

### 4.3 Eigenvalues, widths and degeneracy

Order `λ1≤λ2≤λ3` of Qhat. Principal RMS widths are `sqrt(λj)`. The primary size is `Lhat=√(λ1+λ2+λ3)`; its factor convention is fixed and is not the diameter of a threshold set.

Radial/axial assignment is **not performed for the primary**. If a later descriptive label were justified by the source correspondence and an axial eigengap larger than error, use `lz=√λ3`, `lr=(λ1λ2)^(1/4)`. Elongation alone does not justify calling λ3 axial. Without that justification the widths remain principal widths only.

There is no primary orientation-continuity requirement. For descriptive orientation, use the sign-free projector `eeᵀ`; if a vector is displayed, pick its sign to give nonnegative dot product with the previous identified vector. At a repeated axial eigenvalue or an eigengap unresolved by error, mark orientation undefined and do not interpolate it. The ordinary axisymmetric degeneracy `λ1=λ2>0` is **not** an estimator failure: the transverse plane is identifiable, its internal basis is not. Even `λ1=λ2=λ3>0` leaves L well-defined. Rank deficiency, nonpositive mass, or an unresolved smallest width is a different problem.

### 4.4 Support, conditioning and movement rules

The mathematical minimum for positive-definite Q is positive mass on at least four affinely independent positions. That is algebraic rank, not adequate spatial resolution. Require positive mass, finite fields, symmetry/positive semidefiniteness to numerical tolerance, and a positive lower error bound on λ1. Reject missing/nonfinite samples rather than dropping them.

Concrete candidate engineering screens, none literature-validated as sufficient:

- At least eight grid intervals across `2√λ1`, equivalently `√λ1≥4Δ` (nine locations across an aligned interval). This RMS-diameter convention is not a physical core diameter.
- Effective weight count `Neff=(Σw)²/Σw²≥8`, in addition to full affine rank. This prevents a few nodes carrying essentially all mass; it does not certify shape accuracy.
- The two outer node layers have zero positive weight; every positive node is at least two grid intervals from the cube boundary. This is a crop screen, not proof that another relevant region does not lie outside the cube.
- Require a separately justified covariance error bound `EQ≤λ1/4`. This one-quarter allowance is a design convention; having many nodes does not establish it.
- Centroid displacement at successive stored frames is at most `2Δ`, and the positive set stays inside the same chart and guard. Exceedance makes the window unresolved for this operator; do not recenter it.

No per-frame argmax displacement cutoff is imposed. Argmax is not tracked: tied ring maxima can switch arbitrarily without movement of the region. All maximizing nodes remain subject to the window and guard requirements. A large change in a *unique* peak can flag identity doubt, but it cannot be converted into a theorem-derived speed limit.

### 4.5 Sensitivity and paired failure rules

| Quantity | Direction and failure condition | Translation / rotation / threshold sensitivity |
|---|---|---|
| Uhat | Resolved positive endpoint log change. A resolved nonpositive change fails the joint signature; overlapping error bounds are inconclusive. | Invariant under spatial translation of field and window together and continuum coordinate rotation; not under Galilean boosts. Native-grid offsets and lattice rotations alter sampled maxima. α does not affect Uhat, but crop and competing peaks do. |
| Lhat | Resolved negative endpoint log change in the same adequate window. Resolved noncontraction fails the joint signature; uncertain change is inconclusive. | Central moment removes coordinate-origin dependence. Trace is rotation-invariant for the same complete field/region; a finite cube and grid break exact rotational equivalence when cropping or sampling matters. α controls the weight and cannot be retuned after outcomes. |
| chat, Qhat, support | Adequacy information, not extra positive evidence. Rank, mass, crop, connectivity or association failure prevents interpretation. | An asymmetric axial profile shifts chat. Nearby structures and chart/crop changes can move it. Equal radial eigenvalues do not invalidate L. |

For finite-window decisions let bounds on U and L at each endpoint be `[U−,U+]` and `[L−,L+]`. A certified joint direction requires `U−end>U+start` and `L+end<L−start`. If an opposite direction is certified for either quantity, the joint signature fails. Otherwise it is inconclusive. A window rejected for measurement adequacy is not a negative physical observation.

False contraction can occur when a growing narrow peak raises the relative threshold and removes an unchanged broad background. It can also occur when a second structure leaves the cube, when a connection disappears across one grid cell, when quantization changes a near-tied maximum, or when noise changes normalized weights. A soft weight reduces discontinuous node entry/exit but does not remove moving-threshold bias. An analytic counterexample class is a fixed-width central peak whose amplitude grows against a spatially extended fixed background: outer weights can vanish although neither physical component narrows. This is a logical example, not a simulation or empirical finding.

False anisotropy can arise from grid alignment, two neighboring peaks, a clipped ring or axial eigenvalue swapping. Those do not enter a primary anisotropy score here, but they can also bias trace. For `α,β∈[0,1]`, `|wα−wβ|≤2U²|α−β|`; when total weight is small even a small threshold change can strongly alter normalized moments. This bound explains sensitivity; it does not authorize a threshold sweep.

## 5. Resolution-and-cadence certificate: conditional bounds, not a sufficiency award

### 5.1 Spatial error requirements

**MATHEMATICAL REQUIREMENT.** A finite number of point samples cannot certify an arbitrary smooth field's intersample maximum or width without an additional regularity/bandwidth/error bound. A two-samples-per-wavelength criterion, even for a suitably bandlimited field, is not a universal criterion for accurate nonlinear thresholded moments or maxima. No literature-supported universal cells-per-core threshold is claimed in this receipt.

Let the continuum comparison be the same operator on the fixed cube B. Its cell-center distance bound is `d=√3Δ/2`. Suppose a certified speed Lipschitz bound `Ks` on B and velocity/sample error bound `eu` are available. Then a conservative speed error is `Es=Ks d+eu`, and the sampled-maximum error has a bound `EU≤Es` under complete coverage. Such bounds are **required inputs**, not established by the queried values or by a sparse derivative check.

For a bound U on the exact speed maximum and the chosen α,

`Ew ≤ 2U Es+Es² + α²(2U EU+EU²)`

bounds error in the soft weight. With cube volume `VB`, `E1≤VB Ew` bounds its L1 error. Any separately claimed omitted spatial mass must be included when comparing the cube to a whole core. Let `m=∫B w dx`; require `E1<m` and an independently defensible positive lower mass bound. A conservative total-variation allowance for normalized weights is `η≤E1/(m−E1)`.

For positions within distance `RB=√3H` of a, moving exact mass to cell centers and changing the normalized weights yields the conservative covariance bound

`EQ ≤ 4 RB d+2d²+6 RB² η`.

The first term bounds coordinate quantization and centering; the second-moment change under total variation is bounded by `2RB²η`, and the centroid outer-product change by `4RB²η`. These intentionally conservative estimates may be too weak to certify the chosen crop. That is a legitimate failure of the certificate, not permission to replace it with “eight cells.”

Weyl's inequality gives `|λhat_j−λ_j|≤EQ`, and `|tr Qhat−tr Q|≤3EQ`. Thus

`L−=√max(0,tr Qhat−3EQ)`, `L+=√(tr Qhat+3EQ)`.

Use corresponding sample/value bounds for U. Require `λhat1>EQ` for resolved three-dimensional support. These inequalities give an explicit width–spacing–error relation for the primary without inventing a scientific resolution cutoff. They also show why a crop much larger than the core can make a conservative error estimate useless.

**UNSUPPORTED / REJECTED.** Treating FD gradients as a certified intersample Lipschitz bound without an error argument, treating interpolation as an independent finer DNS, or treating the engineering support screens as a substitute for these inequalities. A full native spectral-field error argument could provide a different certificate, but none was derived or executed here.

### 5.2 Temporal identifiability

**MATHEMATICAL REQUIREMENT.** Two distinct stored times suffice to define an endpoint difference. They do not resolve intervening contraction, identity changes or reversals. A temporal path guarantee requires bounds, not just a chosen number of frames. If `Bf` bounds `|d²f/dt²|` for `f=log U` or `log L`, piecewise-linear temporal reconstruction has error at most `Bf δt²/8` on each interval. Without a defensible Bf or a comparable bandwidth/variation bound, a finite sequence cannot certify behavior between frames.

**ESTIMATOR DESIGN CHOICE.** For the candidate operator require at least five consecutive native stored frames, so `N≥5`, `W=(N−1)δt≥0.008` with documented `δt=0.002`. This is a minimal reporting/identity convention, not a validated timescale requirement. Longer W must be chosen without inspecting the joint outcome; five frames are not five independent events. Report the endpoint estimand as such, even with additional frames.

**MATHEMATICAL REQUIREMENT.** For ideal core-size contraction over a remaining-time ratio S, `Lend/Lstart` lies between `S^−1/2` and `S^(−1/2+h)` for the fixed-shape model. A sufficient detectable contraction is that its log change exceed both endpoint log-error allowances plus the finite-profile remainder allowance. Analogously require `(1/2+h)log S` to exceed the amplitude error and remainder allowances. No source-derived number maps S or the asymptotic-entry scale to a JHTDB W. Dropping anisotropy improves the exponent but does not supply that map.

### 5.3 Requirements by primary observable

| Requirement | Uhat | Lhat | Basis / status |
|---|---|---|---|
| Native samples across smallest width | Inherits the same region-resolution requirement as L; a single sampled peak is insufficient | Candidate: ≥8 intervals across `2√λ1`; ≥9 locations on an aligned span; `√λ1≥4Δ` | Engineering convention requiring later acceptance, not literature-supported sufficiency |
| Quantitative accuracy | `EU≤Ks d+eu`, less than the amplitude change being asserted | EQ and endpoint interval separation as above; `λ1>EQ` | Mathematical error requirements; constants not certified |
| Neighborhood | Complete fixed 65³ node cube, same at all times | Same cube, positive region clear of two outer node layers | Size/guard are engineering choices; full relevant support is a mathematical condition for core correspondence |
| Temporal samples | At least 2 for endpoint change; candidate uses ≥5 actual frames | Same | 2 is an algebraic minimum; 5 is engineering; neither certifies interframe dynamics |
| Displacement | No argmax tracking or peak-jump criterion | Candidate centroid step ≤2Δ; support remains in fixed window | Engineering identity screen, not a material speed bound |
| Derivative order | Operator uses velocity values only | Operator uses velocity values only | No gradient response is required by the primary; a certified error bound needs additional regularity information |
| Boundary requirements | Complete maximum search inside declared cube and guard | Same periodic chart for mass, centroid and covariance | No derivative stencil halo for operator; any later derivative-based error estimate requires its own halo/error contract |
| Components | Correctly ordered three-component velocity, coordinates and actual timestamps | Same plus complete spatial layout | Nine gradient components are not primary inputs; legacy C/Fortran order does not validate an unspecified GetData extraction |
| Interpolation | No interpolated time or space samples in this candidate | No densification of the moment grid | Interpolation can move extrema and alter apparent support without adding information; any later use changes the operator |

### 5.4 Dataset/API classifications

| Evidence being classified | Classification | Reason |
|---|---|---|
| Provider-described three-component velocity on a 1024³ periodic grid | CONDITIONALLY SUFFICIENT | Contains the field type needed for the defined discrete operator, conditional on verified extraction, layout and complete cube access. |
| Native spacing `2π/1024≈0.006135923` and stored cadence `0.002` | CONDITIONALLY SUFFICIENT | Defines possible sampling windows and scales; does not show any selected event meets the certificate. |
| Actual target-core spatial/temporal resolving power | UNKNOWN | Core scales, shape/remainder constants and a priori error bounds are not established. No target data were inspected. |
| Five stored frames and exact endpoint/index mapping for this operator | UNKNOWN | The documentation's 5028-frame count versus inclusive [0,10.056] arithmetic remains unresolved; no client/time-index receipt is pinned. |
| Selected API's vector ordering, extraction nesting, cube layout and transport/provenance | UNKNOWN | Existing repository evidence is draft and includes only historical shape reports; this continuation does not verify a client. |
| Continuum or sub-native-scale inference | INSUFFICIENT | Denser access/interpolation to the same stored DNS cannot establish beyond-grid physics or continuum convergence. |
| Using the short “fine” record to restore arbitrary coarse-event cadence | INSUFFICIENT | Its documented interval is only 0.0002–0.0198; it does not restore missing frames elsewhere. |
| Combined current dataset/API evidence for a certified construction-derived signature | UNKNOWN | No VERIFIED SUFFICIENT classification is justified. Conditional computability is not certified resolving power. |

The provider's mean Kolmogorov scales and Reynolds numbers are not extreme-event resolution certificates. No numerical grid minimum in this receipt is classified as a literature-supported core-width threshold; the numerical engineering screens are proposals whose adequacy is expressly unproven.

## 6. Weakest surviving candidate claim

**ESTIMATOR DESIGN CHOICE — candidate claim, not a finding:**

“Within the resolvable range of isotropic1024coarse native-grid three-component velocity at its stored cadence, selected event windows do exhibit increasing local speed amplitude together with decreasing speed-weighted radius of gyration in the direction predicted for the background concentration geometry of the OpenAI construction.”

This single directional claim is a hypothesis awaiting a valid bridge and resolving-power certificate. It does not identify oscillatory-pulse cancellation; provide proof or evidence of singularity; validate the theorem; imply generic velocity-to-vorticity scaling; or support inference beyond the resolved numerical range. It does not claim all-axis contraction, increasing anisotropy, causal transfer or mechanism specificity. The phrase “resolvable range” must be established prospectively, not defined afterward by keeping favorable windows.

The claim remains scientifically interpretable as a restricted kinematic description rather than amplitude alone, but it is not ready to enter a preregistration. The present audit does not establish that its estimator is a faithful finite-scale measurement of the source geometry. No alternative claim is substituted if that bridge fails.

## 7. Closure checklist and remaining items

| Gate 1 requirement | Disposition |
|---|---|
| Direct traceability | Satisfied for the circulation bound and ideal background scaling; conditional for the chosen whole-region moment operator. |
| Explicit direction | Defined: U increases and L decreases; proven for the ideal fixed-shape limit, not certified over a selected finite DNS range. |
| Outcome-independent estimator | A concrete operator is specified with fixed candidate conventions; no target outcome was used. Window inputs remain prospective external inputs. |
| Resolution and cadence | Explicit inequalities and engineering screens supplied; no nonempty valid operating range certified. |
| Known analogy break | Explicit: constructed forcing/background asymptotics versus stationary, finite-resolution DNS; moment region versus source core. |
| Paired failure condition | Endpoint error intervals distinguish certified joint direction, contradiction, uncertainty and invalid measurement. |
| No excluded shortcut | No global-vorticity scaling, generic scale lag or amplitude-only primary. |

| Unresolved item | Classification | Exact missing receipt / why it matters |
|---|---|---|
| Above-threshold moment inheritance for the constructed background/completed field | **Fatal to Gate 1** | Establish the §3 lemma's whole-region mass, peak, tail and second-moment premises for the fixed operator, or reject it. Compact-profile asymptotics alone do not close this slot. |
| Finite-scale/asymptotic-entry and error envelope compatible with native DNS | **Fatal to Gate 1** | Supply bounds establishing at least one nonempty admissible width/cadence/effect range before target outcomes. Unknown constants cannot be replaced by engineering screens. |
| Concrete client, response shape, spatial layout, time-index convention, provenance and cost | **Deferrable to data feasibility** | Pin authoritative implementation/schema and static metadata; a later bounded live check requires separate authorization. Actual operation remains blocked meanwhile. |
| Which windows meet the predeclared adequacy conditions and sufficient population size | **Deferrable to data feasibility** | Define population before outcomes under later authorization; no empirical assessment here. Gate 1 need not guarantee that matching events exist. |
| Numerical implementation of wrapping, weights, moments and interval decisions | **Deferrable to implementation** | Separate reviewed code and authorized verification; no code or tests created by this receipt. |
| Acceptance of α, cube size, support and temporal engineering screens | **Deferrable to implementation/design freeze only after the fatal analytical items close** | These values are explicit proposals, not frozen text or demonstrated sufficient settings. If the analytical certificate depends on changing them, re-review Gate 1 rather than quietly swapping values. |
| Axial labels, orientation and anisotropy | **Merely desirable** | Not required for the reduced claim; their removal is deliberate and cannot be represented as a positive finding about anisotropy. |
| Circulation as an additional DNS endpoint | **Merely desirable; not part of this design** | Would require its own center/plane/radius estimator. The surviving mathematical bound does not compel adding it. |

No control plan is developed or amended. No E1 preregistration or frozen text is produced. Gate 2 is not authorized. PARTIAL reflects real mathematical and estimator-definition progress, with two specific barriers to closure; it does not assert impossibility of every future bridge.

## 8. Sources and repository preservation

- **[P]** OpenAI, [Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf). Retained 166-page PDF hash: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. Reread locators: §3.1 pp. 7–8; Theorem 3.1(iv), (3.6) p. 16; (4.1)–(4.5) pp. 24–25; (5.26) p. 55; Proposition 5.5, (5.41)–(5.43) pp. 59–60; (9.9) p. 106; Proposition 9.9, especially Step 5 p. 116; (10.20)–(10.23) p. 124 and Corollary 10.6 pp. 125–126. The circulation and moment/error lemmas are this receipt's mathematical consequences, not quotations of a paper theorem about a DNS estimator.
- **[J1]** [JHTDB forced isotropic dataset documentation](https://turbulence.idies.jhu.edu/datasets/homogeneousTurbulence/isotropic), coarse/fine interval and field bullets, inspected during v0.1. Reused here without live refresh.
- **[J2]** [JHTDB extended isotropic README](https://turbulence.pha.jhu.edu/docs/README-isotropic.pdf), p. 1 grid/cadence and p. 4 derivative caveat, inspected during v0.1. Metadata only; no empirical time histories accessed.
- **[J3]** [JHTDB C/Fortran help](https://turbulence.pha.jhu.edu/help/c-fortran/), GetVelocity/GetVelocityGradient examples, and [Database Access](https://turbulence.idies.jhu.edu/database), cutout section, inspected during v0.1. These do not establish a selected client's response contract.
- **[R]** Local repository HEAD `711b6c7f0cfd1c69694bff8a3fd134b585e633df`, branch `codex/e0-h2-preparation`. The frozen E0 preregistration, interface drafts and H2 declaration-only documentation retain the boundaries recorded in v0.1. No repository code was executed.
- **[V1]** Preserved companion `NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.1.md`, SHA-256 `7925644db2b6aba2a8239714b3bfdc8e084d4c8afc9ff22d392f985c9f0dd6fb`. v0.1 is not revised by this continuation.

Repository completion receipt: all pre-existing tracked files and v0.1 retain their entry hashes. This continuation adds only this v0.2 Markdown document. Tracked diff is empty; neither version is committed. No commit or push occurred. The working-tree status lists the two untracked E1 receipt files and no other changes.

Observed `git status --short --untracked-files=all`:

```text
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.1.md
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.2.md
```

`git diff --stat` and `git diff --check` returned no output. Those commands omit untracked files; the substantive new document is v0.2, while v0.1 predates this continuation and is unchanged.

Gate 1 status: PARTIAL.

Gate 2 authorized: NO.

Run authorization: NOT GRANTED.
