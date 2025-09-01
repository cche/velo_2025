import argparse
import json
from pathlib import Path
import pandas as pd

from model import State, run_simulation


def parse_args():
    ap = argparse.ArgumentParser(description="Run one simulation specified by a row in params.csv")
    ap.add_argument("--params", type=Path, default=Path("params.csv"))
    ap.add_argument("--row-index", type=int, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--base-seed", type=int, default=0, help="Used if the row has no seed column")
    return ap.parse_args()


def main():
    args = parse_args()
    params = pd.read_csv(args.params)
    row = params.iloc[args.row_index]

    seed = int(row.seed) if "seed" in row and not pd.isna(row.seed) else args.base_seed + args.row_index

    df, metrics = run_simulation(
        State(int(row.init_mailly), int(row.init_moulin)),
        int(row.steps), float(row.p1), float(row.p2), seed
    )

    outdir = args.out_dir / str(args.row_index)
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "timeseries.csv", index=False)
    pd.DataFrame([{**metrics}]).to_csv(outdir / "metrics.csv", index=False)

    meta = row.to_dict()
    meta.update({"seed": seed})
    with open(outdir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)


if __name__ == "__main__":
    main()
