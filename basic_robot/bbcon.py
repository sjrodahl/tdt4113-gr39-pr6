import time
from behaviour import *
from motob import Motob
from RB import *
from Tester_Ultra import *


class Bbcon:
    active_behaviors = set()
    sensobs = []
    behaviors = []

    def __init__(self):
        self.motobs = [Motob()]

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
            return 0    # TODO: How to terminate run?
        for m in self.motobs:
            m.update(mr)
        time.sleep(0.5)
        for s in self.sensobs:
            s.reset()


def main():
    camera = Camera()
    bbcon = Bbcon()
    cam_sensob = RedandBLue(camera)
    ultra_sensob = In_Front()
    turnToRed = FollowRedInIntersection(bbcon, [cam_sensob, ultra_sensob], 1, True)
    bbcon.add_behavior(turnToRed)
    bbcon.add_sensob(cam_sensob)
    while True:
        bbcon.run_one_timestep()


if __name__ == "__main__":
    main()
