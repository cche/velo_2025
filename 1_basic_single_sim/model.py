from dataclasses import dataclass
from typing import Tuple, Dict
import numpy as np
import pandas as pd


@dataclass
class State:
    mailly: int
    moulin: int


def step(
    state: State,
    p1: float,
    p2: float,
    rng: np.random.Generator,
    metrics: Dict[str, int],
) -> State:
    # User tries to go from mailly -> moulin with prob p1
    if rng.random() < p1:
        if state.mailly > 0:
            state.mailly -= 1
            state.moulin += 1
        else:
            metrics["unmet_mailly"] += 1
    # User tries to go from moulin -> mailly with prob p2
    if rng.random() < p2:
        if state.moulin > 0:
            state.moulin -= 1
            state.mailly += 1
        else:
            metrics["unmet_moulin"] += 1
    return state


def run_simulation(
    initial: State, steps: int, p1: float, p2: float, seed: int
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    rng = np.random.default_rng(seed)
    state = State(initial.mailly, initial.moulin)
    times = [0]
    mailly = [state.mailly]
    moulin = [state.moulin]
    metrics = {"unmet_mailly": 0, "unmet_moulin": 0}

    for t in range(1, steps + 1):
        state = step(state, p1, p2, rng, metrics)
        times.append(t)
        mailly.append(state.mailly)
        moulin.append(state.moulin)

    df = pd.DataFrame({"time": times, "mailly": mailly, "moulin": moulin})
    metrics["final_imbalance"] = state.mailly - state.moulin
    return df, metrics
