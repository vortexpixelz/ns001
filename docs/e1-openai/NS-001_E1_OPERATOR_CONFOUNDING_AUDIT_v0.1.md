# NS-001 / E1 Operator Confounding Audit v0.1

Phase 1 · Round R3 · one bounded analytical circuit

## 1. Question, decision and scope

**Question:** does the v0.2 U–L signature distinguish geometric contraction from relative-amplitude/background changes sufficiently to justify further bridge work?

**Operator-route decision: RETAIN CONDITIONALLY.** The unrestricted sign pair does **not** distinguish those explanations. An explicit counterexample below gives U↑ and L↓ with fixed spatial components and even fixed positive-weight support. Removing the threshold does not cure the confounding. The unchanged operator merits one further source-side bridge round only under restriction 2: independently bounded departure from a single geometric profile. That restriction is not yet established for the source-selected region or for DNS. This is permission to recommend further analytical work, not operator validation, an authorization to start it, or a Gate 1 PASS.

Exactly two alternatives/restrictions are considered. No estimator search, control design, empirical data access, simulation or scientific code execution occurred. All counterexamples are analytic constructions, not observed flows or numerical evidence. v0.1 and v0.2 are preserved, not amended.

**Labels:** SOURCE FACT; MATHEMATICAL CONSEQUENCE; DESIGN CHOICE; UNRESOLVED ASSUMPTION. Rejected implications are identified explicitly. Mathematical calculations below are original deductions about the operator, not statements attributed to the paper.

## 2. Operator under audit and the case it already handles

**DESIGN CHOICE — inherited from v0.2, §4.** In one fixed, unwrapped window, with fixed α=1/2,

`s=|u|`, `U=sup s`, `w=[s²−α²U²]+`,

`m=∫w dx`, `p=w/m`, `c=∫x p dx`,

`Q=∫(x−c)(x−c)ᵀ p dx`, `L²=tr Q`.

The discrete operator replaces integrals by equal-volume native-grid sums. The window/frame/periodic rules remain those of v0.2. Here the continuum version permits exact algebra; the same mixture identity holds for symmetric discrete node sets with different inner/outer mean squared radii.

**MATHEMATICAL CONSEQUENCE — uniform amplitude invariance.** For any scalar `g(t)>0` multiplying the *entire* velocity field in the same window,

`s'=g s`, `U'=g U`, `w'=g²w`, `m'=g²m`, `p'=p`.

Therefore `c'=c`, `Q'=Q`, `L'=L` exactly, in both the continuum and discrete definitions. Pure uniform amplification produces U↑ but cannot produce L↓. The confound at issue is **changing relative amplitudes of fixed components**, not the mere presence of U in the threshold.

This invariance assumes identical coordinates, coverage, α and frame, with positive mass. A time-dependent change of window or an additive background velocity is not uniform multiplication.

## 3. Explicit fixed-geometry counterexample

### 3.1 Geometry and velocity

**MATHEMATICAL CONSEQUENCE — construction assumptions.** Use cylindrical coordinates `(r,θ,z)` and choose fixed lengths `0<a<b<R`. Let

`Tq={R−q<r<R+q, |z|<q, 0≤θ<2π}` for `q=a,b`.

These are solid rings with rectangular meridional cross-sections, bounded away from the axis. Put `C=Ta` and `O=Tb\Ta`. Embed Tb strictly inside the fixed observation cube, with a fixed exterior margin. No wrapping, clipping or movement is involved.

For fixed `B>0` and varying `A(t)` satisfying

`B<A(t)<B/α`, `dA/dt>0`,

define the tangential velocity

`u_A(x)=[A 1C(x)+B 1O(x)] eθ`, zero outside Tb.

The two component shapes C and O, all their radii/thicknesses, and their centroids remain fixed. Only the inner speed changes. The field is azimuthally invariant and divergence-free in the distributional sense: its jumps have normals in the `(er,ez)` plane and no normal velocity. It is not initially smooth; §3.4 explains the smooth version. No claim is made that this is the paper's solution, a stationary turbulent trajectory, or a counterexample to Navier–Stokes regularity.

### 3.2 Exact moments and sign

**MATHEMATICAL CONSEQUENCE.** `U=A`. For all A in the chosen interval, weights are

`wc=(1−α²)A²>0` on C,

`wo=B²−α²A²>0` on O,

and zero outside Tb. The entire positive-weight support is the **same connected Tb at every time**. Thus the effect does not require deleting outer nodes, changing topology or splitting structures.

Rotational symmetry and z-reflection give weighted centroid zero. Integrating `dx=r dr dθ dz` yields

`Vq=vol(Tq)=8πR q²`,

`μq=(1/Vq)∫Tq |x|² dx=R²+4q²/3`.

Let `Vc=Va`, `Vo=Vb−Va`. Then

`μc=R²+4a²/3`,

`μo=(Vb μb−Va μa)/(Vb−Va)=R²+4(b²+a²)/3`,

so `μo−μc=4b²/3>0`.

Consequently

`L²(A)=(Vc wc μc+Vo wo μo)/(Vc wc+Vo wo)`.

Define the weight ratio

`z(A)=wo/wc=(B²/A²−α²)/(1−α²)`.

Then

`dz/dA=−2B²/[(1−α²)A³]<0`,

`dL²/dz=Vc Vo(μo−μc)/(Vc+Vo z)²>0`.

Hence `dL²/dA<0` and `dL/dt<0`, while `dU/dt=dA/dt>0`. Every component scale is constant. This proves the sign pair without relying on a verbal illustration.

**MATHEMATICAL CONSEQUENCE — exact finite example.** Choose `α=1/2`, `a=ℓ`, `b=2ℓ`, `R=4ℓ`, and compare `A1=4B/3` with `A2=5B/3`. Then `Vo/Vc=3`, `z1=5/12`, `z2=11/75`, `μc=52ℓ²/3`, and `μo=68ℓ²/3`. Substitution gives

`U2/U1=5/4`,

`L1²=548ℓ²/27`, `L2²=512ℓ²/27`,

`L2/L1=√(128/137)<1`.

The squared size falls by `4ℓ²/3`. The true support and both component geometries do not change. These values were derived symbolically; no numerical field was generated or sampled.

### 3.3 Why the v0.2 screens do not establish specificity

**MATHEMATICAL CONSEQUENCE.** The example has a fixed center, connected positive support, a fixed frame, no crop loss and no translation. Arbitrarily accurate measurement of its moments would still show the misleading sign pair. Rank/conditioning and resolution safeguards protect measurement accuracy; they do not distinguish amplitude redistribution from shape deformation.

The construction is an operator counterexample, not a claim that this particular choice of ℓ passes every numerical engineering screen of the 65³ proposal. No discrete adequacy certificate is asserted. Its force is that even the exact continuum functional cannot make the proposed interpretation from the two signs alone. Symmetric discrete inner/outer sets with `μo>μc` obey the same derivative identity, independently of integration error.

### 3.4 Smoothness does not rescue the inference

**MATHEMATICAL CONSEQUENCE.** Replace the fixed indicators by fixed smooth, axisymmetric nested cutoffs `φa,φb`, compactly supported away from `r=0`, with `φb=1` on the support of φa and nonempty inner plateaus. Define

`u_A,ε=[B φb,ε+(A−B)φa,ε]eθ`.

This is smooth, compactly supported and exactly divergence-free. Its component functions and transition thickness ε are fixed throughout the amplitude change. `U=A` on the inner plateau. As ε→0 the fields are bounded and converge almost everywhere to the piecewise field for each fixed A. The soft weights converge in L1; their first and second moments converge on the bounded cube, and their mass stays positive. Therefore the strict finite difference `L(A2)<L(A1)` survives for all sufficiently small **fixed** ε, while both component shapes remain fixed. This establishes the needed two-time counterexample without claiming a monotone derivative for every smoothed profile throughout the interval.

If embedded inside a periodic cell with exterior zero margin, the smooth field can be extended periodically. That is a kinematic compatibility observation, not a claim about DNS dynamics or admissible forcing. No simulation is needed for the operator's non-identifiability conclusion.

## 4. What the counterexample defeats and preserves

**REJECTED INTERPRETATION.** From “U increased and the relative-speed-weighted L decreased” alone one cannot infer that an underlying velocity component narrowed, that the paper's similarity core contracted, or that a construction-specific mechanism was present. Connectedness and centroid stability do not repair that inference. Even support deletion is unnecessary: reweighting alone suffices.

**MATHEMATICAL CONSEQUENCE — weaker true description.** The normalized speed-excess distribution became more concentrated in the precise second-moment sense defined by this operator, while local maximum speed increased. That is a genuine change of an intensity distribution, not a false numerical calculation. Calling it physical contraction of a component adds an unproved identification step. It is also not evidence for singularity, the theorem or generic velocity–vorticity scaling.

**SOURCE FACT.** The paper defines its inner core by fixed similarity coordinates and gives shrinking radial/axial extents; it does not define that core as a speed-excess probability distribution. [P, §3.1 p. 8, equations (3.2), (4.1)–(4.3)] The mismatch is exactly why the identification step requires proof.

## 5. Two options only

### Option 1 — fixed-mask, unthresholded speed-squared moments

**DESIGN CHOICE.** Replace the weight with `w0=s² 1Bwindow`, keeping the same complete fixed window, centroid and normalization. This removes the moving relative threshold; it is not adopted.

**MATHEMATICAL CONSEQUENCE.** In the same counterexample, `wc=A²`, `wo=B²`, so `z0=B²/A²` still decreases strictly. The same mixture derivative gives `dL0²/dA<0`. The confounding persists: a central component acquires more probability weight relative to a broader component. The failure is not specific to α=1/2 or to a positive threshold.

**SOURCE FACT / LIMIT.** Weighted velocity moments are compatible with discussing spatial concentration, but the paper's core and fixed final support are distinct [P, §3.1 p. 8; Proposition 10.1]. It does not supply a theorem that full-window energy moments isolate its inner core.

**UNRESOLVED ASSUMPTIONS.** This option would still require a fixed frame, complete localization and a separation/bound for other components, with additional sensitivity to distant low-speed mass. A window or background chosen to make the moment contract would be circular. Even a prospectively fixed mask does not remove the demonstrated mixture effect.

**Disposition:** reject as a cure in this round. The missing proof remains component isolation/moment inheritance. Changing only the weight would relocate the problem and justify no new implementation.

### Option 2 — restrict the unchanged operator to an independently bounded geometric component

**DESIGN CHOICE.** Keep the current weight and α. For *further source-side validation*, require a justified representation on the full weighted region

`u(x,t)=A0(t) R(t) v0(D(t)^−1 R(t)ᵀ[x−c0(t)])+e(x,t)`.

Here `v0` is one fixed vector profile, `D=diag(lr,lr,lz)`, `R` an orthogonal spatial rotation, and e contains ambient contributions and departures from the profile. “Ambient” here means unwanted contributions to the DNS measurement; the paper's desired background vortex `uB` is not something to subtract. No fitted background subtraction or moving Galilean frame is introduced. A spatially rotating coordinate/profile representation is not a subtraction of the frame's velocity.

**MATHEMATICAL CONSEQUENCE — exact case.** If `e=0`, the window contains the complete positive-weight region and its peak, and the profile has finite nonzero weighted moments, changing variables gives

`U=A0 sup|v0|`,

`c_weight=c0+R D μ0`,

`Q=R D Q0 D Rᵀ`.

The common factor `A0² det D` cancels from normalized moments. With D fixed, changes of A0 cannot alter L; the demonstrated relative-amplitude counterexample is excluded rather than corrected after observation. With the source's fixed-profile radial/axial contraction and positive profile moments, trace decreases. For axisymmetric Q0, `L²=2cr lr²+cz lz²`, as in v0.2. This is a conditional model identity, not a DNS identification theorem.

**MATHEMATICAL CONSEQUENCE — bounded contamination.** Let p be the actual normalized soft weight and pg the corresponding ideal geometric-profile weight. Suppose both are contained in a fixed ball of radius Rw in the unwrapped chart and an independent analysis establishes `TV(p,pg)≤η`. Then

`|L²−Lg²|≤6 Rw² η`.

Indeed the raw second-moment trace changes by at most `2Rw²η`; the mean changes by at most `2Rwη`; and the squared mean norm changes by at most `4Rw²η`. This bound includes centroid movement. Therefore a measured squared-size drop must exceed the sum of the two endpoint contamination bounds **and** numerical-error bounds before it can be attributed to a decrease of the ideal profile moment. A corresponding sup-norm remainder bound is needed to attribute U's change to A0.

**UNRESOLVED ASSUMPTION — essential.** η cannot be estimated by declaring the observed contracting part “the core,” fitting a profile to maximize agreement, or selecting only windows with the desired sign. A small velocity error alone is not a normalized-moment bound when total weight is small or spatial tails are large. The representation, peak/mass/tail bounds, component assignment, fixed laboratory frame and error allowances must be supplied independently of the tested U–L outcome. No such DNS qualification procedure is specified or validated here.

**SOURCE FACT.** There is a principled reason to investigate this restriction rather than invent another estimator: the source already supplies fixed profiles in similarity coordinates [P, (3.2), (4.1)–(4.3)] and componentwise background remainder estimates on specified profile rectangles [P, Proposition 5.5, (5.42)]. The inner growth path is preserved in the completed field [P, Proposition 9.9 Step 5 p. 116; (3.6)]. Those facts do not establish a whole-region normalized moment bound for the current weight, nor do they make e negligible in DNS.

**Exact remaining proof:** bind this representation to the actual source-field operator; prove complete weighted-region localization, positive mass and peak control; bound exterior, radial-component and pulse/correction contributions in zeroth and second moments; and determine whether a nontrivial bound survives at finite scales. Separately, any eventual DNS use requires an outcome-independent way to certify its assumptions. The source proof alone cannot certify a stationary turbulent event.

**Disposition:** retain conditionally for one recommended analytical bridge round. This restriction eliminates the demonstrated confound only when its independent bounds are true. Without those bounds it merely renames the unknown mixture and provides no protection. Defeating one counterexample is not validation.

## 6. Circuit decision and stop

| Circuit step | Completed result |
|---|---|
| Question | Does the unchanged U–L pair identify geometric contraction rather than amplitude reweighting? |
| Work | Proved uniform-rescaling invariance; derived a fixed-geometry counterexample and its smooth extension; assessed exactly two options. |
| Evidence receipt | This document: explicit integral identities, derivative signs, finite example, conditional covariance identity and contamination bound. No empirical evidence claimed. |
| Decision | **RETAIN CONDITIONALLY**, restricted to independently justified geometric-profile/contamination bounds. Unrestricted contraction inference is rejected; threshold removal is rejected as a cure. |
| Stop | End R3 here. Recommend, but do not start, R4's source-side contamination/localization proof. Gate 1 remains PARTIAL. |

This decision concerns an operator route. It neither challenges the source theorem nor dismisses NS-001. No data-feasibility blocker is removed by the route decision, and no gate is passed by moving it to another phase.

## 7. Source and preservation register

**[P] SOURCE FACT.** [OpenAI, Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf). Retained PDF hash reverified: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. Exact relevant locators: §3.1 pp. 7–8 and (3.2); Theorem 3.1(iv), (3.6) p. 16; §4.1, (4.1)–(4.5) pp. 24–25; Proposition 5.5, (5.41)–(5.43) pp. 59–60; Proposition 9.9 Step 5 p. 116; Proposition 10.1 on spatial localization. Only targeted source locations were revisited; completed broad research was not repeated.

**[V2] DESIGN RECORD.** [Derivation receipt v0.2](NS-001_E1_OPENAI_GATE1_DERIVATION_RECEIPT_v0.2.md), §§3–5 for the conditional bridge, operator and unresolved resolving power. Entry hash `a0dffb46343beb7cc226cffb49c742619281675af80992a6314639f8a3137ee3`. Preserved unchanged.

**[MAP] GOVERNANCE ORGANIZATION.** [Workflow map v0.1](NS-001_E1_WORKFLOW_MAP_v0.1.md) records the recovered state, original gates, proposed phase placement and scope drift. It grants no approval.

**Preservation receipt.** All pre-existing tracked files and both derivation receipts retain their entry hashes. Only the map and this audit were added. No repository code, scientific code, tests, simulations or JHTDB data queries were executed. No implementation changes, commit or push. Exact tracked/untracked status is recorded in the companion map.

E0: FROZEN / HOLD.

Gate 1: PARTIAL.

Run authorization: NOT GRANTED.
