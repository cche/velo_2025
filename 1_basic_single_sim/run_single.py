import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from model import State, run_simulation


def parse_args():
    """Parse command line arguments for single simulation run.

    Returns:
        Parsed arguments containing:
        - steps: Number of simulation steps
        - p1: Probability of movement from Mailly to Moulin
        - p2: Probability of movement from Moulin to Mailly
        - init_mailly: Initial bikes at Mailly station
        - init_moulin: Initial bikes at Moulin station
        - seed: Random seed (default: 0)
        - out_csv: Output CSV file path
        - plot: Boolean flag to generate plots

    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, help="Nombre des pas a executer")
    parser.add_argument("--p1", type=float, help="probabilité velo vers mailly")
    parser.add_argument("--p2", type=float, help="probabilité velo vers moulin")
    parser.add_argument("--init-mailly", type=int, help="Nombre velo initial mailly")
    parser.add_argument("--init-moulin", type=int, help="Nombre velo initial moulin")
    parser.add_argument(
        "--seed", type=int, default=0, help="Seed pour reproductibilité"
    )
    parser.add_argument("--out-csv", help="Data output")
    parser.add_argument(
        "--plot",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def main():
    """Main function to run a single bike-sharing simulation.

    This function should:
    1. Parse command line arguments
    2. Run the simulation with specified parameters
    3. Save results to CSV files (timeseries and metrics)
    4. Optionally generate and save plots

    Output files:
    - Timeseries data: CSV with time, mailly, moulin columns
    - Metrics data: CSV with key-value pairs of simulation metrics
    - Optional plot: PNG showing bike counts over time for both stations

    Note:
        Create output directories if they don't exist
        Save metrics as tab-separated key-value pairs
    """
    options = parse_args()

    state = State(options.init_mailly, options.init_moulin)
    metrics = run_simulation(
        options.init_mailly,
        options.init_moulin,
        options.steps,
        options.p1,
        options.p2,
        options.seed,
    )

    metrics_path = Path(options.out_csv)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metrics_path, "w") as f:
        for k, v in metrics.items():
            v_out = []
            for i in v:
                v_out.append(str(i))
            f.write(f"{k}\t{'\t'.join(v_out)}\n")

    if options.plot:
        # preparer les données pour le plot
        time = []
        mailly = []
        moulin = []
        unmet_mailly = []
        unmet_moulin = []
        balance = []

        for k, v in metrics.items():
            time.append(k)
            mailly.append(v[0])
            moulin.append(v[1])
            unmet_mailly.append(v[2])
            unmet_moulin.append(v[3])
            balance.append(v[4])

        # generer le plot
        plt.figure(figsize=(12, 8))
        plt.plot(time, mailly, label="Mailly")
        plt.plot(time, moulin, label="Moulin")
        plt.plot(time, balance, label="Balance")
        plt.plot(time, unmet_mailly, label="Unmet Mailly")
        plt.plot(time, unmet_moulin, label="Unmet Moulin")
        plt.xlabel("Time")
        plt.ylabel("Bikes")
        plt.legend()
        plt.savefig(metrics_path.with_suffix(".png"))

        # fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        # fig.set_size_inches(12, 8)
        # fig.subplots_adjust(hspace=0.5)
        # ax1.plot(time, mailly, label="Mailly")
        # ax1.plot(time, moulin, label="Moulin")
        # ax1.set_title("Velos Mailly-Moulin")
        # ax1.set_xlabel("Temps")
        # ax1.set_ylabel("nombre")
        # ax1.legend()
        #
        # ax2.plot(time, unmet_mailly, label="Unmet Mailly")
        # ax2.plot(time, unmet_moulin, label="Unmet Moulin")
        # ax2.set_title("Unmet Mailly-Moulin")
        # ax2.set_xlabel("Temps")
        # ax2.set_ylabel("nombre")
        # ax2.legend()
        #
        # ax3.plot(time, balance, label="Balance")
        # ax3.set_title("Balance Mailly-Moulin")
        # ax3.axhline(y=0, color="black", linestyle="--")
        # ax3.set_xlabel("Temps")
        # ax3.set_ylabel("nombre")
        # ax3.legend()
        # plt.savefig(metrics_path.parent / (metrics_path.stem + "_3plot.png"))


if __name__ == "__main__":
    main()
