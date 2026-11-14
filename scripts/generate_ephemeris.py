#!/usr/bin/env python3
"""
generate_ephemeris.py
Generates accurate lunar ephemeris (sub-solar and sub-Earth selenographic coordinates)
using SPICE kernels (DE440s + high-precision lunar libration frame MOON_ME).

Time range: 2025-01-01T00:00:00Z to 2035-12-31T23:00:00Z
Step: 1 hour (3600 seconds)
Output: data/ephemeris.json
"""

import os
import json
import time
import datetime
import numpy as np
import spiceypy as spice

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    kernels_dir = os.path.join(workspace_dir, "kernels")
    data_dir = os.path.join(workspace_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Required SPICE kernels
    kernel_files = [
        "naif0012.tls",
        "pck00010.tpc",
        "moon_080317.tf",
        "moon_pa_de421_1900-2050.bpc",
        "de440s.bsp",
    ]

    for k in kernel_files:
        kpath = os.path.join(kernels_dir, k)
        if not os.path.exists(kpath):
            raise FileNotFoundError(f"Missing kernel: {kpath}. Run download_kernels.py first.")
        spice.furnsh(kpath)

    print("Loaded SPICE kernels successfully.")

    # Time bounds (UTC)
    t0_str = "2025-01-01T00:00:00"
    t1_str = "2035-12-31T23:00:00"
    
    t0_et = spice.str2et(t0_str)
    t1_et = spice.str2et(t1_str)
    
    # Start timestamp in milliseconds UTC
    t0_dt = datetime.datetime.fromisoformat(t0_str + "+00:00")
    t0_ms = int(t0_dt.timestamp() * 1000)
    step_sec = 3600
    step_ms = step_sec * 1000

    n_steps = int(round((t1_et - t0_et) / step_sec)) + 1
    print(f"Generating {n_steps} hourly steps from {t0_str} to {t1_str}...")

    t_start = time.time()
    # Pre-allocate records: [slat, slon, elat, elon]
    # MOON_ME is the Moon Mean Earth/Polar Axis frame with high-precision libration
    frame = "MOON_ME"
    records = []

    for i in range(n_steps):
        et = t0_et + i * step_sec
        
        # Sun position relative to Moon center
        sun_pos, _ = spice.spkpos("SUN", et, frame, "LT+S", "MOON")
        _, sun_lon, sun_lat = spice.reclat(sun_pos)
        
        # Earth position relative to Moon center
        earth_pos, _ = spice.spkpos("EARTH", et, frame, "LT+S", "MOON")
        _, earth_lon, earth_lat = spice.reclat(earth_pos)

        # Convert to degrees, rounding to 3 decimals (0.001 deg precision)
        slat = round(float(np.degrees(sun_lat)), 3)
        slon = round(float(np.degrees(sun_lon)), 3)
        elat = round(float(np.degrees(earth_lat)), 3)
        elon = round(float(np.degrees(earth_lon)), 3)

        records.append([slat, slon, elat, elon])

        if (i + 1) % 10000 == 0 or (i + 1) == n_steps:
            elapsed = time.time() - t_start
            pct = (i + 1) / n_steps * 100
            print(f"  {i + 1}/{n_steps} ({pct:.1f}%) in {elapsed:.1f}s")

    ephemeris_data = {
        "version": "1.0",
        "description": "High-precision lunar ephemeris from JPL DE440 + MOON_ME libration frame",
        "t0": t0_ms,
        "t0_iso": t0_str + "Z",
        "step_ms": step_ms,
        "step_h": 1,
        "count": len(records),
        "fields": ["sun_lat", "sun_lon", "earth_lat", "earth_lon"],
        "units": "degrees, selenographic (Mean Earth/Polar Axis), lon range [-180, 180]",
        "data": records
    }

    out_path = os.path.join(data_dir, "ephemeris.json")
    print(f"Writing {out_path} ...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ephemeris_data, f, separators=(',', ':'))

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Done! Created {out_path} ({size_mb:.2f} MB, {len(records)} points)")
    spice.kclear()

if __name__ == "__main__":
    main()

