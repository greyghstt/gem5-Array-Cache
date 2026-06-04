#!/usr/bin/env python3

import csv
import math
import re
import sys
from pathlib import Path


def read_stats(stats_path: Path):
    stats = {}

    with stats_path.open("r", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("-"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            key = parts[0]
            value_str = parts[1]

            try:
                value = float(value_str)
            except ValueError:
                continue

            stats[key] = value

    return stats


def exact(stats, key):
    return stats.get(key)


def first_suffix(stats, suffix, must_contain=None, must_not_contain=None):
    must_contain = [s.lower() for s in (must_contain or [])]
    must_not_contain = [s.lower() for s in (must_not_contain or [])]

    for key, value in stats.items():
        low = key.lower()

        if not low.endswith(suffix.lower()):
            continue

        if any(s not in low for s in must_contain):
            continue

        if any(s in low for s in must_not_contain):
            continue

        return value

    return None


def first_contains(stats, contains_all, contains_any=None):
    contains_all = [s.lower() for s in contains_all]
    contains_any = [s.lower() for s in (contains_any or [])]

    for key, value in stats.items():
        low = key.lower()

        if any(s not in low for s in contains_all):
            continue

        if contains_any and not any(s in low for s in contains_any):
            continue

        return value

    return None


def sum_contains(stats, contains_all, contains_any=None):
    contains_all = [s.lower() for s in contains_all]
    contains_any = [s.lower() for s in (contains_any or [])]

    total = 0.0
    found = False

    for key, value in stats.items():
        low = key.lower()

        if any(s not in low for s in contains_all):
            continue

        if contains_any and not any(s in low for s in contains_any):
            continue

        total += value
        found = True

    return total if found else None


def fmt(value):
    if value is None:
        return ""

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        if value.is_integer():
            return str(int(value))
        return f"{value:.6f}"

    return str(value)


def extract_cache_stats(stats):
    # Nama statistik cache pada Gem5 dapat berbeda tergantung versi dan objek cache.
    # Parser ini dibuat longgar agar tetap bisa mengambil data jika nama statistik mengandung
    # l1d/dcache dan hit/miss/missrate.

    l1d_miss_rate = first_contains(
        stats,
        contains_all=["missrate"],
        contains_any=["l1d", "dcache"],
    )

    l1d_misses = first_contains(
        stats,
        contains_all=["misses"],
        contains_any=["l1d", "dcache"],
    )

    l1d_hits = first_contains(
        stats,
        contains_all=["hits"],
        contains_any=["l1d", "dcache"],
    )

    return l1d_miss_rate, l1d_misses, l1d_hits


def main():
    if len(sys.argv) != 4:
        print("Usage: parse_stats.py <raw_results_dir> <summary_csv> <summary_md>")
        sys.exit(1)

    raw_dir = Path(sys.argv[1])
    csv_path = Path(sys.argv[2])
    md_path = Path(sys.argv[3])

    rows = []

    for exp_dir in sorted(raw_dir.iterdir()):
        if not exp_dir.is_dir():
            continue

        stats_path = exp_dir / "stats.txt"

        if not stats_path.exists():
            continue

        parts = exp_dir.name.split("_")
        mode = parts[0]
        cache = "_".join(parts[1:])

        stats = read_stats(stats_path)

        sim_ticks = exact(stats, "simTicks")
        sim_insts = exact(stats, "simInsts")

        num_cycles = first_suffix(
            stats,
            "numCycles",
            must_contain=["core"],
        )

        if num_cycles is None:
            num_cycles = first_suffix(stats, "numCycles")

        ipc = first_suffix(
            stats,
            "ipc",
            must_contain=["core"],
        )

        if ipc is None and sim_insts is not None and num_cycles not in (None, 0):
            ipc = sim_insts / num_cycles

        l1d_miss_rate, l1d_misses, l1d_hits = extract_cache_stats(stats)

        rows.append({
            "mode": mode,
            "cache": cache,
            "simTicks": sim_ticks,
            "simInsts": sim_insts,
            "numCycles": num_cycles,
            "IPC": ipc,
            "l1d_miss_rate": l1d_miss_rate,
            "l1d_misses": l1d_misses,
            "l1d_hits": l1d_hits,
            "stats_path": str(stats_path),
        })

    rows.sort(key=lambda r: (r["mode"], r["cache"]))

    fieldnames = [
        "mode",
        "cache",
        "simTicks",
        "simInsts",
        "numCycles",
        "IPC",
        "l1d_miss_rate",
        "l1d_misses",
        "l1d_hits",
        "stats_path",
    ]

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({k: fmt(row[k]) for k in fieldnames})

    with md_path.open("w") as f:
        f.write("# Summary Hasil Eksperimen Gem5\n\n")
        f.write("| Mode | Cache | simTicks | simInsts | numCycles | IPC | L1D Miss Rate | L1D Misses | L1D Hits |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")

        for row in rows:
            f.write(
                f"| {row['mode']} | {row['cache']} | {fmt(row['simTicks'])} | "
                f"{fmt(row['simInsts'])} | {fmt(row['numCycles'])} | {fmt(row['IPC'])} | "
                f"{fmt(row['l1d_miss_rate'])} | {fmt(row['l1d_misses'])} | {fmt(row['l1d_hits'])} |\n"
            )

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
