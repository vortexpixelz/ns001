# NS-001 / E1 R7: S1 versus S2 signed-moment certification v0.1

21 September 2026 · Phase 1 / Gate 1 · one bounded scientific review

## 1. Decision, identities and scope

**MATHEMATICAL CONSEQUENCE — comparative decision.** Under the currently verified source assumptions, S1 supplies the already established joint U/L endpoint certificate. S2 supplies a correct exact variance-error identity and can inherit an eventual endpoint certificate from those same assumptions, but no additional signed information or strictly better source-supported error bound has been established. S1 is the evidence-complete baseline; this is not a theorem that it universally dominates S2. S2 can exploit separately proved cancellations, but those cancellations must not be inferred from their desirability or from unrelated source moments. Neither route materially strengthens the scientific claim beyond R6 in this circuit. Gate 1 remains PARTIAL.

**MATHEMATICAL CONSEQUENCE — nomenclature and unchanged claim.** The preserved R5 inventory defines S1 as the full-profile positive-soft-threshold route and S2 as the direct signed/relative-moment route. S1 is not a second signed-moment formula. This review compares those existing routes, without relabeling them or changing the operator. The common source-conditioned claim is: for the completed construction, fixed 0<sigma<1 and sufficiently small tau, local peak U increases and speed-excess RMS radius L decreases between remaining times tau and sigma tau. The comparator is the complete leading tangential profile, not an identified DNS component or the designated inner core.

Entry checks passed: branch `codex/e0-h2-preparation`, HEAD `f685e6470a7c3a864aa33885e66b6e16975d3992`, clean tracked/untracked tree and completed R6 receipt present with SHA-256 `c3d2217938df1f0813ac4d6a0841970c87baf5912d8b50efad8c636fc21699e4`. R5 SHA-256 is `52d718b54068481ba1fcac21259be6795777e108dea02e8a4fcc8b5609833084`. Those records are inputs, not conclusions that this comparison must favor.

**PAPER-DERIVED — source register.** [P], OpenAI, [Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), was retrieved into temporary storage and its PDF SHA-256 independently matched `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. Source identities relevant to claimed cancellation were reread at (6.24)-(6.29), pp. 69-70; Proposition 8.1, p. 89; and (9.7)-(9.10), p. 106. R6's checked source-to-uniform-bound result is the inherited verified premise; this circuit does not redo the entire construction audit. No source-paper assertion about momentum is treated as an assertion about the new weighted quantities below.

No estimator, scientific code, simulation, test suite, target-data inspection, JHTDB query, H2A2 work or E0 execution occurred. Existing operator conventions and every earlier artifact remain unchanged. This is paper-and-algebra review; administrative PDF retrieval, extraction, hashing and Git preservation are distinct.

## 2. Common mathematical objects and the available evidence

**MATHEMATICAL CONSEQUENCE — definitions.** Integrals below are over the same fixed physical window B, in the same fixed velocity frame. Let u be the completed source field and g its independently specified complete leading tangential comparator. Use the inherited fixed alpha=1/2; formulas remain valid for any fixed alpha in (0,1), without authorizing a threshold change:

`U=sup_B |u|`, `G=sup_B |g|`,

`w=[|u|^2-alpha^2 U^2]+`, `w_g=[|g|^2-alpha^2 G^2]+`,

`m=integral w`, `m_g=integral w_g`, `p=w/m`, `p_g=w_g/m_g`,

`c=integral x p`, `c_g=integral x p_g`,

`L^2=integral |x-c|^2 p`, `L_g^2=integral |x-c_g|^2 p_g`.

Positive masses and finite second moments are required whenever these normalized quantities are used. No signed measure is interpreted as a probability distribution.

**PAPER-DERIVED — source inputs used through R6.** The source fixes h>0 under nested restrictions (in particular h<1/100), similarity variables and profiles, finite-stage amplitude bounds, summation cutoffs and final localization. Relevant locations are (4.1)-(4.5), Theorem 4.6 and Lemma 4.8; Lemma 5.4 and Proposition 5.5; (9.9), Proposition 9.9; Proposition 10.1. Smoothness alone is not substituted for the uniform estimates or the endpoint bounds away from concentration.

**MATHEMATICAL CONSEQUENCE — R6 premises.** Put `a=1/2+h`, `d=1/2-h`, `beta=h/4`, and `D_tau=diag(tau^(1/2),tau^(1/2),tau^d)`. R6 establishes, conditional on those source statements,

`epsilon_tau := sup_(D_tau^(-1)B) |tau^a |u(D_tau y,1-tau)|-F(y)| <= K tau^beta`,

`G=tau^(-a) M`, `m_g=tau^(1/2-3h) m_F`,

`L_g^2=2c_r tau+c_z tau^(2d)`, with `M,m_F,c_r,c_z>0`.

For sufficiently small tau, both positive weights are supported in `D_tau K_alpha`, inside B. Let `D_alpha=diam(K_alpha)`, `D(tau)=D_alpha tau^d`, and `rho(tau)=C_alpha epsilon_tau`. Then

`D0 := integral |w-w_g| <= m_g rho`, `rho<1`,

`|U-G|<=tau^(-a) epsilon_tau`, `TV(p,p_g)<=rho`.

These bounds retain the shrinking mass and support. K, the validity thresholds, and profile constants are finite but not numerically certified. h, B, alpha and sigma are fixed before the smallness threshold is chosen; no uniformity in their limiting values is implied.

## 3. S1: what is certified and why it survives

**MATHEMATICAL CONSEQUENCE — quantity and bound.** S1 certifies the joint source-field endpoint directions by controlling the unsigned peak error and the centered variance error:

`|L^2-L_g^2| <= D(tau)^2 rho(tau) = C_L tau^(2d) epsilon_tau`,

where `C_L=D_alpha^2 C_alpha`. The variance inequality follows by evaluating each variance about the other distribution's centroid and bounding the difference of expectations of a function ranging over an interval of length at most D(tau)^2. The TV convention is half the L1 distance. Centroid movement is included.

**MATHEMATICAL CONSEQUENCE — available signs.** The comparator endpoint differences have known strict signs. With `tau_2=sigma tau_1`,

`G_2-G_1=M tau_1^(-a)(sigma^(-a)-1)>0`,

`Delta_g := L_g,1^2-L_g,2^2`

`=2c_r tau_1(1-sigma)+c_z tau_1^(2d)(1-sigma^(2d))>0`.

The errors need not have either sign. If Delta_g exceeds both size-error allowances and the amplitude gap exceeds both peak-error allowances, then `L_2<L_1` and `U_2>U_1`. R6 proves a nonempty symbolic interval on which both conditions hold. Cancellation cannot defeat this inference because the inequalities allow the worst signs at both endpoints. An error bound alone, without these margins, would not prove the directions.

**MATHEMATICAL CONSEQUENCE — status and minimal premises.** S1 requires the complete-profile comparison, peak inclusion, positive mass, relevant-support enclosure and fixed-ratio error margin. Source cutoff and Cartesian regularity assumptions enter through R6. No derivative of L, threshold-surface regularity, or new transversality assumption is required. The result is an eventual existence theorem with an explicit symbolic sufficient bound; it is not a usable numerical time range without values or certified bounds for its constants. S1 adds no directional result beyond R6.

## 4. S2: independent derivation, signs and inherited bounds

### 4.1 Exact identity and normalization

**MATHEMATICAL CONSEQUENCE.** Define the signed weight difference and its moments about the comparator centroid:

`delta w=w-w_g`, `delta m=integral delta w`,

`v=integral (x-c_g) delta w`, `s=integral |x-c_g|^2 delta w`,

`A=s-delta m L_g^2 = integral (|x-c_g|^2-L_g^2) delta w`.

Since the comparator's first centered moment vanishes,

`m=m_g+delta m`, `c-c_g=v/m`.

The actual second moment about c_g is `(m_g L_g^2+s)/m`. Subtracting the squared centroid shift gives the exact identity

`delta := L^2-L_g^2 = A/m - |v|^2/m^2`.

Thus S2 directly certifies a **signed variance error**, not geometric narrowing by itself and not the peak U. Its elementary identity needs only positive masses and finite second moments, not differentiability or a particular PDE. Smoothness of the constructed field is sufficient but is not an extra assumption of this identity.

**MATHEMATICAL CONSEQUENCE — dimensions.** If physical length and time units are L and T, then `[w]=L^2/T^2`, `[m]=L^5/T^2`, `[v]=L^6/T^2`, and `[s]=[A]=L^7/T^2`. Both A/m and |v|^2/m^2 have units L^2. The source powers of tau concern its nondimensional construction coordinates; they are not a dimensional map to DNS. Omitting the factor m or replacing it by m_g without an error argument changes the identity.

### 4.2 What signs actually follow

**MATHEMATICAL CONSEQUENCE.** The only unconditional sign in the identity is `-|v|^2/m^2<=0`. Neither delta m, s, A nor delta has a sign from the R6 norm bounds. Even if A=0, a changing centroid contribution can make an apparent variance decrease. Even if s=0, the mass-normalization term and centroid term remain. A bound on delta m alone cannot control A.

**MATHEMATICAL CONSEQUENCE — two distinct endpoint inferences.** Let `l_i<=delta_i<=u_i`, with indices 1 and 2 denoting earlier and later physical times. Then

`Delta := L_1^2-L_2^2 = Delta_g+delta_1-delta_2`.

For **comparator-to-field** certification, the common forward claim here,

`Delta_g > u_2-l_1` implies `Delta>0`.

For **field-to-comparator** certification,

`Delta > u_1-l_2` implies `Delta_g>0`.

These margins are reversed, not interchangeable. R5 §6.2's stated observed-to-comparator margin is correct, but it is not by itself a proof of the forward source-field claim. A negative centroid term at one endpoint cannot simply be called favorable: its earlier-minus-later difference can have either sign. Peak certification must still be supplied separately.

### 4.3 What S2 obtains from the same verified inputs

**MATHEMATICAL CONSEQUENCE.** Because c_g lies in the convex hull of the combined support, `|x-c_g|<=D(tau)` there and `0<=L_g^2<=D(tau)^2`. Consequently R6 implies

`|delta m|<=m_g rho`, `|v|<=D(tau) m_g rho`,

`|A|<=D(tau)^2 m_g rho`, `m>=m_g(1-rho)>0`.

The centered kernel in A has absolute value at most D(tau)^2; it is not necessary to add two independent upper bounds for s and delta m L_g^2. Substitution gives the valid conservative interval

`-D(tau)^2 rho/(1-rho)^2 <= delta <= D(tau)^2 rho/(1-rho)`.

The negative centroid term is at most order `D(tau)^2 rho^2/(1-rho)^2` in magnitude. Thus the leading inherited scale remains

`delta=O(tau^(2d+beta))`, with the centroid-square allowance `O(tau^(2d+2beta))`.

Also `delta m=O(m_g tau^beta)`, `v=O(m_g tau^(d+beta))`, and `A=O(m_g tau^(2d+beta))`. These orders account for `m_g=tau^(1/2-3h)m_F`; absolute smallness without normalization would not suffice.

**MATHEMATICAL CONSEQUENCE — comparison on identical evidence.** Using D(tau) and rho from R6, this particular S2 envelope is no tighter than the S1 interval `[-D(tau)^2 rho,+D(tau)^2 rho]`. Intersecting the two retains S1. The S2 identity is exact; the loss arises from replacing unknown signed quantities by absolute bounds. This computation does not prove that every possible refinement of S2 is inferior, only that this source-supported derivation provides no guaranteed improvement over the verified S1 bound.

Since rho tends to zero, one can choose rho<1/2 and make these S2 endpoint allowances smaller than the fixed-ratio comparator drop. Together with the inherited peak bound, S2 therefore also recovers eventual joint U/L ordering, potentially on a smaller sufficient interval. It does not produce a second independent line of source evidence: the quantitative inputs came from S1/R6.

### 4.4 Source cancellations do not supply the missing signed data

**PAPER-DERIVED.** Equations (9.7)-(9.10) distinguish angularly averaged waves, auxiliary-averaged velocity corrections, and their momentum/flux constraints. The source maintains integrals of the form `integral R^2 <v_source>_Y dR=0` and `integral R <gamma_source>_Y dR=0`. Here v_source is the paper's azimuthal velocity correction, not the vector v defined above. Proposition 8.1 retains wave covariances even when terms linear in a zero-angular-mean wave integrate to zero.

**MATHEMATICAL CONSEQUENCE.** The soft-weight change involves the positive part of

`|g|^2-alpha^2 G^2 + 2g dot e+|e|^2-alpha^2(U^2-G^2)`, where `e=u-g`.

A zero average of a velocity component need not annihilate its square, a spatially weighted cross term, the peak shift, or the threshold-selected domain. Physical spatial integration after auxiliary evaluation is also not automatically the source's auxiliary Haar average. Even genuine unthresholded angular cancellation does not justify moving it through the positive-part operation. No cancellation of delta m, v or A is established by those source constraints.

**UNSUPPORTED / REJECTED.** Setting these signed weight moments to zero, assigning a favorable sign to A, improving its decay order, or dropping the threshold/centroid contribution solely on the basis of zero momentum, flat residual, finite energy or oscillatory terminology is invalid. Radial/tangential orthogonality can eliminate a particular cross term before thresholding; it does not eliminate all other terms or certify the sign of the final variance error.

**MATHEMATICAL CONSEQUENCE — logical failure example, not a source-flow counterexample.** Transfer a small amount of nonnegative weight between two symmetric populations at different distances from c_g, keeping total weight and first moment fixed. Then delta m=0 and v=0, while s and delta can be positive or negative according to transfer direction. Such examples can be realized with smooth symmetric bumps inside a region of positive baseline weight. They show why zero low-order moments alone do not fix the variance sign; they are not claimed to satisfy the entire source construction. Cancellations among pieces of delta w are legitimate only when the complete A, v and mass are bounded after summing every contribution.

### 4.5 Relative-weight subroute and missing amplitude information

**MATHEMATICAL CONSEQUENCE.** If independently proved bounds give `(1-r)lambda w_g<=w<=(1+r)lambda w_g`, with lambda>0 and 0<=r<1, set `kappa=(1+r)/(1-r)`. Integrating bounds m, and normalizing gives `kappa^(-1)p_g<=p<=kappa p_g`. Minimizing second moments over the center then gives

`kappa^(-1)L_g^2<=L^2<=kappa L_g^2`.

The common amplitude factor lambda cancels. A sufficient forward endpoint condition is `L_g,1^2/L_g,2^2>kappa_1 kappa_2`. This is a sound alternative sufficient condition, not an inherited R6 premise.

**UNSUPPORTED / REJECTED.** Uniform absolute speed error does not supply a pointwise relative-weight bound near `w_g=0`. The multiplicative premise forces w=0 wherever w_g=0, whereas R6 only encloses both supports in the same larger compact set. Small perturbations may activate weight near an ideal threshold. No level-set gap, transversality or relative domination can be silently added to bridge this difference.

**MATHEMATICAL CONSEQUENCE.** Neither the exact signed variance identity nor relative normalized-weight control supplies U's direction. Under uniform velocity amplification, normalized moments may be unchanged while U changes. A narrow spike can alter U strongly with little mass. The currently justified amplitude certificate remains the separate source peak estimate inherited from R6. Dropping it would fail to certify the joint claim.

## 5. Comparative result and surviving assumptions

| Classification | Comparison dimension | S1 | S2 |
| --- | --- | --- | --- |
| MATHEMATICAL CONSEQUENCE | Exact target | Peak error and centered-variance error sufficient for joint endpoint ordering | Exact signed variance error; separate peak certificate required |
| MATHEMATICAL CONSEQUENCE | Currently available evidence | Uniform speed/peak comparison, positive mass, shrinking-support and TV bounds already established | Same inputs imply conservative signed-moment envelopes; improved signed intervals are not currently supplied |
| MATHEMATICAL CONSEQUENCE | Cancellation | Worst-sign bound remains valid without cancellation | Can preserve proved cancellation; cannot assume it. Centroid and normalization terms must remain |
| MATHEMATICAL CONSEQUENCE | General algebraic premises | Support/TV information for the displayed variance certificate, plus peak bounds | Finite positive masses and second moments suffice for the identity; rigorous error intervals and peak information are required for certification |
| MATHEMATICAL CONSEQUENCE | Source dependence | Fixed h, source coefficients/cutoffs, B, alpha, sigma and sufficiently small tau | Inherited existence result uses those same premises. A genuinely independent S2 certificate could replace uniform control with justified moment/tail bounds, but they are absent here |
| MATHEMATICAL CONSEQUENCE | Quantitative force now | Symbolic sufficient inequalities and a nonempty eventual interval | Exact symbolic identity plus an inherited eventual interval; no certified larger interval or smaller error |
| UNSUPPORTED / REJECTED | Operational force | No finite-grid/DNS certificate | No finite-grid/DNS certificate; lower-dimensional moments do not create missing numerical constants or event correspondence |
| MATHEMATICAL CONSEQUENCE | Increment beyond R6 | None in the source directional claim | Clarified normalization, forward/reverse margins and inherited bounds; no stronger scientific conclusion |

**MATHEMATICAL CONSEQUENCE — dominance statement.** There is no established strict mathematical dominance of the route families. Given exact independently known delta m, v and s, S2 determines the variance error exactly and can beat a coarse S1 upper envelope; for instance proportional weights have unchanged normalized variance even when their absolute weight difference is nonzero. That is a conditional information advantage, not current source evidence. Conversely, S1 already certifies the joint claim without needing such signed information. Exact distribution information sufficient for S1 could itself recover the signed moments; these routes are overlapping certificates, not independent experiments. On the *currently verified* inputs, S1 is the justified baseline and S2 adds no proved improvement.

**NEEDS ADDITIONAL SOURCE CHECK.** Any claimed S2 improvement requires a source-specific bound on `A/m-|v|^2/m^2` at the two endpoints, or independently justified signed moment intervals/relative-weight inequalities that improve the S1 allowance while preserving the same peak claim. The cited momentum constraints do not furnish them. This review does not claim such an improvement is impossible, and it does not initiate a search for an altered operator or new regularity hypothesis.

**UNSUPPORTED / REJECTED.** Neither route certifies inner-core identification, arbitrary physical-component narrowing, mechanism specificity, continuous-time monotonicity, arbitrary-close-pair ordering, a numerical crossover or a DNS-resolvable operating range. Unknown constants and asymptotic upper bounds on tau have not been converted to a finite-resolution certificate. No additional Gate 1 evidence is created by counting S1 and S2 as two supporting routes when their inputs are the same.

## 6. Preservation and closure

The baseline contains 36 pre-existing non-Git regular artifact files, including two ignored bytecode caches. Their exact bytes remain unchanged. The only addition is this R7 receipt. The frozen E0 preregistration and sidecar retain SHA-256 values `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78` and `0e1e5900aec22a55332c1bde18147c3f2ff5a55351a8d1bec6e504b3eb960de8`, respectively. No scientific or implementation test run is claimed. Commit/push is the user-authorized preservation step after the final byte check, not a gate decision; its outcome is reported separately rather than pre-claimed here.

- **S1 verdict:** SURVIVES as the source-conditioned, evidence-complete baseline for the existing fixed-ratio continuum U-up/L-down claim; no promotion to a final operator.
- **S2 verdict:** Exact signed/relative-moment algebra SURVIVES. Inherited source bounds recover eventual certification, but no independent cancellation advantage, sharper source-specific bound or joint amplitude certificate beyond R6 is established. Relative-weight domination remains an additional unverified premise, not a consequence of S1.
- **Whether either route strictly dominates the other mathematically:** NO established strict dominance of the families. With the current verified evidence S1 supplies the stronger completed justification; S2's exact identity offers conditional precision, not an established improvement.
- **Exact surviving assumptions:** fixed completed source and complete leading comparator; acceptance of R6's cited source statements; fixed positive h and source cutoffs; fixed frame and window containing the concentrating region; fixed alpha=1/2 and 0<sigma<1; sufficiently small tau satisfying the existing peak/support/mass/error thresholds; finite positive masses and second moments. S2 sign certification additionally requires correct signed endpoint intervals, obtainable conservatively from R6 here; any stronger or relative certificate requires its own proved premises and the separate peak bound. No new regularity assumption is adopted.
- **Exact unsupported claims:** source momentum constraints equal signed soft-weight constraints; favorable error signs or cancellation without proof; automatic relative-weight bounds at threshold zeros; guaranteed S2 rate/constant/interval improvement; moment-only certification of U; finite DNS resolution, inner-core/component identification, mechanism specificity, continuous-time monotonicity, or empirical support.
- **Whether either route materially strengthens Gate 1:** NO new source-direction or operational evidence beyond R6. The comparison strengthens the audit trail by separating exact identities, available inputs and invalid sign transfers; it does not close a scientific gate.
- **Gate 1 status:** PARTIAL. E0 HOLD. H2A2 remains unstarted. No execution authority is inferred.
- **One recommended next bounded scientific action:** a source-only quantitative-input audit of S1's remainder constant K and validity threshold tau_0, identifying which bounds can actually be extracted from the cited construction and which remain existential. Do not choose numerical event windows, inspect DNS, implement an estimator or begin that audit in this circuit.
