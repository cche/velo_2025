import argparse
from pathlib import Path
import threading
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for parallel parameter sweep.

    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations
        - out_dir: Output directory for results
        - workers: Number of worker processes ('auto' for automatic detection)
        - plot: Boolean flag to generate plots after run

    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    # TODO: Implement argument parsing
    pass


def main():
    """Main function to run parallel parameter sweep using threading.

    This function should:
    1. Parse command line arguments
    2. Read parameter combinations from CSV file
    3. Set up parallel processing with appropriate number of workers
    4. Submit simulation jobs to worker processes
    5. Collect results as they complete
    6. Aggregate and save results
    7. Optionally generate plots

    Expected parameter CSV columns:
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - seed: Random seed

    Output files:
    - metrics.csv: Aggregated metrics for all runs
    - Optional plots: PNG files for timeseries and metrics visualization

    Note:
        - Use the threading module for parallel processing
    """
    pass


if __name__ == "__main__":
    main()
