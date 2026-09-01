# NS-001 reproducibility contract

NS-001 is a time-first feasibility test for extreme-value analysis of vorticity in JHTDB DNS records.

## Scientific question

For a fixed spatial sub-box, construct

\[
M(t)=\max_x |\omega(x,t)|
\]

and estimate its temporal autocorrelation, integral time scale, and effective number of independent observations before fitting any GEV/GPD tail model.

## Frozen measurement path

1. Dataset: `isotropic1024coarse`.
2. Retrieve velocity cutouts from JHTDB.
3. Add a two-cell spatial halo.
4. Compute curl locally using a centered fourth-order finite difference.
5. Compute the vector magnitude `|omega|`.
6. Reduce each frame to the maximum over the retained interior sub-box.
7. Cache only the resulting `M(t)` vector.
8. Estimate the lag-count-corrected ACF.
9. Sum the initial positive ACF sequence to obtain `tau_int`.
10. Compute `N_eff = N / tau_int`.

The GREEN/AMBER/RED thresholds are screening heuristics, not EVT theorems.

## Frozen protocols

- `protocols/sanity.json`: one live frame, `12^3` interior. Fits the public JHTDB testing-token point limit after the derivative halo.
- `protocols/smoke.json`: five live frames, `5^3` interior. Exercises temporal ordering, caching, ACF, result output, and receipts while remaining under the public-token limit.
- `protocols/day_one.json`: canonical 5,024-frame feasibility experiment. Requires a normal JHTDB authorization token.

Protocol files are inputs. Do not silently edit a protocol after a result exists. Create a new protocol/version instead.

## Reproduction unit

A completed run writes:

```text
output_dir/
  protocol.json
  M_of_t.npy
  result.json
  receipt.json
```

`receipt.json` records:

- frozen protocol and protocol hash;
- JHTDB dataset and numerical constants;
- source commit supplied to the container at build time;
- SHA-256 of the runner and measurement engine;
- Python, NumPy, OS and container identity where available;
- SHA-256 of `M_of_t.npy` and `result.json`;
- the resulting statistics;
- explicit claim boundaries;
- the fact that the JHTDB token value was not recorded.

Two runs using the same protocol should therefore be comparable at the level of source, environment, reduced data, and result.

## Claim boundary

A successful run does **not** imply:

- that a sub-box maximum equals the global maximum;
- that a GREEN screening verdict proves a valid GEV/GPD model;
- that large vorticity establishes finite-time blow-up;
- that NS-001 proves or disproves Navier-Stokes regularity.

A failed independence/power screen is a valid outcome and should be retained as such.
