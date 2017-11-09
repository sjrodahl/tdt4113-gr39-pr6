import time
from behaviour import *
from motob import *

class Bbcon:
    active_behaviors = set()

    def __init__(self, behaviors, sensobs, motobs, arbitrator):
        self.behaviors = behaviors
        self.sensobs = sensobs
        self.motobs = motobs
        self.arbitrator = arbitrator

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        self.active_behaviors.add(behavior)

    def deactivate_behavior(self, behavior):
        self.active_behaviors.discard(behavior) #discard removes x if x is present in the set

    def run_one_timestep(self):
        for s in self.sensobs:
            s.update()
        for b in self.active_behaviors:
            b.update()
        (mr, halt_req) = self.arbitrator.choose_action()
        if (halt_req):
            # Terminate run
            return 0    # TODO: How to terminate run?
        for m in self.motobs:
            m.update(mr)
        time.sleep(0.5)
        for s in self.sensobs:
            s.reset()
