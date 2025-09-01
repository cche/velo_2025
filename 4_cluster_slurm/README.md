# 4_cluster_slurm

Goal: run the sweep on a Slurm cluster using job arrays.

Files:
- params.csv: parameter grid (one row per run)
- run_one.py: executes a single row (by index) and writes outputs
- sweep_array.sbatch: submit a job array mapping indices to rows
- collect_results.py: aggregates per-run outputs

Submit (edit --array range to match params.csv lines):

```bash
sbatch sweep_array.sbatch
```

After completion:

```bash
python collect_results.py --in-dir results/ --out-dir aggregated/
```
