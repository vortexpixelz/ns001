"""
NS-001 :: Day-One Feasibility Check
===================================
Measures the integral time scale tau of M(t) = max|omega| and the
effective number of INDEPENDENT extremes in the record.

This is the go/no-go gate. Run it BEFORE building any EVT pipeline.

Why: GEV/GPD fits need independent block maxima. M(t) is highly
autocorrelated -- successive maxima often track the SAME long-lived
vortex structure. If N_eff is ~20, your confidence intervals on the
shape parameter xi will be too wide to distinguish xi<0 from xi>0,
and the study is dead no matter what the physics says.

You do NOT need the full 27 TB. A sub-box max is a lower bound on the
global max, but it inherits essentially the same correlation structure,
which is the only thing being measured here.

Usage:
    1. Fill in fetch_subbox_max() with your JHTDB call.
    2. python ns001_tau_check.py
    3. Read the verdict at the bottom.
"""

import numpy as np

# ----------------------------------------------------------------------
# STEP 1: get M(t). Replace the stub with a real JHTDB fetch.
# ----------------------------------------------------------------------

def fetch_subbox_max(n_times=1024, box=128, cache="M_of_t.npy"):
    """
    Return M(t): shape (n_times,), the max vorticity magnitude inside a
    fixed box x box x box sub-volume, at each stored timestep.

    Fetch 'vorticity' (not velocity -- let the server do the curl), take
    np.abs then .max() per timestep, append. Cache to disk: you only
    want to pay for this download once.

    Cost estimate: 128^3 x 3 components x 4 bytes x 1024 steps ~ 8 GB.
    """
    import os
    if os.path.exists(cache):
        return np.load(cache)

    raise NotImplementedError(
        "Plug in your JHTDB fetch here, save to %s, and rerun.\n"
        "Sanity check first: pull ONE timestep, confirm the shape and\n"
        "that the magnitude is physically plausible, before looping 1024x."
        % cache
    )


# ----------------------------------------------------------------------
# STEP 2: autocorrelation and integral time scale
# ----------------------------------------------------------------------

def autocorrelation(x):
    """Normalized ACF via FFT. r[0] == 1."""
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    n = len(x)
    f = np.fft.rfft(x, n=2 * n)          # zero-pad: linear, not circular
    acf = np.fft.irfft(f * np.conj(f))[:n]
    return acf / acf[0]


def integral_time_scale(r):
    """
    Sum the ACF out to its first zero crossing (initial positive
    sequence). Truncating there is standard -- integrating into the
    noisy tail inflates tau without adding signal.
    Returns tau in units of SAMPLES.
    """
    zero = np.argmax(r <= 0)
    if zero == 0:                         # never crosses
        zero = len(r)
    return 1.0 + 2.0 * r[1:zero].sum()


def report(M, dt=1.0):
    n = len(M)
    r = autocorrelation(M)
    tau = integral_time_scale(r)
    n_eff = n / tau

    print("=" * 58)
    print("NS-001 FEASIBILITY :: autocorrelation of M(t) = max|omega|")
    print("=" * 58)
    print(f"  samples in record        n     = {n}")
    print(f"  integral time scale      tau   = {tau:.2f} samples"
          f"  ({tau * dt:.3g} in physical time)")
    print(f"  EFFECTIVE INDEPENDENT    N_eff = {n_eff:.1f}")
    print(f"  ACF drops below 1/e at         : "
          f"{np.argmax(r < np.exp(-1))} samples")
    print("-" * 58)

    if n_eff >= 200:
        print("  VERDICT: GREEN. Enough independent extremes for GEV/GPD.")
        print("  -> Build the pipeline. Block size >= 2*tau, and report")
        print("     N_eff (not n) as your sample size in the paper.")
    elif n_eff >= 50:
        print("  VERDICT: AMBER. Workable but CIs will be wide.")
        print("  -> Go POT/GPD over block-maxima (uses more of the record).")
        print("  -> Bootstrap the CI on xi before claiming any sign.")
        print("  -> Say plainly in the note that power is limited.")
    else:
        print("  VERDICT: RED. Too few independent extremes.")
        print("  -> Do NOT claim a sign for xi off this record.")
        print("  -> The honest paper is now about the LIMITS of what")
        print("     current public DNS records can support for EVT.")
        print("     That is still novel, still publishable, and it is")
        print("     exactly falsification criterion #2 firing as designed.")
    print("=" * 58)

    # Block-size guidance: blocks must be long vs tau or maxima correlate.
    for b in (8, 16, 32, 64, 128):
        print(f"    block={b:4d} samples -> {n // b:4d} blocks, "
              f"block/tau = {b / tau:5.1f}"
              f"{'   <-- usable' if b / tau >= 2 else ''}")
    return tau, n_eff


if __name__ == "__main__":
    M = fetch_subbox_max()
    report(M)
