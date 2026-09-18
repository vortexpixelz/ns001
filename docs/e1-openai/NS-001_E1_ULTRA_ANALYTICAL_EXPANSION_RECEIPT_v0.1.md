# NS-001 / E1 Ultra Analytical Expansion Receipt v0.1

Round R5 · Phase 1 / Gate 1 · resumed 17 September 2026

## 1. Result, scope and classification

**MATHEMATICAL CONSEQUENCE — principal result.** Accepting the cited construction statements, the completed source field does admit a nonempty **eventual continuum regime** in which its normalized speed converges uniformly to the complete leading tangential profile. For every fixed positive threshold fraction below one and every fixed remaining-time ratio strictly between zero and one, its local peak increases and its soft-weight radius decreases at sufficiently late paired times. Sections 4–5 supply the missing assembly and a positive symbolic interval. This is stronger than R4's unassembled certificate; R4 remains unchanged as a historical receipt.

**UNSUPPORTED / REJECTED.** This does not establish a numerical crossover, a DNS-resolvable operating interval, an outcome-independent decomposition of an arbitrary DNS event, inner-core identification, continuous-time monotonicity, or mechanism specificity. Small admissible perturbations can still manufacture small changes; interpretation requires an effect exceeding the proved error budget. No operator is promoted and Gate 1 remains PARTIAL.

**ESTIMATOR DESIGN CHOICE — round boundary.** This is the continuation of the interrupted Ultra round and its three workstreams: source ranges, observable routes, stability routes. It maps six candidate bridge families plus one limited amplitude diagnostic. It does not open a new experiment or alter any inherited operator convention. All alternatives are analytical candidates. No experiments, simulations, JHTDB queries, repository scientific code/tests, empirical parameter searches, controls, implementation, preregistration, commits or pushes were performed. Administrative source reading, hashing and document work were the only execution in this task.

**ESTIMATOR DESIGN CHOICE — labels.** PAPER-DERIVED identifies source statements; MATHEMATICAL CONSEQUENCE identifies deductions with stated premises; ESTIMATOR DESIGN CHOICE identifies proposed conventions; UNSUPPORTED / REJECTED identifies unjustified implications or failed routes; OPEN CANDIDATE identifies a surviving route whose further premises or suitability remain unresolved. Source-theorem acceptance is not independent verification of the entire paper or its formalization.

## 2. Source and claim ladder

**PAPER-DERIVED.** The primary source is [OpenAI, Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), the retained 166-page PDF with SHA-256 `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. It was reverified against the version used in R4. All page references below are printed, one-based pages. This round uses the retained source, not a different version.

**ESTIMATOR DESIGN CHOICE — inherited reference.** In a fixed physical window B and fixed velocity frame, the current candidate is

`U=sup_B|u|, w=[|u|²−α²U²]+, m=∫_B w, p=w/m,`

`c=∫x p, Q=∫(x−c)(x−c)^T p, L²=tr Q`, with current `α=1/2`.

Continuum integrals are analytical objects; the inherited discrete candidate uses equal-volume native samples. This round studies other fixed α values analytically, without changing α in the candidate, fitting it, or running a sweep.

| Classification | Claim level | Additional implication required |
|---|---|---|
| MATHEMATICAL CONSEQUENCE | Measured contraction: the declared weight distribution has smaller variance. | Accurate evaluation of that functional. |
| MATHEMATICAL CONSEQUENCE | Comparator contraction: an independently specified geometric comparator has smaller variance. | Perturbation margins sufficient to transfer the observed sign. |
| OPEN CANDIDATE | Inner-core contraction: that comparator measures the source's specified inner Cτ. | Core/annulus identification or peak-gap/moment-isolation argument. |
| OPEN CANDIDATE | Physical-component narrowing: an underlying component's spatial scale decreases. | Component identity and shape assumptions excluding pure redistribution. |
| UNSUPPORTED / REJECTED as a consequence of U,L alone | Construction-mechanism resemblance. | Designed forcing, stress cancellation and pulse structure are additional information. |

**MATHEMATICAL CONSEQUENCE.** The first two claims are distinct even with exact measurements. A scalar variance decrease cannot establish all-axis contraction or identify every underlying component. Conversely, the paper already prescribes contracting source scales; an operator bridge concerns whether a proposed measurement inherits them.

## 3. Decomposition inventory

**PAPER-DERIVED.** Put `τ=1−t`, `a=1/2+h`, `d=1/2−h`, `0<h<1/100`. The source uses `τ=q(1−η²)`, `z=q^dη`, `X=r²/(2q)`. Its leading tangential field is `g=q^(−a)(E eθ+U_profile ez)`; its leading radial field obeys `r u_r^(0)=V0`. The final localization is `u=c_loc u_loc+∇c_loc×A_pot`. [§3.1 pp. 7–8; (4.3)–(4.5) p. 25; (10.4) p. 118]

| Classification / decomposition | What can be gained | Limitation and route affected |
|---|---|---|
| MATHEMATICAL CONSEQUENCE: complete leading g versus completed u | `u=g+e` includes radial leading flow, background corrections, annular waves/means and all localization/curl terms. It gives a fixed-shape comparator. | g is a comparator, not a separately asserted divergence-free solution or observed DNS component. S1–S3. |
| PAPER-DERIVED: inner Cτ versus annulus/exterior | Cτ is independently defined by fixed similarity coordinates inside the protected inner region; annular corrections vanish inside the protected radial interval. | The leading annulus/exterior can have the same velocity order as the core. Source support separation is not separation by half-peak speed. S6/P0. |
| MATHEMATICAL CONSEQUENCE: tangential versus radial | For an exactly tangential g and radial r, `|g+r er|²=|g|²+r²`; no first-order cross term. | Only this orthogonal term gets the quadratic gain. Generic wave/mean errors are not radial. All moment routes can use this refinement. |
| PAPER-DERIVED: wave, angular mean, auxiliary mean and correction stages | Finite-stage coefficient bounds and supported potentials permit an absolute error bound after evaluation. | Zero angular/auxiliary average does not zero positive energy, a thresholded cross term, or the whole-window peak. S1/S2. |
| MATHEMATICAL CONSEQUENCE: positive spatial mixture | Partitioning the actual nonnegative weight gives exact mixture-variance formulas. | A vector-field decomposition does not give additive positive energies; `2g·e` remains. Positive support can stay fixed while relative weights change. |
| MATHEMATICAL CONSEQUENCE: signed weight error | `δw=w−w_g` preserves useful signed moment cancellations. | A signed measure is not a probability distribution; its cancellations need independent bounds. S2. |
| MATHEMATICAL CONSEQUENCE: physical versus similarity coordinates | A shrinking physical support is a fixed similarity support, making error margins scale with the shrinking moment. | The source supplies the coordinates; a DNS event does not supply τ, axis, center or dilation merely by looking similar. S1–S6. |
| OPEN CANDIDATE: u_B as comparator | Removes annular/cutoff contamination from one comparison step. | u_B still has radial and higher-order shape changes; a second bridge to g remains. It is useful bookkeeping, not automatic improvement over g. |

**MATHEMATICAL CONSEQUENCE.** In source coordinates, the leading radial normalized amplitude is O(q^h). Its contribution to squared speed is O(q^(2h)), including the perturbation of the squared maximum, when treated using orthogonality. With an additional nonradial error e', retain `2(g+r er)·e'+|e'|²`. The positive O(q^(h/2)) wave-amplitude order can dominate; the radial refinement alone does not certify the full field.

## 4. Establishing an eventual continuum range

### 4.1 Ideal profile and support

**MATHEMATICAL CONSEQUENCE from PAPER-DERIVED profiles.** Let `Dτ=diag(τ^(1/2),τ^(1/2),τ^d)`, `q=τ Qs(ζ)` and `Qs−ζ²Qs^(2h)=1`. In similarity coordinates y, the leading speed is `|g(Dτy,1−τ)|=τ^(−a)F(y)`, with

`F=Qs^(−a) sqrt(E(X,η)²+U_profile(X,η)²)`,

`X=ρ²/(2Qs), η=ζ/Qs^d`.

Theorem 4.6(i),(v), p. 33, gives bounded closed-η profiles on finite X ranges and the exact exterior. Consequently there are finite C0,C1 such that

`F≤C0 Qs^(−a)`, `F≤C1(ρ²/2)^(−a)` for ρ>0.

Thus F is continuous, nonzero, and tends to zero at similarity infinity. Its maximum `M>0` is attained. For every fixed `0<α<1`, the soft weight `W_F=[F²−α²M²]+` has bounded support, positive finite mass `m_F`, and nondegenerate covariance. This repeats the legitimate ideal-profile result in R4 without assuming that its support equals Cτ.

### 4.2 Completed-field comparison, including the axis and summed tail

**PAPER-DERIVED — ingredients.** Positive-order background coefficients have exponents 2nh in (5.1), p. 46, common radial supports and smooth Cartesian representatives at the axis, and recover each fixed asymptotic truncation. Proposition 5.5 proof Steps 3–4, pp. 61–62, explicitly treats axis-reaching estimates and normalized summation. Finite correction states satisfy (9.9), p. 106; the definitions (6.24),(6.29), pp. 69–70, have stage-dependent constants and polynomial factors in `S*=ell²`. Lemma 6.3, p. 68, bounds pointwise label multiplicity; harmonics are finite at each fixed stage. Physical velocity normalization is `Q_band^(−a)`, p. 101, with `q` comparable to `Q_band`. Lemma 5.4 (5.35), p. 58, and Proposition 9.9, pp. 114–116, control the actually summed field.

**MATHEMATICAL CONSEQUENCE — fix stages before taking the limit.** On a fixed bounded X interval containing all corrections, the background estimates give

`q^a |u_B−g| ≤ C_B q^h`.

This includes the leading radial field; tangential background errors are of higher order. The bound at the axis follows through smooth Cartesian coefficients and the recovered expansion, not by extending the displayed annular (5.42) beyond its domain without justification. At one fixed correction stage J, absolute harmonic assembly gives

`q^a |u^[J]−u_B| ≤ C_J q^(h/2)(1+|log q|)^P_J`.

Here finite stage constants, shell weights, label multiplicity, mean terms and curl remainders are included. No oscillatory cancellation is assumed.

**MATHEMATICAL CONSEQUENCE — control the infinite tail.** Write `ell'_0` for the fixed physical loss in (5.35). For a fixed J sufficiently large that

`a+h(J+1)/20−ell'_0 ≥ β`, choose `β=h/4>0`.

For `q<(2a_J)^(−1)`, the final correction tail, after normalization, is bounded by

`2^(−J) q^(a+h(J+1)/20−ell'_0)`.

Such a finite J exists because h>0 and the loss is independent of J. The finitely many retained stages may have large constants; none must be uniformly bounded as J grows. The background sum can similarly be compared with a sufficiently high fixed truncation using its `g_n=2nh` tail, or its stronger recovered expansion can be used directly.

**MATHEMATICAL CONSEQUENCE — explicit logarithm handling.** For γ>β and finite P≥0,

`H_(γ−β,P)=sup_(s≥0) e^(−(γ−β)s)(1+s)^P < ∞`,

so `q^γ(1+|log q|)^P≤H_(γ−β,P)q^β` for 0<q≤1. This is a finite constant, not a discarded logarithmic loss. Combine the preceding inequalities on one positive `q<q_c`, with q_c below the background/stage domains, `(2a_J)^(−1)`, and 1.

### 4.3 From local q control to the fixed observation window

**MATHEMATICAL CONSEQUENCE.** Choose a fixed bounded B containing the concentration origin in its interior. Shrink q_c, if necessary, so bounded-X points with q<q_c lie where final cutoffs equal one. This is possible because `r≤sqrt(2X_ext q)` and `|z|≤q^d`; Proposition 10.1 supplies a fixed neighborhood with c_loc=1 near terminal time. On that region,

`|u−g|≤C q^(−a+β)`.

Since q≥τ and β<a, `τ^a|u−g|≤Cτ^β`. This comparison is uniform, not merely pointwise at a growth path.

**PAPER-DERIVED / MATHEMATICAL CONSEQUENCE.** Outside the bounded X interval, Proposition 9.9 Step 4, p. 116, gives exact exterior agreement and A_pot=0. Any final-cutoff discrepancy there is away from the origin and bounded. For q≥q_c on the compact window, one-sided endpoint regularity bounds the completed field and g; for sufficiently small τ that region stays away from the singular point. Those contributions give `C_far τ^a`. Hence finite constants K,τ0>0 exist with

`ετ := sup_(y∈Dτ^−1 B) |τ^a|u(Dτy,1−τ)|−F(y)| ≤ K τ^β`,

for every `0<τ<τ0`, with `β=h/4`. The vector comparison implies this speed comparison. There is no need for a physical-space derivative estimate to prove this continuum value bound.

**MATHEMATICAL CONSEQUENCE — status.** This assembles a source-derived eventual comparison for the completed field. Unknown numerical values of the finite constants do not invalidate its existence. It is not a hypothesis about an arbitrary DNS field, and it is not yet a sampled-data certificate.

## 5. Positive symbolic interval and finite-ratio directions

**MATHEMATICAL CONSEQUENCE — support transfer.** Fix 0<α<1 and choose a compact similarity set Kα containing the ideal peak, with

`sup_(outside Kα)F≤αM/2`.

If `ετ<αM/[2(1+α)]`, actual and ideal soft weights both vanish outside Kα. For sufficiently small τ, DτKα is contained in B. This is a proof enclosure inside a fixed observation window; the window is not moved to impose contraction.

**MATHEMATICAL CONSEQUENCE — mass and normalized error.** Take a fixed allowance `0<εbar≤M`. On Kα the normalized weight error is at most

`(1+α²)(2M+εbar) ετ`.

Let `Cα=vol(Kα)(1+α²)(2M+εbar)/m_F`. Then `D0/m_g≤Cαετ`, and positivity of the actual mass follows when `Cαετ<1`. With `η=TV(p,p_g)`, `η≤Cαετ`. The ideal mass itself is

`m_g=τ^(1/2−3h)m_F`.

This shrinking normalization is accounted for explicitly rather than replaced by a fixed absolute error.

**MATHEMATICAL CONSEQUENCE — shrinking moment error.** Let Dα be the diameter of Kα and set `C_L=Dα² Cα`. The variance bound in §6 gives

`|L²−L_g²|≤C_L τ^(2d) ετ` for τ≤1,

while `|U−τ^(−a)M|≤τ^(−a) ετ`. Ideal covariance has radial/axial constants cr,cz>0 and

`L_g²=2cr τ+cz τ^(2d)`.

**MATHEMATICAL CONSEQUENCE — nonempty interval.** Fix `0<σ<1` prospectively, comparing `τ2=σ τ1`. Select a positive ε* strictly below each of

`εbar, αM/[2(1+α)], 1/Cα,`

`M(1−σ^a)/(1+σ^a),`

`cz(1−σ^(2d))/[C_L(1+σ^(2d))]`.

All these quantities are positive and finite. Let τB>0 ensure DτKα⊂B, and choose

`0<τ*<min(τ0,τB,1,(ε*/K)^(1/β))`.

K may be enlarged to be positive. For every `0<τ1<τ*`, both completed-field endpoints have positive mass and obey

`U(1−σ τ1)>U(1−τ1)`, `L(1−σ τ1)<L(1−τ1)`.

For amplitude, use `σ^(−a)(M−ε*)>M+ε*`. For size, the ideal squared drop is at least `cz τ1^(2d)(1−σ^(2d))`, exceeding the two endpoint error allowances. This is an established nonempty symbolic continuum interval, not merely a sufficient inequality with an unestablished source premise.

**UNSUPPORTED / REJECTED.** Uniform value convergence does not prove dL/dt<0 at every time, directions for arbitrarily close endpoint pairs, or a usable interval on a fixed grid. Constants may be very unfavorable; h is selected under nested restrictions, including Lemma 4.8, p. 35. No value such as h=0.01 is substituted. No numerical τ*, finite-grid lower scale or dimensional DNS mapping has been established.

**MATHEMATICAL CONSEQUENCE — relation to R4.** R4 correctly withheld a certificate that it had not assembled. This round closes the narrower mathematical existence question for the full-profile comparator, subject to the source statements. Its conclusion does not close the operational or inner-core bridge and does not amend R4's text or historical custody.

## 6. Stability routes and what each actually requires

### 6.1 Absolute and relative errors

**MATHEMATICAL CONSEQUENCE.** For `e=u−g`, `G=sup|g|`, `E=sup|e|`, the inherited soft-weight bound is

`|U−G|≤E`,

`|δw|≤(2|g|+|e|)|e|+α²(2G+E)E`.

Integrate with weights 1,|x|,|x|² to obtain R4's absolute Dk bounds. L² velocity control can bound the first term by Cauchy–Schwarz: on a region S,

`∫_S (2|g||e|+|e|²) ≤ 2||g||_2 ||e||_2+||e||_2²`.

But it still needs separate peak control and an enclosure for the uniform threshold term. Weighted L² versions analogously control moment errors. L¹ velocity control needs an amplitude bound to control its square; an Lp norm with finite p alone does not bound U.

**MATHEMATICAL CONSEQUENCE.** If `|δw|≤ρ w_g` everywhere with ρ<1, then D0≤ρm_g and TV≤ρ. This is a useful relative-weight certificate. It forces δw=0 where w_g=0, so it is stronger than generic small speed perturbation near a soft threshold. It is not automatically inherited from `|e|≤ρ|g|`.

**MATHEMATICAL CONSEQUENCE — amplitude-invariant relative variant.** More generally, for λ>0 and 0≤ρ<1, if `(1−ρ)λw_g≤w≤(1+ρ)λw_g`, the normalized densities are bounded above and below by factors `(1+ρ)/(1−ρ)` and its reciprocal. Minimizing second moments over the center gives

`[(1−ρ)/(1+ρ)]L_g²≤L²≤[(1+ρ)/(1−ρ)]L_g²`.

The arbitrary common λ cancels, but the strong premise still forbids newly activated exterior weight. Before integrating absolute errors, one can also retain `|δw|≤|δs²−α²δU²|`, where `δs²=|u|²−|g|²` and `δU²=U²−G²`; this is tighter when that cancellation is independently controlled.

### 6.2 Signed centered moments: retain cancellation instead of bounding it away

**MATHEMATICAL CONSEQUENCE — exact identity.** Put

`δm=∫δw, v=∫(x−c_g)δw, s=∫|x−c_g|²δw, m=m_g+δm>0`.

Then

`c−c_g=v/m`,

`L²−L_g²=(s−δm L_g²)/m−|v|²/m²`.

This follows by expanding the actual second moment about c_g and then shifting to c. With `T=∫(x−c_g)(x−c_g)^Tδw`, the matrix identity is

`Q−Q_g=(T−δm Q_g)/m−vv^T/m²`.

Only these few signed moments need to be controlled for a variance claim; full-distribution convergence with appropriate second-moment control, such as the shrinking-support bounds in §5, is a sufficient stronger condition.

**MATHEMATICAL CONSEQUENCE.** A two-sided bound is

`|L²−L_g²|≤|s−δm L_g²|/m+|v|²/m²`.

For one-sided decisions, retain the negative centroid term and the signs rather than immediately taking absolute values. If error intervals at endpoints are `l_i≤L_i²−L_g,i²≤u_i`, an observed squared drop greater than `u_1−l_2` plus numerical error forces comparator contraction. The source's signed momentum constraints are not these signed soft-weight moments; their identification remains an input.

### 6.3 TV and transport

**MATHEMATICAL CONSEQUENCE.** If the union of supports of p,p_g has diameter D, then

`|L²−L_g²|≤D² TV(p,p_g)`,

`|L²−L_g²|≤2D W1(p,p_g)`.

For TV, evaluate each variance about the other distribution's centroid; squared distance lies in [0,D²]. For W1, the same squared-distance function has Lipschitz constant at most 2D. These control the central moment, not just the raw second moment. On a radius-R ball, the D²TV bound is no worse than 4R²TV and improves R4's conservative 6R²TV under the same support information.

**MATHEMATICAL CONSEQUENCE.** For any two probability measures with finite second moments,

`|L−L_g|≤W2(p,p_g)`,

and more sharply

`|L−L_g|≤sqrt(W2(p,p_g)²−|c−c_g|²)`.

For each coupling, subtract its mean displacement; the squared transport cost splits into squared centroid displacement plus the centered cost. Reverse triangle inequality in L² controls the difference of centered RMS radii. This can handle small geometric displacement even when TV is large. It requires a bound on actual transport cost; a visual similarity or fitted correspondence is not such a bound.

**MATHEMATICAL CONSEQUENCE.** A mass η moved a distance R has W1 of order ηR but variance contribution of order ηR². Taking R large shows that small W1 alone, without a support or tail condition, cannot control variance. W2 detects that second-moment cost. Conversely small variance error need not imply small W2: different shapes can have identical variance. On diameter-D support there are genuine norm implications, including `W2²≤D² TV` and `W2²≤D W1`; the resulting finite variance-error bounds nevertheless need not be ordered the same way in every case.

### 6.4 Peak and component isolation

**MATHEMATICAL CONSEQUENCE.** Suppose an independently specified component has peak G and exterior speed at most H, with pointwise error ≤E. A sufficient threshold exclusion condition is

`H+E<α(G−E)`, equivalently `H+(1+α)E<αG`.

A peak identity gap `G−H>2E` excludes an exterior winner, but is weaker than exclusion from the entire positive-weight region. Neither condition follows just from source support labels or an inner growth-path lower bound.

**OPEN CANDIDATE.** These refinements can be combined: use orthogonality for the leading radial term, signed moments where source cancellations are proved, and positive tail bounds for everything else. Such hybrid bookkeeping can reduce conservatism while retaining every correction. It is not a license to discard terms based on their names.

## 7. Alternative observables and threshold architecture

| Classification / option | Derived behavior or sufficient stability condition | Failure and disposition |
|---|---|---|
| MATHEMATICAL CONSEQUENCE: fixed α in (0,1), same U,L | Sections 4–5 work for each fixed α; soft weights need no hard level-set transversality. | Constants depend on α. α→0 enlarges tails; α→1 can collapse mass. No universal optimal α or threshold promotion. Retain in S1. |
| MATHEMATICAL CONSEQUENCE: covariance eigenvalues | An operator-norm covariance error gives `|λ_j(Q)−λ_j(Q_g)|≤||Q−Q_g||op`. Under exact profile scaling from τ to στ, sorted eigenvalues lie between σ and σ^(2d) times their earlier values. | Gives a stronger all-width descriptive claim if errors resolve it; fixed-component mixtures can shrink all eigenvalues. It adds requirements, not automatic identification. S1/S2 subroute. |
| OPEN CANDIDATE: quantile radius R_q | Around a specified center, TV≤η brackets its radial distribution between comparator quantiles at q−η and q+η. A density lower bound k>0 near the target quantile gives radius error ≤η/k, plus center error. Ideal pushforward gives radius ratio in `[σ^(1/2),σ^d]`. | Tail-resistant with an independently stable center, but mixtures can move a quantile across components; a flat CDF has no inverse margin. Centroid-based centering can reintroduce distant-tail sensitivity. S4. |
| OPEN CANDIDATE: soft concentration volume `V_soft=m/U²` | Ideal `V_soft=τ^(3/2−h)m_F/M²`; uses bounded relative-speed weights without a covariance denominator. Normalized-speed/peak error and support volume bound its integral error. | Measures effective occupied volume, not radius or component narrowing. Relative amplitudes can decrease it at fixed support. S5. |
| OPEN CANDIDATE: participation volume `V_eff=(∫w)²/∫w²=1/∫p²` | Ideal `V_eff=det(Dτ) V_eff,F`. `|∫p²−∫p_g²|≤||p−p_g||_2(||p||_2+||p_g||_2)`; a positive denominator margin transfers inverse bounds. | Blind to distances between separated pieces; tiny concentrated spikes can dominate ∫p². Needs L²-density control beyond TV. S5. |
| OPEN CANDIDATE: minimum volume containing mass b, `V_b(p)=inf_{p(A)≥b}vol(A)` | Ideal `V_b=det(Dτ)V_b,F`; TV≤η brackets it by `V_(b−η)(p_g)` and `V_(b+η)(p_g)` for η<min(b,1−b). | Ignores topology and separation; denser central weighting can reduce it at fixed component support. Needs a useful quantile-volume bracket. S5 subroute, not a separate architecture. |
| OPEN CANDIDATE: hard concentration volume | A sup-speed error gives set inclusions between nearby profile levels; a bound on the volume of the threshold boundary layer controls volume error. | No boundary-layer modulus is established for a selected level. A plateau makes hard volume unstable. Soft volume avoids this additional premise for its own, different measurand. Not preferred as a separate survivor. |
| ESTIMATOR DESIGN CHOICE: externally normalized soft weight `[|u|²−α²A_ref²M_ref²]+` | Removes dependence on the observed winner if A_ref,M_ref are independently known; threshold-reference error enters separately. | Requires an independent amplitude calibration. Fitting it to observed contraction merely moves the circularity. Even a fixed absolute threshold admits mixture-only narrowing. S6. |
| ESTIMATOR DESIGN CHOICE: robust amplitude, e.g. a speed quantile | Can avoid a sup-norm spike requirement under a CDF margin and suitable probability/reference measure. | Changes U's meaning and source prediction; spatial reference measure must not hide the shrinking core. A fixed-window speed quantile may miss a vanishing-volume core. S4/S6 only after a new bridge. |
| UNSUPPORTED / REJECTED as a cure: α=0, unthresholded full-window energy moments | Uniform amplification still cancels, but relative-amplitude mixtures remain. | Also loses the full ideal profile's finite mass, as proved below. A separately isolated bounded component is needed; not a free simplification. |
| OPEN CANDIDATE, supporting only: protected-circle circulation | The prescribed source circle yields `Γ=2πsqrt(2Xin) τ^(−h)[e0+O(τ^(2h))]`; disk-average axial curl grows as `τ^(−1−h)`. | Source-traceable amplitude diagnostic, not an independently measured contraction endpoint. DNS center, radius, axis and correspondence are missing. P0, not a full joint bridge. |

**MATHEMATICAL CONSEQUENCE — family and quantile qualifications.** On a prospectively fixed compact threshold interval `[α_−,α_+]⊂(0,1)`, α_− supplies a common ideal support enclosure and α_+ a positive lower mass bound. Agreement across that interval still does not identify narrowing: the R3 counterexample works simultaneously for all its thresholds when `B<A1<A2<B/α_+`. Quantile brackets require probability levels to remain in (0,1); the radius inequality assumes a fixed source center or a center transported consistently with the ideal dilation, with any observational center error added separately.

**ESTIMATOR DESIGN CHOICE / MATHEMATICAL CONSEQUENCE — fixed component proportions.** If components can be independently isolated and individually normalized to amplitude-invariant densities p_j, then `p_tilde=Σπ_j p_j` with fixed π_j removes separate scalar amplitude changes. The missing work is precisely the independent decomposition, fixed proportions and treatment of overlapping vector cross terms. Normalizing the whole observed speed by U or multiplying all weights by a common factor changes none of the current normalized weights. This is an S6 subroute, not an automatic fix.

**OPEN CANDIDATE — independently qualified affine template, S6 subroute.** With a prospectively justified center c, orthogonal orientation R and positive dilation D, compare the pulled-back density `p_tilde(y)=det(D)p(c+RDy)` to a prescribed profile density p_F. Small weighted-moment or transport discrepancy then supports that specific profile comparison. This is distinct from supplying only an external scalar amplitude. The source supplies its coordinates; fitting c,R,D and p_F to obtain contraction does not independently certify them for another field. Coordinate/template error and complete mass coverage remain required inputs.

**MATHEMATICAL CONSEQUENCE — alpha zero has an additional obstruction.** From the exact heat exterior (4.29), in similarity coordinates and for sufficiently large ρ, the wedge `|ζ|≤cρ^(1−2h)` lies in the exterior for suitably small fixed c>0. There `F` is bounded below by a positive constant times `ρ^(−1−2h)` because the heat factor tends to a positive limit. Including cylindrical measure and wedge height gives

`∫F²dy ≥ C∫^∞ ρ^(−6h)dρ = ∞`.

Since h<1/100, the integral diverges. Therefore the full ideal profile has no normalized unthresholded energy probability measure on similarity space. The completed localized source still has finite physical energy; this statement does not contradict Theorem 1.1. On a fixed physical crop, alpha-zero normalization retains the moving similarity cutoff and exterior mass. The clean fixed-profile normalization used for α>0 cannot be extended by setting α=0.

**MATHEMATICAL CONSEQUENCE — source masks and circularity.** A prescribed shrinking source-coordinate region can isolate the source's protected component. Its imposed diameter is not an independent measurement of narrowing. Any candidate restricted to such a region must measure nontrivial internal geometry and eventually identify the region from information independent of the tested sign pair. A complete-field comparator avoids this mask circularity, while accepting a broader leading-profile claim.

## 8. Counterexamples and failed routes retained

**MATHEMATICAL CONSEQUENCE — common mixture identity.** With actual normalized weight `p=(1−b)p_C+b p_O`,

`L²=(1−b)L_C²+bL_O²+b(1−b)|c_C−c_O|²`.

Fixed component geometries can therefore yield contraction solely through changing b. Connected positive support and a stable centroid do not remove the effect. The R3 nested-torus example supplies a divergence-free fixed-geometry realization and a smooth approximation; those prior files are preserved.

| Classification / counterexample | What fails | What would exclude it |
|---|---|---|
| MATHEMATICAL CONSEQUENCE: R3 nested torus, growing inner amplitude against fixed exterior | U rises and L falls while both component widths and all positive support stay fixed. With inner half-width a and outer b, `Q_O−Q_C=diag(b²/2,b²/2,b²/3)`, so all covariance eigenvalues can fall too. | Independent component/weight-moment error bounds plus an effect margin; extra eigenvalues alone do not suffice. |
| MATHEMATICAL CONSEQUENCE: participation volume on the same disjoint uniform components | With `z=w_O/w_C∈(0,1)`, `V_eff=(V_C+V_O z)²/(V_C+V_O z²)` has positive derivative in z. Increasing inner dominance lowers it without narrowing support. Soft volume also loses outer relative-speed weight. | Independent profile or mixture control, not a switch to a volume functional. |
| MATHEMATICAL CONSEQUENCE: minimum mass-containing volume | When mass b fits entirely in the denser fixed inner set, `V_b=b(V_C+V_O z)` falls as z falls. | Independent interpretation of density redistribution versus component-volume change; the quantile-volume functional alone does not distinguish them. |
| MATHEMATICAL CONSEQUENCE: vanishing-mass high spike | Smooth localized perturbations can have arbitrarily small finite-p velocity norm while their maximum dominates U and suppresses the original relative-threshold weights. Divergence-free examples can be scaled from compactly supported curls. | Separate sup/peak control, a regularity-to-sup inequality with known constants, or a genuinely different amplitude reference. |
| MATHEMATICAL CONSEQUENCE: small mass at large distance | Tiny TV or W1 can coexist with large variance error if support/tails are uncontrolled. | Weighted second moments, bounded diameter or W2 control. |
| MATHEMATICAL CONSEQUENCE: two fixed radial populations with changing proportions | A mass quantile can move from an outer population to an inner one at fixed widths; a CDF plateau can magnify a small probability change. | Quantile inverse margin and independent mixture/center bounds. |
| MATHEMATICAL CONSEQUENCE: peak migration among separated contenders | A different maximum changes the threshold everywhere and can change which component dominates. | Peak identity gap; full positive-region exclusion needs the stronger threshold gap. |
| MATHEMATICAL CONSEQUENCE: arbitrarily small signed errors at fixed comparator | Any nonzero allowance permits some small observed variance change even with fixed geometry. | A drop larger than the two endpoint error budget. No finite tolerance validates signs of arbitrary size. |
| MATHEMATICAL CONSEQUENCE: higher-frequency small-amplitude temporal perturbation | Uniform value convergence can coexist with derivative sign changes. | Derivative control for monotonicity, or restrict the claim to the proved fixed-ratio endpoint ordering. |
| UNSUPPORTED / REJECTED: annular mean zero, finite energy, flat forcing residual, or fixed support used as a moment certificate | These concern different quantities; none controls normalized threshold mass, peak and spatial second moment jointly. | The actual operator inequalities, not a verbal substitution. |
| UNSUPPORTED / REJECTED: alpha-zero, fixed absolute threshold, or profile fitting advertised as an automatic cure | Relative reweighting survives; alpha-zero also loses ideal mass; fitted normalization can build the desired result into the comparator. | An independently justified region/reference/decomposition and a new bridge. |

**MATHEMATICAL CONSEQUENCE — compatibility limit.** These are operator counterexamples or fields satisfying only selected structural/norm properties. They are not claimed to be alternative realizations satisfying every bound and equation of the OpenAI construction. Once the complete source comparison and the fixed-ratio error margins of §5 hold, a counterexample reversing those particular endpoint directions is excluded. Claims outside those premises remain vulnerable.

**MATHEMATICAL CONSEQUENCE — scope of the failure class.** For a homogeneous weight `w=U^k φ(s/U)` with φ(1)>0, two fixed regions of speeds A>B have relative weight `z(A)=φ(B/A)/φ(1)`. Where φ increases, increasing A reduces z. Many power and soft-threshold weights therefore share the same reweighting confound. Binary weights avoid continuous reweighting only while their selected support stays unchanged; crossings can still remove fixed exterior components.

**MATHEMATICAL CONSEQUENCE — circulation counterexample.** A smooth fixed spatial swirl `u=A(t)r eθχ(r,z)` with χ=1 near the origin is divergence-free. Set `A(t)=τ^(−1−h)` and evaluate on the prescribed `rτ=sqrt(2Xinτ)` circle. Then its loop speed scales as `τ^(−1/2−h)` and circulation as `τ^(−h)` although the spatial component has fixed shape. This is a kinematic example, not the constructed Navier–Stokes solution; it explains why the prescribed-loop signal alone does not identify geometric narrowing.

## 9. Conditional dominance and observation boundary

**MATHEMATICAL CONSEQUENCE.** For the same U,L claim, signed centered moments contain exactly the information required for the variance error; absolute Dk and TV bounds are sufficient ways to control them and can be strictly more conservative when cancellations are known. This is a conditional information advantage, not proof that the source or DNS supplies signed cancellations. The diameter TV constant improves the old radius constant under the same support information. Neither improvement supplies missing physical inputs.

**MATHEMATICAL CONSEQUENCE.** W2 can certify small geometric displacement even for nearly disjoint translated distributions where TV is maximal. TV can instead be convenient for a small fraction of redistributed mass on bounded support. Direct variance equality can hold for distributions far apart in either metric. No resulting finite error bound is uniformly smallest; the bounded-support norm implications in §6 remain valid. Full covariance also contains the trace exactly under the same distribution assumptions, an advantage in descriptive information that does not remove the mixture counterexample. Quantile, eigenvalue and effective-volume changes make different claims, so declaring one strictly better than L without a common claim would be invalid.

**MATHEMATICAL CONSEQUENCE.** Soft thresholding avoids the boundary-layer premise required for stability of a hard volume. It does not dominate hard volume as a measurement of actual excursion-set volume, because that is a different functional. Alpha-positive full-profile localization strictly supplies a normalization that alpha-zero lacks, but this alone does not select a preferred alpha or operator.

**OPEN CANDIDATE — downstream numerical margins, no feasibility work.** A future observation interface would need independently bounded peak error, positive mass margin, coordinate/crop completeness, and errors in the selected moment, transport, quantile or density functional. To transfer a measured sign to its comparator, numerical error must be added to the two endpoint contamination allowances. For fixed grid spacing Δ, resolving the smallest source scale requires a lower constraint on τ, schematically `τ^(1/2)≥C_res Δ` after any dimensional scale conversion. The source proof gives an upper constraint `τ<τ*`. Their intersection has not been shown nonempty. Shrinking τ to make the analytic error small can worsen spatial and temporal resolution.

**UNSUPPORTED / REJECTED.** No DNS-specific constants, cadence, API contracts, event windows, profile fits or eligibility procedures were examined or certified in this round. Source τ, its dilation, the annular labels, correction stages and auxiliary averages are not directly observed metadata. Their analogues need an independent estimator bridge. Generic turbulent events are not guaranteed to admit the source decomposition even if they can be sampled accurately.

## 10. Finite survivor set: full route tuples

**OPEN CANDIDATE — interpretation of this table.** These six families overlap: some are alternative measurements, others alternative certificates for the same measurement. They are a finite set for reconciliation, not six independent pieces of evidence and not an operator selection. S1 has an established eventual source-side result; the others have the stated mathematical sufficient conditions, not automatically established premises for DNS.

| Survivor | Claim | Assumptions | Source support | Derived bound | Failure mode | Smallest unresolved quantity |
|---|---|---|---|---|---|---|
| **S1 Full-profile positive soft threshold** | Comparator peak up and RMS radius down; covariance widths optional | Fixed α∈(0,1), fixed B containing origin, fixed σ, completed source comparison; independent analogous certificate for any DNS transfer | Theorem 4.6; background expansion; (9.9); (5.35); Proposition 9.9; final localization | `ετ≤Kτ^(h/4)`, `TV≤Cαετ`, `|L²−L_g²|≤C_Lτ^(2d)ετ`; §5 yields τ*>0 | No operational overlap; source profile confused with inner core; favorable event fitting | Operational K,τ0/profile constants and independent event correspondence; **no missing premise for the stated eventual source regime** |
| **S2 Direct signed/relative moment certificate** | Transfer a measured variance drop to a declared comparator | Positive actual mass; independent δm,v,s or relative-weight/tail bounds; separate peak bound | Source decomposition offers candidate terms, but its momentum identities do not equal these moments | Exact signed identity in §6.2; one-sided endpoint intervals | Cancellation asserted without proof; normalization nearly singular; omitted positive tail | Three signed moment bounds (or justified relative bounds) and peak error on the intended region |
| **S3 Transport certificate** | Transfer RMS-radius contraction with less dependence on pointwise density alignment | Independent coupling/cost bound; finite second moments; separate amplitude certificate | Source dilation supplies an ideal transport map; completed-field comparison can imply a conservative cost bound on bounded support | `|L−L_g|≤sqrt(W2²−|δc|²)`; or `2D W1` for squared radius | A fitted transport map explains arbitrary fields; tiny distant mass; amplitude unbounded | Independently justified centered W2 budget or W1 plus support/tails, and peak error |
| **S4 Quantile-radius geometry** | A chosen mass radius decreases, with independently meaningful amplitude growth | Fixed quantile, stable independent center, positive mass, CDF inverse margin; controlled contaminating fraction | Fixed profile and source dilation give ideal ordering; positive α supplies compact ideal mass | Quantile sandwich at q±η; error ≤η/k plus center error when density margin k holds | Component switching, plateau, center dragged by tails; robust amplitude changes source claim | Quantile margin k, center error, contamination budget and amplitude bridge |
| **S5 Concentration-volume family** | Soft, participation or fixed-mass occupied volume decreases, not necessarily widths or component diameter | Fixed weight; support/peak control for V_soft; L²-density/denominator bounds for V_eff; probability bracket for V_b | Fixed-profile change of variables yields determinant scaling | `V∝τ^(3/2−h)` ideally; integral, L² or quantile-volume bounds in §7 | Mixture-only redistribution; separated blobs retain V_eff; high-density spikes; wide quantile bracket | Independently certified error for the selected volume functional and effect; decision whether this weaker geometric claim is useful |
| **S6 Independent reference / component isolation** | Geometry of an independently identified region or amplitude-normalized profile | External amplitude/region/axis information, threshold gap or contamination bound, internal geometry not imposed by mask | Protected source core and annular exclusion exist; no generic DNS identification follows | `H+(1+α)E<αG`; standard moment/quantile bounds after certified restriction | Shrinking mask or fitted normalization encodes the desired contraction; leading exterior wrongly discarded | Noncircular component/reference rule and its errors; proof that the measured geometry is not prescribed by that rule |

**OPEN CANDIDATE — P0, supporting route only.** Protected-circle circulation remains a source-derived amplitude diagnostic with an explicit remainder margin. Its tuple is: claim, inner-loop amplitude/curl-average growth; assumptions, correctly located source loop and bounded remainder; support, (3.6), Proposition 9.9 Step 5 and Stokes' theorem as audited in v0.2; bound, Γ and disk-average formulas in §7; failure, inferred loop/terminal scale or irrelevant global maximum; missing quantity, independently observable loop correspondence and error. It does not replace the contraction half of a joint bridge and is not counted as a seventh full survivor.

## 11. Recommendation, stop and custody

**ESTIMATOR DESIGN CHOICE — next narrower pass, recommendation only.** Reconcile S1–S3 first because they can retain the same U,L measurement while changing only the certificate. Independently check the §4 source-to-uniform-bound assembly and §5 fixed-ratio interval, then compare the exact signed-moment and centered-transport certificates against that baseline for the same claim and available source inputs. Eliminate routes that add unobservable assumptions without a proved improvement. Keep S4–S6 only if they buy a clearly stated claim or assumption advantage; otherwise demote them. Separate the source-side existence result from operational and inner-core requirements. That pass should reconcile and eliminate this finite inventory, not launch more broad exploration, choose event windows, implement an estimator or acquire data. It has not started.

**ESTIMATOR DESIGN CHOICE — stop.** R5's three workstreams are closed for this expansion receipt. No final operator is selected. No authorization is transferred to another phase.

Custody is administrative evidence, not scientific support. The Ultra entry snapshot was retained across interruption and verified again on resumption: no intervening additions, removals or byte changes. Before/after comparison covers all 29 pre-existing non-Git regular files: 22 tracked, five untracked prior E1 receipts, and two ignored bytecode files. All are preserved unchanged. Prior hashes, including the R4 hash, were checked directly; none was inferred from memory.

- Branch: `codex/e0-h2-preparation`.
- HEAD: `711b6c7f0cfd1c69694bff8a3fd134b585e633df`, unchanged.
- Frozen E0 SHA-256: `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`, matches its unchanged sidecar.
- R4 SHA-256: `62fa138fd984baf2f598c4cf6c469109dd6ebe3bdc16b8bcfdb2817c7f3bd539`, unchanged.
- Exact new repository file: `docs/e1-openai/NS-001_E1_ULTRA_ANALYTICAL_EXPANSION_RECEIPT_v0.1.md`.
- Tracked files changed: **NO**. Staged and tracked worktree diffs are empty.
- A byte-identical delivery copy is in the current task's outputs directory. The retained custody snapshot and draft are outside the repository in work/.

Final `git status --short --untracked-files=all`:

```text
?? docs/e1-openai/NS-001_E1_CONTAMINATION_BRIDGE_AUDIT_v0.1.md
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.1.md
?? docs/e1-openai/NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.2.md
?? docs/e1-openai/NS-001_E1_OPERATOR_CONFOUNDING_AUDIT_v0.1.md
?? docs/e1-openai/NS-001_E1_ULTRA_ANALYTICAL_EXPANSION_RECEIPT_v0.1.md
?? docs/e1-openai/NS-001_E1_WORKFLOW_MAP_v0.1.md
```

Only the Ultra receipt is new this round. All other untracked files predate it. No experiments, simulations, JHTDB queries, scientific code/tests, commits or pushes occurred. These checks establish this task's byte custody and actions, not a historical audit of external execution.

E0: **FROZEN / HOLD**.

Gate 1: **PARTIAL**.

Run authorization: **NOT GRANTED**.
