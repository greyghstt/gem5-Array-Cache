set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GEM5_ROOT="${GEM5_ROOT:-$HOME/gem5}"
GEM5_BIN="${GEM5_BIN:-$GEM5_ROOT/build/X86/gem5.opt}"

SRC="$PROJECT_ROOT/src/array_access.c"
BINARY="$PROJECT_ROOT/build/array_access"

SIZE="${SIZE:-131072}"
REPEATS="${REPEATS:-8}"
STRIDE="${STRIDE:-16}"

MODES=("seq" "stride" "random")
CACHES=("nocache" "l1_16k" "l1_32k" "l1_l2")

mkdir -p "$PROJECT_ROOT/build"
mkdir -p "$PROJECT_ROOT/results/raw"

echo "[1/3] Checking Gem5 binary..."
if [ ! -x "$GEM5_BIN" ]; then
    echo "Gem5 binary not found or not executable: $GEM5_BIN"
    exit 1
fi

echo "[2/3] Compiling benchmark..."
gcc -O2 -static -Wall -Wextra -o "$BINARY" "$SRC"

echo "Benchmark binary:"
file "$BINARY"

echo "[3/3] Running simulations..."
for mode in "${MODES[@]}"; do
    for cache in "${CACHES[@]}"; do
        EXP_NAME="${mode}_${cache}"
        OUTDIR="$PROJECT_ROOT/results/raw/$EXP_NAME"

        mkdir -p "$OUTDIR"

        echo "Running: mode=$mode cache=$cache"

        "$GEM5_BIN" \
            -d "$OUTDIR" \
            "$PROJECT_ROOT/configs/run_array_cache.py" \
            --binary "$BINARY" \
            --mode "$mode" \
            --cache "$cache" \
            --size "$SIZE" \
            --repeats "$REPEATS" \
            --stride "$STRIDE" \
            > "$OUTDIR/terminal.log" 2>&1

        if [ ! -f "$OUTDIR/stats.txt" ]; then
            echo "stats.txt not found for $EXP_NAME"
            exit 1
        fi

        echo "Done: $EXP_NAME"
    done
done

echo "Parsing results..."
python3 "$PROJECT_ROOT/scripts/parse_stats.py" \
    "$PROJECT_ROOT/results/raw" \
    "$PROJECT_ROOT/results/summary.csv" \
    "$PROJECT_ROOT/results/summary.md"

echo "All experiments completed."
echo "CSV summary: $PROJECT_ROOT/results/summary.csv"
echo "Markdown summary: $PROJECT_ROOT/results/summary.md"
