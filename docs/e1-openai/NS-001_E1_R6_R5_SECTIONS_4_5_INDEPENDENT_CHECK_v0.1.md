# NS-001 / E1 R6: independent check of R5 sections 4-5 v0.1

18 September 2026 · Phase 1 / Gate 1 · one bounded scientific review

## 1. Verdict and review boundary

**MATHEMATICAL CONSEQUENCE — verdict:** R5 §4 and §5 survive independent checking as consequences of the cited construction statements, with the domains and order of choices made explicit below. The result is eventual, uniform, continuum comparison to the **complete leading tangential profile**, followed by strict endpoint inequalities for each fixed remaining-time ratio. It is not a numerical operating certificate or a DNS result. Gate 1 remains **PARTIAL**.

This review re-read the primary source and reconstructed the estimates; it did not accept R5's conclusion merely because earlier receipts repeat it. Accepting the cited paper propositions is an explicit premise. R6 is not an independent verification of the entire paper, its construction, or a formalization. No final operator is chosen, estimator implemented, target data inspected, JHTDB queried, E0 executed, or H2A2 work performed. No scientific code, simulation, parameter search, or test suite was run. Administrative hashing, PDF extraction/rendering and Git preservation are separate from scientific execution.

**PAPER-DERIVED — source identity:** [P], OpenAI, [Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), retained PDF `/tmp/ns001-gate1/paper.pdf`, 166 pages, SHA-256 `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. All page numbers below are printed page numbers. The retained bytes match R5's source identity. The public PDF was opened as a source check; the mathematical examination used the hashed local bytes. Pages 58, 61 and 106 were also rendered and visually checked to disambiguate exponents and subscripts.

R5 is `NS-001_E1_ULTRA_ANALYTICAL_EXPANSION_RECEIPT_v0.1.md`, SHA-256 `52d718b54068481ba1fcac21259be6795777e108dea02e8a4fcc8b5609833084`. It remains unchanged.

## 2. Source premises actually checked

| Classification | Source location | Premise used, and its limit |
| --- | --- | --- |
| PAPER-DERIVED | (4.1)-(4.5), pp. 24-25 | Similarity coordinates, unique q, positive coordinate denominator, component normalizations and smooth Cartesian factors at the axis. |
| PAPER-DERIVED | Theorem 4.6(i),(v), p. 33 | Bounded profiles on each fixed finite X range and closed eta interval; positive swirl for X>0; exact decaying heat exterior; radial and axial components vanish in that exterior. |
| PAPER-DERIVED | Lemma 4.8, p. 35 | One fixed h is selected under nested restrictions, including h<min(1/100,lambda,exp(-T_d)); h is not a freely chosen numerical fit parameter. |
| PAPER-DERIVED | (5.1)-(5.2), pp. 46-47; (5.26)-(5.30), pp. 55-57 | Positive-order background coefficients have powers 2nh, Cartesian regularity and a physical summation framework with losses independent of truncation. |
| PAPER-DERIVED | Lemma 5.4, (5.35), p. 58 | Physical tail bound against a fixed finite partial sum, including curl/cutoff terms; loss ell'_m is independent of truncation J. |
| PAPER-DERIVED | Proposition 5.5 and proof, pp. 60-62 | Realized background, common correction support, recovered expansion and endpoint extensions. (5.42) itself is on a radial rectangle bounded away from the axis; it must not simply be extended to X=0. |
| PAPER-DERIVED | (6.1), pp. 62-63; Lemma 6.3, p. 68; (6.24),(6.27),(6.29), pp. 69-70 | q comparable to a band scale Q; epsilon=Q^h, S*=ell^2; bounded pointwise label overlap; finite harmonic sets at a fixed stage; coefficient constants uniform in band/label/point. |
| PAPER-DERIVED | p. 101; Definition 9.4, (9.9), p. 106 | Physical velocity has prefactor Q^(-a); total fixed-stage waves are W_(1/2), mean velocity corrections have higher positive powers. These are total velocity bounds, not only residual bounds. |
| PAPER-DERIVED | Lemma 9.8, pp. 113-114; Proposition 9.9, pp. 114-116 | Correction summation uses g_j=hj/10; a common domain exists; the completed local field has endpoint regularity away from q=0 and exact exterior agreement. |
| PAPER-DERIVED | Proposition 10.1, pp. 117-118, (10.3)-(10.4) | Fixed final cutoffs equal one near (0,1); u=c u_loc+grad(c) cross A; localization is supported strictly inside the local domain and extends smoothly by zero. |

**NEEDS ADDITIONAL SOURCE CHECK — outside this bounded claim:** independent verification of the proofs of every underlying construction proposition, rather than using those propositions as premises, would require a separate paper audit. No essential citation in the present consequence chain remains unread or provisionally substituted by an assertion from R5.

## 3. Independent reconstruction of section 4

### 3.1 Coordinates and complete-profile localization

**PAPER-DERIVED.** Write a=1/2+h, d=1/2-h, tau=1-t, with the source's fixed 0<h<1/100. Then

`z=q^d eta`, `tau=q(1-eta^2)`, `X=r^2/(2q)`,

and the coordinate denominator is `1-2h eta^2 >= 1-2h > 0`. The leading tangential field is

`g=q^(-a)(E e_theta + U_profile e_z)`.

Here d denotes the axial scaling exponent, not the paper's separate shorthand `1-eta^2`. The omitted leading radial velocity is part of u-g, not silently zeroed.

**MATHEMATICAL CONSEQUENCE.** Under `x=D_tau y`, with `D_tau=diag(tau^(1/2),tau^(1/2),tau^d)`, write y=(rho cos(theta),rho sin(theta),zeta). Substitution gives

`q=tau Q(zeta)`, `Q-zeta^2 Q^(2h)=1`,

`X=rho^2/(2Q)`, `eta=zeta/Q^d`,

`|g(D_tau y,1-tau)|=tau^(-a) F(y)`,

`F=Q^(-a) sqrt(E(X,eta)^2+U_profile(X,eta)^2)`.

The source's uniqueness argument applies to Q: Q>=1 and Q>|zeta|^(1/d). This is an exact change of variables, not an asymptotic ansatz about u.

**MATHEMATICAL CONSEQUENCE.** On bounded X ranges the profiles are bounded uniformly up to eta=+/-1. In the exterior U_profile=0 and `E=c_infty X^(-a) H(2(1-eta^2)/X)`, with `0<H<=1` from its integral formula. Thus finite constants C0,C1 give

`F <= C0 Q^(-a)`, `F <= C1 (rho^2/2)^(-a)` for rho>0.

For the second inequality inside the finite-X region, bound `X^a sqrt(E^2+U_profile^2)` there; no singular division at X=0 is needed. The first bound controls large |zeta| and the second large rho, jointly proving F tends to zero at similarity infinity. Axis continuity follows from the Cartesian factors, even though the cylindrical direction e_theta is undefined on the axis.

**MATHEMATICAL CONSEQUENCE.** F is continuous, nonzero and attains a finite maximum M>0. For each fixed 0<alpha<1, `[F^2-alpha^2 M^2]+` is positive on a nonempty open set and supported in a bounded set. Consequently its mass m_F is finite and strictly positive. Its covariance is positive definite: a positive density on an open three-dimensional set cannot be supported in a plane. Axisymmetry, without requiring z-reflection symmetry, makes this *centered* covariance `diag(c_r,c_r,c_z)` with c_r,c_z>0. None of these facts identifies the region with the source's designated inner core.

### 3.2 Background, including the axis

**MATHEMATICAL CONSEQUENCE.** The leading radial term is `q^(-1/2) V0/sqrt(2X)`. Since V0=X v0 with v0 bounded on fixed profile rectangles, its magnitude in the q^a normalization is O(q^h), uniformly including X=0. A fixed positive-order tangential coefficient is O(q^(2nh)) after normalization, and a fixed radial coefficient is O(q^(h+2nh)).

To check the infinite background sum independently of an extension of the annular formula (5.42), use the physical tail estimate with background orders g_n=2nh. Choose one fixed truncation N large enough that

`a+h(N+1)-ell'_(0,bg) >= h`.

The normalized physical tail is then O(q^h) for q below its positive cutoff threshold. The finite initial block has the coefficient bounds just described; smooth Cartesian representatives justify them on `0<=X<=X_ext`, `-1<=eta<=1`. This establishes

`q^a |u_B-g| <= C_B q^h`

uniformly on that fixed profile range. It also accounts for the streamfunction cutoff contribution in (5.45). R5's appeal to normalized summation is supported by Proposition 5.5's proof; the physical-tail argument gives an additional explicit route and avoids treating annular bounds as axis bounds.

### 3.3 Fixed correction stage and the actual infinite tail

**MATHEMATICAL CONSEQUENCE.** Fix J first. The definitions of W and M, together with (9.9), bound complete normalized velocity amplitudes at that stage. Flat shell weights times any fixed inverse edge-distance power are bounded; the pulse envelope is at most one. The number of simultaneously relevant labels is bounded and the harmonic set is finite at fixed J. Taking absolute values of the oscillatory factors costs no power; no mean cancellation is invoked. Since q and Q are comparable and S* is proportional to a squared logarithm at small q,

`q^a |u^[J]-u_B| <= C_J q^(h/2)(1+|log q|)^P_J`.

Mean terms with powers 0.9h or 1.9h can be included in this upper bound for q<=1. Curl remainders are already included in the complete finite-state velocity classes. Constants may grow with J; a bound uniform in J is unnecessary and is not claimed.

**MATHEMATICAL CONSEQUENCE.** For the actual completed local field, Lemma 5.4 and Proposition 9.9 give, at derivative order zero,

`q^a |u_loc-u^[J]| <= 2^(-J) q^(a+h(J+1)/20-ell'_0)`,

for `J>=1` and `q<(2a_J)^(-1)`, after also entering the region where the finite initialization cutoff equals one. In a Euclidean component norm an inessential fixed norm-equivalence factor may be absorbed into the eventual constant. The 1/20 is correct: the summation lemma uses g_(J+1)/2 and g_j=hj/10.

Set beta=h/4. Because ell'_0 is independent of J and h>0, a finite J can be fixed with `a+h(J+1)/20-ell'_0>=beta`. For gamma>beta and finite P, `sup_(s>=0) exp(-(gamma-beta)s)(1+s)^P` is finite. Hence the fixed-stage logarithmic term is O(q^beta), since h/2>beta. The background term also is O(q^beta). Taking the minimum of the finitely many positive domain/cutoff thresholds yields

`|u_loc-g| <= C q^(-a+beta)` for `0<q<q_c`, on the common bounded-X region.

The quantifier order is crucial: fix source data and h, choose finite background/correction truncations, then constants and q_c, and only then take q small. Neither J(tau) nor summing uncontrolled finite-stage constants is used. Flatness of the forcing residual is not used as a velocity-error estimate.

### 3.4 Final cutoff and uniformity over the whole window

**MATHEMATICAL CONSEQUENCE.** Let B be the fixed bounded observation window with a neighborhood of the origin in its interior (the inherited cube suffices). Fix X_ext beyond every slow and annular correction support. If X<=X_ext and q<q_c, then

`r<=sqrt(2 X_ext q)`, `|z|<=q^d`.

For q_c small enough and t sufficiently close to 1, these points are inside the plateau of both final cutoffs. Therefore u=u_loc there. Since q>=tau and -a+beta<0,

`tau^a |u-g| <= C tau^a q^(-a+beta) <= C tau^beta`.

**MATHEMATICAL CONSEQUENCE.** The rest of B requires two separate checks; smoothness for each t<1 alone would not suffice:

- On q>=q_c where localization is active, its support is bounded away from q=q_* and the paper's one-sided endpoint bounds apply to u_loc and its potential. They bound the cutoff product and curl term uniformly as t approaches 1. Outside that support u=0, while g is bounded for q>=q_c.
- On q<q_c and X>X_ext, the local field equals g exactly and its potential A vanishes. A final-cutoff discrepancy can occur only away from the fixed plateau. For sufficiently small q, |z| is inside the axial plateau and the temporal cutoff equals one, so a discrepancy requires r bounded below by a fixed positive radius. The exact heat exterior is uniformly bounded there. This covers small q at large X without pretending q is bounded below.

Thus the remainder contributes at most C_far tau^a. As 0<beta<a and tau<=1, it is absorbed into K tau^beta. Using `||u|-|g||<=|u-g|`,

`epsilon_tau := sup_(y in D_tau^(-1)B) |tau^a |u(D_tau y,1-tau)|-F(y)| <= K tau^(h/4)`

for all `0<tau<tau_0`, with finite K and strictly positive tau_0. This is uniform on the expanding similarity image of the fixed physical window. **Section 4 survives.**

## 4. Independent reconstruction of section 5

### 4.1 Positive-threshold support and peaks

**MATHEMATICAL CONSEQUENCE.** Fix alpha in (0,1). Choose a compact ball K_alpha containing an ideal maximizer and such that `sup_(outside K_alpha) F <= alpha M/2`. Since d>0 and B contains a neighborhood of zero, there is tau_B>0 with `D_tau K_alpha` inside B for every 0<tau<tau_B.

Let `f_tau(y)=tau^a |u(D_tau y,1-tau)|` and `M_tau=sup_(D_tau^(-1)B) f_tau`. The ideal maximizer is now in the domain, so `|M_tau-M|<=epsilon_tau`. Outside K_alpha but inside that domain,

`f_tau <= alpha M/2+epsilon_tau < alpha(M-epsilon_tau) <= alpha M_tau`

whenever `epsilon_tau<alpha M/[2(1+alpha)]`. Both ideal and actual positive soft weights vanish there. The actual weight here is the **window-defined** weight; no assertion about all space outside B is needed. Including the ideal maximizer and full relevant support in B precedes, rather than follows from, the peak comparison.

### 4.2 Weight, mass and total variation

**MATHEMATICAL CONSEQUENCE.** Define `W_tau=[f_tau^2-alpha^2 M_tau^2]+` and `W_F=[F^2-alpha^2 M^2]+`. Positive-part truncation is 1-Lipschitz. If epsilon_tau<=epsilon_bar<=M, then

`|W_tau-W_F| <= (1+alpha^2)(2M+epsilon_bar) epsilon_tau`.

The squared amplitude contributes tau^(-2a), while `det D_tau=tau^(3/2-h)`. Therefore

`m_g=tau^(3/2-h-2a) m_F=tau^(1/2-3h) m_F`,

`D0/m_g <= C_alpha epsilon_tau`,

`C_alpha=vol(K_alpha)(1+alpha^2)(2M+epsilon_bar)/m_F`.

D0 is the physical L1 weight difference. It has the same scale factor as m_g; the shrinking normalization has not been dropped. If C_alpha epsilon_tau<1, the actual mass m is positive.

**MATHEMATICAL CONSEQUENCE.** With the convention `TV(p,p_g)=0.5 integral |p-p_g|`, the bound without an extra denominator is valid:

`p-p_g=(w-w_g)/m_g + w(1/m-1/m_g)`,

`integral |p-p_g| <= D0/m_g+|m-m_g|/m_g <= 2D0/m_g`.

Thus `TV(p,p_g)<=C_alpha epsilon_tau`. This identity uses m>0, already proved; it does not assume m=m_g. An alternative denominator-bearing estimate would be weaker, not a correction required here.

### 4.3 Centered size and amplitude errors

**MATHEMATICAL CONSEQUENCE.** If two probability distributions have combined support of diameter D, their centered variances differ by at most `D^2 TV`. To see this, evaluate the first variance about the second distribution's centroid and use that a centroid lies in the convex hull of the support. Squared distance from that centroid is between 0 and D^2 on the support. The opposite comparison gives the other sign. This bounds centered variance, including centroid displacement, not merely its raw second moment.

For tau<=1, `||D_tau||=tau^d`, because d<1/2. Both physical supports lie in D_tau K_alpha, of diameter at most tau^d D_alpha. Consequently

`|L^2-L_g^2| <= C_L tau^(2d) epsilon_tau`, `C_L=D_alpha^2 C_alpha`,

`|U-tau^(-a)M| <= tau^(-a) epsilon_tau`.

Changing variables in the ideal probability measure gives its centered covariance `D_tau diag(c_r,c_r,c_z) D_tau`, hence

`L_g^2=2c_r tau+c_z tau^(2d)`.

These powers agree with R5. Axial asymmetry can move the ideal centroid, but is already included in c_z and does not invalidate this covariance transformation.

### 4.4 Strict endpoint directions on a nonempty symbolic interval

**MATHEMATICAL CONSEQUENCE.** Fix 0<sigma<1 independently of tau. All of the following are positive and finite:

`epsilon_bar`, `alpha M/[2(1+alpha)]`, `1/C_alpha`,

`M(1-sigma^a)/(1+sigma^a)`,

`c_z(1-sigma^(2d))/[C_L(1+sigma^(2d))]`.

Choose epsilon_* strictly below their minimum. Enlarge K to be positive if necessary. Then choose

`0<tau_*<min(tau_0,tau_B,1,(epsilon_*/K)^(1/beta))`.

This minimum is strictly positive: each construction choice was finite, h and beta are strictly positive, and only finitely many positive thresholds enter after fixing the truncation. This proves existence rather than merely writing an inequality whose premises were never established. It gives no useful numerical lower bound on tau_*.

For `tau_1<tau_*`, `tau_2=sigma tau_1`, both errors are below epsilon_*. Direct subtraction gives

`U(1-tau_2)-U(1-tau_1)`

`>=tau_1^(-a)[sigma^(-a)(M-epsilon_*)-(M+epsilon_*)]>0`.

For squared size, the earlier-minus-later ideal difference is

`2c_r tau_1(1-sigma)+c_z tau_1^(2d)(1-sigma^(2d))`.

Subtracting both endpoint error allowances leaves at least

`tau_1^(2d)[c_z(1-sigma^(2d))-C_L epsilon_*(1+sigma^(2d))]>0`.

Therefore `L(1-tau_2)<L(1-tau_1)` as well as U increasing. Positive square roots preserve this strict squared-size ordering. **Section 5 survives.**

## 5. Assumptions, exclusions and classification of stronger readings

| Classification | Dependency or claim | Finding |
| --- | --- | --- |
| PAPER-DERIVED | Fixed h and constructed profile/correction/cutoff data | Required. The proof is conditional on the cited source statements, not on arbitrary fields or arbitrary h in a numerically chosen interval. |
| MATHEMATICAL CONSEQUENCE | Constants independent of tau after choices | Required and supported. Constants may depend on h, the fixed profile, finite truncations, cutoffs, B, alpha and sigma. They need not be small or computationally available. |
| MATHEMATICAL CONSEQUENCE | Fixed laboratory frame and fixed bounded B containing zero in its interior | Required. No moving or outcome-selected window, background subtraction or Galilean change is introduced. |
| MATHEMATICAL CONSEQUENCE | 0<alpha<1 fixed | Required for localized positive mass. The argument is not uniform as alpha tends to zero or one and does not justify alpha=0. |
| MATHEMATICAL CONSEQUENCE | 0<sigma<1 fixed | Required. The permissible epsilon_* and tau_* may collapse as sigma approaches one. There is no assertion uniform over arbitrarily close pairs. |
| MATHEMATICAL CONSEQUENCE | Value regularity/support | Continuity, axis regularity, endpoint bounds away from concentration, bounded relevant support and positive mass are used explicitly. Derivative control of the measured time series is not obtained. |
| UNSUPPORTED / REJECTED | Continuous-time monotonicity or dL/dt<0 everywhere | Uniform value convergence and fixed-ratio ordering do not establish derivative signs. |
| UNSUPPORTED / REJECTED | Numerical crossover or a nonempty DNS-resolvable range | No numerical K, tau_0, profile constants, dimensional map or spatial/cadence error certificate is supplied. An asymptotic upper constraint on tau can conflict with a grid-resolution lower constraint. |
| UNSUPPORTED / REJECTED | Inner-core identification, arbitrary component narrowing, mechanism specificity | The comparator is the full leading tangential profile. The relative-amplitude counterexample for unrestricted U/L interpretation remains valid outside the proved premises. |
| UNSUPPORTED / REJECTED | Vorticity/global-extreme, singularity or empirical DNS conclusions | These do not follow from this velocity/moment consequence. No target data or new empirical results exist in R6. |
| NEEDS ADDITIONAL SOURCE CHECK | Full independent validation of the underlying paper | Not performed or claimed. It is distinct from verifying the mathematical implication of its cited statements. |

No step in the checked chain requires replacing unknown constants with engineering screens or silently promoting eventual smallness into a DNS-resolvable claim. In particular, R5's assertion of a nonempty **symbolic continuum** interval is justified; interpreting that phrase as a certified finite-grid interval is not.

## 6. Preservation and completion record

Branch at entry: `codex/e0-h2-preparation`; HEAD before: `912453345b86682856d258b9680326bca2e3e2b7`; tracked and untracked worktree clean apart from the two known ignored bytecode caches. The administrative baseline covers all 35 pre-existing non-Git regular files. All retain their entry SHA-256 bytes. The sole new repository artifact is this receipt. Frozen preregistration SHA-256 remains `a2a8523c065d4d41155aa29d367c888d49ab3032f6075b8cebbd2475ff1efd78`; sidecar SHA-256 remains `0e1e5900aec22a55332c1bde18147c3f2ff5a55351a8d1bec6e504b3eb960de8`.

The review is complete at the stated source-premise boundary. Its permitted preservation commit/push is conditional on confirming only this file is added; this receipt does not pre-claim a remote-publication result or embed a self-referential final commit hash. E0 remains HOLD and H2A2 remains unstarted.

## 7. Closing determinations

- **Whether §4 survives independent checking:** YES, as a mathematical consequence of the checked source statements. The axis, physical tail, fixed-stage logarithms, exterior and final-cutoff regions support an eventual uniform value bound with beta=h/4.
- **Whether §5 survives independent checking:** YES, for each fixed alpha in (0,1) and sigma in (0,1), in a fixed bounded window containing the origin, at sufficiently late paired continuum times. The support, normalization, variance scaling and strict endpoint margins are valid.
- **Exact assumptions still required:** accept the cited construction statements and their realized field; hold its positive h, profile and cutoffs fixed; choose finite truncations before the small-q limit; use the complete leading tangential comparator in a fixed velocity frame; use fixed B with an interior neighborhood of zero; fixed 0<alpha,sigma<1; remain below all positive cutoff/domain/support/error thresholds. No uniformity as h tends to zero, alpha reaches its endpoints or sigma tends to one is asserted.
- **Exact claims that remain unsupported:** numerical crossover; DNS-resolvable overlap; operational DNS/component correspondence; continuous-time monotonicity; arbitrary-close-pair ordering; inner-core identity; all-axis contraction of the actual field; mechanism specificity; global-vorticity or singularity inference; empirical support; final-operator validation; independent verification of the entire paper.
- **Is the R5 fixed-ratio result strong enough to remain a valid Gate 1 input?** YES, as a source-conditioned continuum directional result for the complete-profile comparator. It is not sufficient to pass Gate 1 or authorize measurement, design freeze or execution.
- **Gate 1 status:** PARTIAL. E0 HOLD; H2A2 unstarted; no run authorization inferred.
- **One recommended next bounded scientific action:** a paper-and-algebra-only S1-versus-S2 comparison for the same U/L claim, asking whether the exact signed-moment certificate provides a proved improvement using source inputs already available, without adding unobservable assumptions. Retain S1 as the checked baseline; do not implement, select a final operator, fit DNS profiles or begin that comparison in R6.
