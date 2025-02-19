import os
import time
import multiprocessing
import argparse

from aw_engine import Simulator
from aw_engine.generative_agents_simple import TheVille, SimpleAgent

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--num-processes", type=int, default=os.cpu_count())
    parser.add_argument("--base-step", type=int, default=2880)
    parser.add_argument("--target-step", type=int, default=3060)

    parser.add_argument("--num-agents", type=int, default=25)
    parser.add_argument("--cache", action="store_true", default=False)

    parser.add_argument("--mode",
                        type=str,
                        default="async",
                        choices=["async", "sync", "no-dependency", "oracle-dependency"])
    parser.add_argument("--priority", action="store_true", default=False)

    # parser.add_argument("--sync", action="store_true", default=False)
    # parser.add_argument("--no-dependency", action="store_true", default=False)
    # parser.add_argument("--oracle-dependency", action="store_true", default=False)

    base_step = parser.parse_args().base_step
    target_step = parser.parse_args().target_step
    num_agents = parser.parse_args().num_agents
    num_processes = min(parser.parse_args().num_processes, num_agents)
    material_cache = parser.parse_args().cache
    mode = parser.parse_args().mode
    if mode == "no-dependency":
        num_processes = 128
    priority = parser.parse_args().priority

    sim = Simulator(TheVille, base_step=base_step, num_agents=num_agents, cache=material_cache)
    multiprocessing.freeze_support()
    tic = time.time()
    sim.run(target_step, SimpleAgent, num_processes=num_processes, mode=mode, priority=priority)
    duration = time.time() - tic
    print(
        f"Simulation from step {base_step} to {target_step} for {num_agents} agents took {duration:.2f} seconds with {num_processes} processes."
    )
