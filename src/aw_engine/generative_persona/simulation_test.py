import multiprocessing


from aw_engine.generative_agents_simple import TheVille
from generative_agent_new import GenerativeAgent
import sys
sys.path.append("../")
from simulator_generative import Simulator

if __name__ == '__main__':
    sim = Simulator(TheVille, 2880)
    multiprocessing.freeze_support()
    sim.run(3600, GenerativeAgent, num_processes=16)
