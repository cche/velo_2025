import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from model import State, run_simulation


def parse_args():
    ap = argparse.ArgumentParser(description="Single bike-share simulation")
    ap.add_argument("--steps", type=int, required=True)
    ap.add_argument("--p1", type=float, required=True, help="Prob mailly->moulin")
    ap.add_argument("--p2", type=float, required=True, help="Prob moulin->mailly")
    ap.add_argument("--init-mailly", type=int, required=True)
    ap.add_argument("--init-moulin", type=int, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--plot", action="store_true")
    return ap.parse_args()


def main():
    args = parse_args()
    df, metrics = run_simulation(
        State(args.init_mailly, args.init_moulin),
        args.steps,
        args.p1,
        args.p2,
        args.seed,
    )
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    with open(args.out_csv.with_suffix(".metrics.csv"), "w") as f:
        f.write("\n".join(f"{k}\t{v}" for k, v in metrics.items()))
    if args.plot:
        plt.figure(figsize=(8, 4))
        plt.plot(df["time"], df["mailly"], label="mailly")
        plt.plot(df["time"], df["moulin"], label="moulin")
        plt.xlabel("time")
        plt.ylabel("bikes")
        plt.title("Bike counts over time")
        plt.legend()
        plt.tight_layout()
        plt.savefig("mailly.png", dpi=150)


if __name__ == "__main__":
    main()
