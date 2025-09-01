import argparse
from pathlib import Path
import concurrent.futures as cf
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation


def parse_args():
    ap = argparse.ArgumentParser(description="Parallel parameter sweep (local)")
    ap.add_argument("--params", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--workers", default="auto", help="int or 'auto'")
    ap.add_argument("--plot", action="store_true", help="Plot results after run")
    return ap.parse_args()


def worker(args_tuple):
    run_id, row = args_tuple
    df, metrics = run_simulation(
        State(int(row.init_mailly), int(row.init_moulin)),
        int(row.steps), float(row.p1), float(row.p2), int(row.seed)
    )
    return run_id, row.to_dict(), df, metrics


def main():
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    params = pd.read_csv(args.params)
    if args.workers == "auto":
        max_workers = None
    else:
        max_workers = int(args.workers)

    metrics_rows = []
    ts_rows = []

    with cf.ProcessPoolExecutor(max_workers=max_workers) as ex:
        for run_id, row in params.iterrows():
            pass
        futures = [ex.submit(worker, (run_id, row)) for run_id, row in params.iterrows()]
        for fut in cf.as_completed(futures):
            run_id, row_dict, df, metrics = fut.result()
            metrics_rows.append({"run_id": run_id, **metrics, **row_dict})
            ts_long = df.melt(id_vars=["time"], var_name="station", value_name="count")
            ts_long.insert(0, "run_id", run_id)
            ts_rows.append(ts_long)

    metrics_df = pd.DataFrame(metrics_rows)
    ts_df = pd.concat(ts_rows, ignore_index=True)

    metrics_df.to_csv(args.out_dir / "metrics.csv", index=False)
    ts_df.to_csv(args.out_dir / "timeseries.csv", index=False)

    if args.plot:
        # Plot timeseries overlays per station
        for station_name in ts_df["station"].unique():
            plt.figure(figsize=(10, 6))
            station_data = ts_df[ts_df["station"] == station_name]
            for run_id in pd.unique(station_data["run_id"]):
                run_data = station_data[station_data["run_id"] == run_id]
                plt.plot(run_data["time"], run_data["count"], label=f"Run {run_id}")
            plt.title(f"Timeseries for station: {station_name}")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(args.out_dir / f"timeseries_{station_name}.png", dpi=150)
            plt.close()

        # Plot standard metric columns per run
        value_cols = [
            c for c in metrics_df.columns
            if c in [
                "unmet_mailly",
                "unmet_moulin",
                "stockout_mailly_steps",
                "stockout_moulin_steps",
                "final_imbalance",
            ]
        ]
        for col in value_cols:
            plt.figure(figsize=(8, 5))
            metrics_df.set_index("run_id")[col].plot(kind="bar")
            plt.title(f"Metric per run: {col}")
            plt.xlabel("Run ID")
            plt.ylabel(col)
            plt.tight_layout()
            plt.savefig(args.out_dir / f"metric_{col}.png", dpi=150)
            plt.close()


if __name__ == "__main__":
    main()
