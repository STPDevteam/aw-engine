
from action import Action
from event import Event
from memory import Memory
class Agent:
    '''
    This class is the base class for all agents
    The instance of the agent will be empheral and will be created and destroyed during the simulation
    '''
    def __init__(self, name, memory, env, step):
        self.name = name
        self.memory = memory
        self.env = env
        self.step = step

    def perceive(self) -> list[Event]:
        return self.env.perceive_events()
            
    def proceed(self):
        # this will be implemented in the derived classes
        raise NotImplementedError

    