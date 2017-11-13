import time
from behaviour import *
from motob import Motob
from sensobs import *
from arbitrator import Arbitrator



class Bbcon:
    active_behaviors = set()
    sensobs = []
    behaviors = []

    def __init__(self):
        self.motobs = [Motob()]
        self.arbitrator = Arbitrator(self)

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)
        if behavior.active_flag:
            self.activate_behavior(behavior)

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
            # TODO: How to terminate run?
            return True     # Freeze all motor functions
        for m in self.motobs:
            m.update(mr)
        time.sleep(0.5)
        for s in self.sensobs:
            s.reset()
        return False    # Do not halt


def main():
    bbcon = Bbcon()
    cam_sensob = RedandBlueSensob(bbcon)
    ultra_sensob = UltrasonicSensob(bbcon)
    followRedBehavior = FollowRedInIntersection(bbcon, [cam_sensob, ultra_sensob], 1, True)

    halt = False
    while not halt:
        halt = bbcon.run_one_timestep()


if __name__ == "__main__":
    main()
