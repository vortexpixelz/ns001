# NS-001
> [!IMPORTANT]
> **Current status — 2026-09-02:** The temporal fixed-sub-box design documented below is preserved as a superseded protocol and is not authorized for execution. The active prospective experiment is [E0 Stride Refinement](preregistrations/e0/NS-001_E0_STRIDE_REFINEMENT_PREREG_FROZEN_2026-09-02.md). Sanity is complete; E0 has not run. Do not run the legacy `make sanity`, `make smoke`, or `make day-one` targets. Required order: verify the frozen hash, approve the exact execution manifest, run E0, then stop.

Time-first feasibility test for extreme-value analysis of vorticity in JHTDB turbulence DNS.

The first question is deliberately narrower than an EVT fit:

> Does the available trajectory contain enough effectively independent extreme-vorticity observations to support defensible tail inference?

Primary observable:

\[
M(t)=\max_x |\omega(x,t)|.
\]

The measurement engine lives in `ns001_tau_check.py`. The reproducible runner is `run_experiment.py`, which consumes frozen JSON protocols and emits hashed receipts.

## Fastest reproduction

Requirements: Docker and a JHTDB token in `JHTDB_TOKEN`.

Public-token sanity check:

```bash
export JHTDB_TOKEN='edu.jhu.pha.turbulence.testing-201406'
make sanity
```

Public-token five-frame temporal smoke test:

```bash
export JHTDB_TOKEN='edu.jhu.pha.turbulence.testing-201406'
make smoke
```

Canonical day-one experiment, after receiving a normal JHTDB authorization token:

```bash
export JHTDB_TOKEN='YOUR_REAL_TOKEN'
make day-one
```

Each run creates an output directory containing:

```text
protocol.json
M_of_t.npy
result.json
receipt.json
```

The receipt records the protocol, source/runtime provenance, hashes of code and reduced data, and the resulting statistics. The token value is never written to the receipt.

## Run without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export JHTDB_TOKEN='...'
python run_experiment.py protocols/sanity.json --output-dir outputs/sanity
```

## Protocols

- `protocols/sanity.json` — one-frame live data-path check.
- `protocols/smoke.json` — five-frame live temporal/ACF smoke test under the public-token limit.
- `protocols/day_one.json` — frozen 5,024-frame feasibility run using `isotropic1024coarse`.

See [`EXPERIMENT.md`](EXPERIMENT.md) for the reproducibility contract and claim boundaries.

## Scientific boundary

NS-001 does not claim a Navier-Stokes proof. A sub-box maximum is not a global maximum, and the GREEN/AMBER/RED thresholds are screening heuristics rather than guarantees of GEV/GPD validity. If the independence gate fails, that negative result is retained rather than forcing a sign for the tail parameter.
