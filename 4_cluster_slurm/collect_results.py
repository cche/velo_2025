import argparse
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    ap = argparse.ArgumentParser(
        description="Collect per-run outputs into aggregated CSVs"
    )
    ap.add_argument("--in-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument(
        "--plot", action="store_true", help="Plot the results after collection"
    )
    return ap.parse_args()


def main():
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    metrics_rows = []
    ts_rows = []

    for sub in sorted(p for p in args.in_dir.iterdir() if p.is_dir()):
        rid = int(sub.name)
        # metrics
        mpath = sub / "metrics.csv"
        if mpath.exists():
            m = pd.read_csv(mpath).iloc[0].to_dict()
            m["run_id"] = rid
            # add metadata if present
            meta_path = sub / "metadata.json"
            if meta_path.exists():
                with open(meta_path) as f:
                    meta = json.load(f)
                m.update({f"param_{k}": v for k, v in meta.items()})
            metrics_rows.append(m)
        # timeseries
        tpath = sub / "timeseries.csv"
        if tpath.exists():
            df = pd.read_csv(tpath)
            df.insert(0, "run_id", rid)
            ts_rows.append(
                df.melt(
                    id_vars=["run_id", "time"], var_name="station", value_name="count"
                )
            )

    if metrics_rows:
        pd.DataFrame(metrics_rows).to_csv(args.out_dir / "metrics.csv", index=False)
    if ts_rows:
        ts_df = pd.concat(ts_rows, ignore_index=True)
        ts_df.to_csv(args.out_dir / "timeseries.csv", index=False)
        if args.plot:
            # Plotting timeseries (example: line plot for each station)
            for station_name in ts_df["station"].unique():
                plt.figure(figsize=(12, 7))
                station_data = ts_df[ts_df["station"] == station_name]
                for run_id in pd.unique(station_data["run_id"]):
                    run_data = station_data[station_data["run_id"] == run_id]
                    plt.plot(run_data["time"], run_data["count"], label=f"Run {run_id}")
                plt.title(f"Timeseries for Station: {station_name}")
                plt.xlabel("Time")
                plt.ylabel("Count")
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(args.out_dir / f"timeseries_{station_name}.png")
                plt.close()

    if args.plot:
        if metrics_rows:
            metrics_df = pd.DataFrame(metrics_rows)
            # Plotting metrics (example: bar plot for each metric)
            for col in metrics_df.columns.drop(
                ["run_id"] + [c for c in metrics_df.columns if c.startswith("param_")]
            ):
                plt.figure(figsize=(10, 6))
                metrics_df.set_index("run_id")[col].plot(kind="bar")
                plt.title(f"Metric: {col} per run")
                plt.xlabel("Run ID")
                plt.ylabel(col)
                plt.tight_layout()
                plt.savefig(args.out_dir / f"metric_{col}.png")
                plt.close()


if __name__ == "__main__":
    main()
