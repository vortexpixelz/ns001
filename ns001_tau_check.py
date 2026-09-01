"""
NS-001 :: Day-One Feasibility Check
===================================
Measure the correlation time of

    M(t) = max_x |omega(x,t)|

inside a fixed JHTDB sub-box, then estimate how many effectively
independent extreme-vorticity observations the record contains.

This is the go/no-go gate BEFORE any GEV/GPD claim.

Default dataset
---------------
JHTDB ``isotropic1024coarse`` (forced homogeneous isotropic turbulence).
The public dataset page reports 5,028 stored frames including extra guard
frames used for temporal interpolation. The current raw-cutout metadata
exposes 5,024 ordinary cutout frames; this script therefore defaults to
frames 1..5024 at dt = 0.002.

Data path
---------
The raw cutout service stores velocity, not vorticity. We therefore:

    velocity cutout -> local 4th-order curl -> |omega| -> sub-box max

A two-cell halo is fetched around the requested box so every retained
vorticity value uses a centered 4th-order finite difference. Only M(t)
is cached; raw velocity chunks are discarded immediately.

Authentication
--------------
Set your JHTDB token in the environment before running:

    export JHTDB_TOKEN='...'

Examples
--------
One-frame sanity check (do this first):

    python ns001_tau_check.py --sanity-only

Full default feasibility run:

    python ns001_tau_check.py

Smaller development run:

    python ns001_tau_check.py --n-times 256 --box 24

Notes on interpretation
-----------------------
* The sub-box maximum is NOT the global maximum. This first pass asks
  whether the extreme-observable time series has enough temporal
  independence to justify a larger EVT study.
* GREEN/AMBER/RED thresholds below are project screening heuristics,
  not EVT theorems and not guarantees that a GEV/GPD fit is valid.
* A failure of the independence/power gate is a valid result. Do not
  force a sign for xi from a record that cannot identify it.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np


DATASET = "isotropic1024coarse"
GRID_N = 1024
DX = 2.0 * np.pi / GRID_N
DT = 0.002
N_CUTOUT_FRAMES = 5024
JHTDB_CUTOUT_URL = "https://web.idies.jhu.edu/turbulence-svc/cutout/api/local"
FD_HALO = 2


# ----------------------------------------------------------------------
# STEP 1: construct M(t) from JHTDB velocity cutouts.
# ----------------------------------------------------------------------


def _fetch_velocity_chunk(
    *,
    token: str,
    first_frame: int,
    last_frame: int,
    origin: tuple[int, int, int],
    box: int,
    timeout: int = 1000,
) -> list[np.ndarray]:
    """Return raw velocity cutouts for an inclusive frame range.

    JHTDB's current local cutout endpoint returns JSON with one 3-D
    velocity array per requested frame. Spatial ranges are inclusive.
    A two-cell halo is added on every side for the local curl.
    """
    x0, y0, z0 = origin
    side = box + 2 * FD_HALO

    params = {
        "token": token,
        "function": "velocity",
        "dataset": DATASET,
        "xs": x0 - FD_HALO,
        "xe": x0 - FD_HALO + side - 1,
        "ys": y0 - FD_HALO,
        "ye": y0 - FD_HALO + side - 1,
        "zs": z0 - FD_HALO,
        "ze": z0 - FD_HALO + side - 1,
        "ts": first_frame,
        "te": last_frame,
        "stridet": 1,
        "stridex": 1,
        "stridey": 1,
        "stridez": 1,
        "filter_width": 1,
    }

    url = f"{JHTDB_CUTOUT_URL}?{urlencode(params)}"
    with urlopen(url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    data_vars = payload.get("data_vars", {})
    if not data_vars:
        raise RuntimeError("JHTDB cutout response contained no data_vars")

    arrays: list[np.ndarray] = []
    expected_shape = (side, side, side, 3)
    for name in sorted(data_vars):
        arr = np.asarray(data_vars[name]["data"], dtype=np.float64)
        if arr.shape != expected_shape:
            raise RuntimeError(
                f"unexpected JHTDB shape for {name}: {arr.shape}; "
                f"expected {expected_shape}"
            )
        arrays.append(arr)

    expected_frames = last_frame - first_frame + 1
    if len(arrays) != expected_frames:
        raise RuntimeError(
            f"JHTDB returned {len(arrays)} frames; expected {expected_frames} "
            f"for [{first_frame}, {last_frame}]"
        )
    return arrays


def _d4_centered(a: np.ndarray, axis: int, h: float) -> np.ndarray:
    """Fourth-order centered derivative on the common 2-cell interior."""
    if a.ndim != 3:
        raise ValueError(f"expected a 3-D scalar field, got shape {a.shape}")

    core = [slice(FD_HALO, -FD_HALO)] * 3

    def shifted(offset: int):
        s = core.copy()
        if offset == -2:
            s[axis] = slice(None, -4)
        elif offset == -1:
            s[axis] = slice(1, -3)
        elif offset == 1:
            s[axis] = slice(3, -1)
        elif offset == 2:
            s[axis] = slice(4, None)
        else:
            raise ValueError(offset)
        return tuple(s)

    return (
        a[shifted(-2)]
        - 8.0 * a[shifted(-1)]
        + 8.0 * a[shifted(1)]
        - a[shifted(2)]
    ) / (12.0 * h)


def max_vorticity_magnitude(velocity: np.ndarray, dx: float = DX) -> float:
    """Compute max |curl(u)| on the halo-free interior of one cutout.

    JHTDB velocity arrays are ordered (z, y, x, component), with
    components (u, v, w) corresponding to (x, y, z).
    """
    if velocity.ndim != 4 or velocity.shape[-1] != 3:
        raise ValueError(f"expected (z,y,x,3) velocity array, got {velocity.shape}")

    u = velocity[..., 0]
    v = velocity[..., 1]
    w = velocity[..., 2]

    # Array axes: 0=z, 1=y, 2=x.
    dw_dy = _d4_centered(w, axis=1, h=dx)
    dv_dz = _d4_centered(v, axis=0, h=dx)
    du_dz = _d4_centered(u, axis=0, h=dx)
    dw_dx = _d4_centered(w, axis=2, h=dx)
    dv_dx = _d4_centered(v, axis=2, h=dx)
    du_dy = _d4_centered(u, axis=1, h=dx)

    omega_x = dw_dy - dv_dz
    omega_y = du_dz - dw_dx
    omega_z = dv_dx - du_dy
    omega_mag = np.sqrt(omega_x**2 + omega_y**2 + omega_z**2)
    return float(np.max(omega_mag))


def fetch_subbox_max(
    n_times: int = N_CUTOUT_FRAMES,
    box: int = 32,
    cache: str = "M_of_t.npy",
    *,
    start_frame: int = 1,
    time_chunk: int = 32,
    origin: tuple[int, int, int] = (256, 256, 256),
    token_env: str = "JHTDB_TOKEN",
) -> np.ndarray:
    """Build and cache M(t) = max |omega| for a fixed JHTDB sub-box."""
    cache_path = Path(cache)
    partial_path = cache_path.with_suffix(cache_path.suffix + ".partial.npy")

    if n_times < 1:
        raise ValueError("n_times must be >= 1")
    if box < 5:
        raise ValueError("box must be >= 5")
    if time_chunk < 1:
        raise ValueError("time_chunk must be >= 1")
    if start_frame < 1 or start_frame + n_times - 1 > N_CUTOUT_FRAMES:
        raise ValueError(
            f"requested frames {start_frame}..{start_frame + n_times - 1}; "
            f"raw cutout range is 1..{N_CUTOUT_FRAMES}"
        )

    for coord in origin:
        lo = coord - FD_HALO
        hi = coord + box + FD_HALO - 1
        if lo < 1 or hi > GRID_N:
            raise ValueError(
                f"origin={origin}, box={box} crosses the raw cutout boundary; "
                "choose an interior origin so the finite-difference halo fits"
            )

    if cache_path.exists():
        cached = np.load(cache_path)
        if cached.shape == (n_times,) and np.all(np.isfinite(cached)):
            print(f"loading complete cache: {cache_path}")
            return cached
        print(
            f"ignoring incompatible/incomplete cache {cache_path} with "
            f"shape {cached.shape}; expected {(n_times,)}"
        )

    token = os.environ.get(token_env)
    if not token:
        raise RuntimeError(
            f"missing JHTDB token. Set environment variable {token_env}, e.g.\n"
            f"    export {token_env}='your-token-here'"
        )

    M = np.full(n_times, np.nan, dtype=np.float64)
    if partial_path.exists():
        partial = np.load(partial_path)
        if partial.shape == M.shape:
            M[:] = partial
            done = int(np.isfinite(M).sum())
            print(f"resuming partial cache: {done}/{n_times} frames complete")

    side = box + 2 * FD_HALO
    raw_gib = side**3 * 3 * 4 * n_times / 1024**3
    print(
        f"dataset={DATASET}  frames={start_frame}..{start_frame+n_times-1}  "
        f"box={box}^3 (+{FD_HALO}-cell halo)"
    )
    print(f"approx raw float payload across run: {raw_gib:.2f} GiB")
    print("raw chunks are discarded; only M(t) is cached")

    i = 0
    while i < n_times:
        if np.isfinite(M[i]):
            i += 1
            continue

        j = min(i + time_chunk, n_times)
        finite_inside = np.flatnonzero(np.isfinite(M[i:j]))
        if finite_inside.size:
            j = i + int(finite_inside[0])

        first = start_frame + i
        last = start_frame + j - 1
        print(f"fetching frames {first}..{last} ({j}/{n_times})")
        velocity_frames = _fetch_velocity_chunk(
            token=token,
            first_frame=first,
            last_frame=last,
            origin=origin,
            box=box,
        )

        for local_k, velocity in enumerate(velocity_frames):
            M[i + local_k] = max_vorticity_magnitude(velocity)

        np.save(partial_path, M)
        i = j

    if not np.all(np.isfinite(M)):
        missing = np.flatnonzero(~np.isfinite(M))
        raise RuntimeError(f"M(t) still has {len(missing)} missing values")

    np.save(cache_path, M)
    try:
        partial_path.unlink()
    except FileNotFoundError:
        pass
    print(f"saved complete M(t) cache: {cache_path}")
    return M


# ----------------------------------------------------------------------
# STEP 2: autocorrelation and integral time scale.
# ----------------------------------------------------------------------


def autocorrelation(x: np.ndarray) -> np.ndarray:
    """Normalized, lag-count-corrected ACF via FFT; r[0] == 1."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 2:
        raise ValueError("ACF requires a 1-D series with at least two samples")
    if not np.all(np.isfinite(x)):
        raise ValueError("ACF input contains NaN/Inf")

    x = x - x.mean()
    n = len(x)
    f = np.fft.rfft(x, n=2 * n)
    acov = np.fft.irfft(f * np.conj(f))[:n]
    acov /= np.arange(n, 0, -1)

    if not np.isfinite(acov[0]) or acov[0] <= 0:
        raise ValueError("M(t) has zero/invalid variance; ACF is undefined")
    return acov / acov[0]


def integral_time_scale(r: np.ndarray) -> float:
    """Initial-positive-sequence integral time scale, in samples."""
    r = np.asarray(r, dtype=float)
    crossings = np.flatnonzero(r <= 0)
    zero = int(crossings[0]) if crossings.size else len(r)
    tau = 1.0 + 2.0 * float(r[1:zero].sum())
    return max(tau, 1.0)


def _first_below(r: np.ndarray, threshold: float) -> int | None:
    idx = np.flatnonzero(r < threshold)
    return int(idx[0]) if idx.size else None


def report(M: np.ndarray, dt: float = DT) -> tuple[float, float]:
    n = len(M)
    r = autocorrelation(M)
    tau = integral_time_scale(r)
    n_eff = n / tau
    e_fold = _first_below(r, np.exp(-1))

    print("=" * 66)
    print("NS-001 FEASIBILITY :: autocorrelation of M(t) = max|omega|")
    print("=" * 66)
    print(f"  samples in record        n     = {n}")
    print(
        f"  integral time scale      tau   = {tau:.2f} samples"
        f"  ({tau * dt:.6g} physical time)"
    )
    print(f"  EFFECTIVE INDEPENDENT    N_eff = {n_eff:.1f}")
    print(
        "  ACF drops below 1/e at         : "
        + (f"{e_fold} samples" if e_fold is not None else "not within record")
    )
    print("-" * 66)
    print("  SCREENING HEURISTIC (not an EVT theorem):")

    if n_eff >= 200:
        print("  VERDICT: GREEN. Independence/power screen passed strongly.")
        print("  -> Proceed to EVT diagnostics; do not treat GREEN as fit validity.")
    elif n_eff >= 50:
        print("  VERDICT: AMBER. Potentially workable; uncertainty may be wide.")
        print("  -> Prefer POT/GPD diagnostics and bootstrap uncertainty on xi.")
        print("  -> Stress-test threshold and declustering choices.")
    else:
        print("  VERDICT: RED. Too few effectively independent extremes.")
        print("  -> Do NOT claim a sign for xi from this record.")
        print("  -> Report the public-record limitation instead of forcing a fit.")
    print("=" * 66)

    candidate_blocks = sorted(set([8, 16, 32, 64, 128, int(np.ceil(2 * tau))]))
    for b in candidate_blocks:
        if b <= 0:
            continue
        print(
            f"    block={b:4d} samples -> {n // b:4d} blocks, "
            f"block/tau = {b / tau:5.1f}"
            f"{'   <-- >= 2*tau heuristic' if b / tau >= 2 else ''}"
        )
    return tau, n_eff


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n-times", type=int, default=N_CUTOUT_FRAMES)
    p.add_argument("--box", type=int, default=32)
    p.add_argument("--start-frame", type=int, default=1)
    p.add_argument("--time-chunk", type=int, default=32)
    p.add_argument("--cache", default="M_of_t.npy")
    p.add_argument("--token-env", default="JHTDB_TOKEN")
    p.add_argument(
        "--origin",
        type=int,
        nargs=3,
        metavar=("X", "Y", "Z"),
        default=(256, 256, 256),
        help="interior sub-box origin in raw grid indices",
    )
    p.add_argument(
        "--sanity-only",
        action="store_true",
        help="fetch one frame, print max|omega|, and exit without the ACF gate",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    n_times = 1 if args.sanity_only else args.n_times
    cache = args.cache
    if args.sanity_only and cache == "M_of_t.npy":
        cache = "M_of_t_sanity.npy"

    M = fetch_subbox_max(
        n_times=n_times,
        box=args.box,
        cache=cache,
        start_frame=args.start_frame,
        time_chunk=min(args.time_chunk, n_times),
        origin=tuple(args.origin),
        token_env=args.token_env,
    )

    if args.sanity_only:
        print(f"SANITY max|omega| = {M[0]:.8g}")
        print("Sanity fetch complete. Inspect plausibility before the full run.")
        return

    report(M, dt=DT)


if __name__ == "__main__":
    main()
