# 3_parallel_local

Goal: accelerate the sweep using local CPU cores via ProcessPoolExecutor.

Run:

```bash
python run_parallel.py --params params.csv --workers auto --out-dir results/
```

Notes:
- Avoid globals to ensure picklability and correctness.
- Seeds are passed per-run for deterministic results.
