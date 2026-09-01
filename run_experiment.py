"""Canonical reproducible runner for NS-001.

Usage:
    python run_experiment.py protocols/sanity.json --output-dir outputs/sanity
    python run_experiment.py protocols/day_one.json --output-dir outputs/day_one

The runner records the frozen protocol, source/runtime provenance, hashes of
code and reduced data, and the resulting feasibility statistics in
``receipt.json``. The JHTDB token value is never written to disk.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import ns001_tau_check as ns


REQUIRED_KEYS = {
    "protocol_version",
    "name",
    "purpose",
    "n_times",
    "box",
    "start_frame",
    "time_chunk",
    "origin",
    "sanity_only",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_protocol(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - set(data)
    if missing:
        raise ValueError(f"protocol missing required keys: {sorted(missing)}")
    if int(data["protocol_version"]) != 1:
        raise ValueError(f"unsupported protocol_version={data['protocol_version']}")
    if len(data["origin"]) != 3:
        raise ValueError("protocol origin must contain exactly three integers")
    return data


def verdict_from_n_eff(n_eff: float) -> str:
    if n_eff >= 200:
        return "GREEN"
    if n_eff >= 50:
        return "AMBER"
    return "RED"


def run(protocol_path: Path, output_dir: Path) -> Path:
    protocol_path = protocol_path.resolve()
    protocol = load_protocol(protocol_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    canonical_protocol_path = output_dir / "protocol.json"
    canonical_protocol_path.write_text(
        json.dumps(protocol, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    cache_path = output_dir / "M_of_t.npy"
    n_times = int(protocol["n_times"])
    sanity_only = bool(protocol["sanity_only"])

    if sanity_only and n_times != 1:
        raise ValueError("sanity_only protocols must use n_times=1")

    M = ns.fetch_subbox_max(
        n_times=n_times,
        box=int(protocol["box"]),
        cache=str(cache_path),
        start_frame=int(protocol["start_frame"]),
        time_chunk=min(int(protocol["time_chunk"]), n_times),
        origin=tuple(int(v) for v in protocol["origin"]),
        token_env="JHTDB_TOKEN",
    )

    result: dict[str, object]
    if sanity_only:
        value = float(M[0])
        print(f"SANITY max|omega| = {value:.8g}")
        result = {
            "mode": "sanity",
            "max_vorticity_magnitude": value,
        }
    else:
        tau, n_eff = ns.report(M, dt=ns.DT)
        r = ns.autocorrelation(M)
        below = np.flatnonzero(r < np.exp(-1))
        e_fold = int(below[0]) if below.size else None
        result = {
            "mode": "feasibility",
            "tau_samples": float(tau),
            "tau_physical_time": float(tau * ns.DT),
            "n_eff": float(n_eff),
            "acf_one_over_e_lag_samples": e_fold,
            "screening_verdict": verdict_from_n_eff(float(n_eff)),
            "screening_verdict_is_heuristic": True,
        }

    result_path = output_dir / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    engine_path = Path(ns.__file__).resolve()
    runner_path = Path(__file__).resolve()

    receipt = {
        "receipt_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": {
            "name": protocol["name"],
            "purpose": protocol["purpose"],
            "protocol_sha256": sha256_file(canonical_protocol_path),
            "protocol": protocol,
        },
        "data_source": {
            "dataset": ns.DATASET,
            "jhtdb_endpoint": ns.JHTDB_CUTOUT_URL,
            "grid_n": ns.GRID_N,
            "dx": float(ns.DX),
            "dt": float(ns.DT),
            "raw_cutout_frames": ns.N_CUTOUT_FRAMES,
            "field_retrieved": "velocity",
            "derived_observable": "max_x |curl(u)| over fixed sub-box",
            "finite_difference": "4th-order centered",
            "finite_difference_halo_cells": ns.FD_HALO,
        },
        "source": {
            "commit": os.environ.get("NS001_SOURCE_COMMIT", "unknown"),
            "runner_sha256": sha256_file(runner_path),
            "engine_sha256": sha256_file(engine_path),
        },
        "runtime": {
            "python": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "container_image": os.environ.get("NS001_CONTAINER_IMAGE", "unknown"),
        },
        "artifacts": {
            "M_of_t": cache_path.name,
            "M_of_t_sha256": sha256_file(cache_path),
            "result": result_path.name,
            "result_sha256": sha256_file(result_path),
        },
        "result": result,
        "credential_receipt": {
            "token_environment_variable": "JHTDB_TOKEN",
            "token_value_recorded": False,
        },
        "claim_boundary": [
            "The sub-box maximum is not the global maximum.",
            "A screening verdict is not proof that a GEV/GPD model is valid.",
            "The experiment does not establish or refute Navier-Stokes finite-time blow-up.",
        ],
    }

    receipt_path = output_dir / "receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"receipt: {receipt_path}")
    print(f"M(t) sha256: {receipt['artifacts']['M_of_t_sha256']}")
    return receipt_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("protocol", type=Path, help="frozen JSON protocol")
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="directory for M_of_t.npy, result.json, protocol.json and receipt.json",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run(args.protocol, args.output_dir)


if __name__ == "__main__":
    main()
