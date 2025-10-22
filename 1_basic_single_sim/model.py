from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass
class State:
    """Represents the state of bikes at two stations.

    Attributes:
        mailly: Number of bikes at Mailly station
        moulin: Number of bikes at Moulin station
        unmet_mailly: Number of unmet requests at Mailly
        unmet_moulin: Number of unmet requests at Moulin
    """

    mailly: int
    moulin: int
    unmet_mailly: int = 0
    unmet_moulin: int = 0


def step(state: State, p1: float, p2: float, rng: np.random.Generator) -> State:
    """Simulate one time step of the bike-sharing system.

    Args:
        state: Current state of the system (bike counts at each station)
        p1: Probability of a user wanting to go from Mailly to Moulin
        p2: Probability of a user wanting to go from Moulin to Mailly
        rng: Random number generator for stochastic events

    Returns:
        Updated state after one simulation step

    Note:
        - If a station has no bikes available, increment the appropriate unmet demand counter
        - Update the state by moving bikes between stations based on probabilities
    """
    # User tries to go from mailly -> moulin with prob p1
    if rng.random() < p1:
        if state.mailly <= 0:
            state.unmet_mailly += 1
        else:
            state.mailly -= 1
            state.moulin += 1

    # User tries to go from moulin -> mailly with prob p2
    if rng.random() < p2:
        if state.moulin <= 0:
            state.unmet_moulin += 1
        else:
            state.moulin -= 1
            state.mailly += 1

    return state


def run_simulation(
    init_mailly: int, init_moulin: int, steps: int, p1: float, p2: float, seed: int
) -> Dict[str, list[int]]:
    """Run a complete bike-sharing simulation.

    Args:
        initial: Initial state of the system
        steps: Number of simulation steps to run
        p1: Probability of movement from Mailly to Moulin
        p2: Probability of movement from Moulin to Mailly
        seed: Random seed for reproducibility

    Returns:
        Tuple containing:
        - DataFrame with columns ['time', 'mailly', 'moulin'] tracking bike counts over time
        - Dictionary with metrics including:
            - 'unmet_mailly': Number of unmet requests at Mailly
            - 'unmet_moulin': Number of unmet requests at Moulin
            - 'final_imbalance': Final difference between station bike counts

    Note:
        - Initialize metrics dictionary with appropriate counters
        - Record state at each time step for the DataFrame
        - Calculate final imbalance as mailly - moulin
    """
    rng = np.random.default_rng(seed)

    metrics = {}
    state = State(init_mailly, init_moulin)
    for time in range(steps):
        state = step(state, p1, p2, rng)
        metrics[time] = [
            state.mailly,
            state.moulin,
            state.unmet_mailly,
            state.unmet_moulin,
            state.mailly - state.moulin,
        ]

    return metrics
