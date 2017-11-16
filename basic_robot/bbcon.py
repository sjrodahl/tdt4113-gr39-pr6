import time
from behaviour import *
from motob import Motob
from arbitrator import Arbitrator
from zumo_button import ZumoButton
import sensobs

class Bbcon:
    active_behaviors = set()
    sensobs = []
    behaviors = []

    def __init__(self):
        self.motobs = [Motob()]
        self.arbitrator = Arbitrator(self)
        self.button = ZumoButton()

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
        self.button.update()
        if not self.button.val:
            self.motobs[0].halt()
            return 1

        for b in self.behaviors:
            if b.active_flag:
                b.consider_deactivation()
            else:
                b.consider_activation()
        for s in self.sensobs:
            s.update()
        for b in self.behaviors:
            b.update()
        (mr, halt_req) = self.arbitrator.choose_action()
        if (halt_req):
            # Terminate run
            # TODO: How to terminate run?
            return True     # Freeze all motor functions
        for m in self.motobs:
            m.update(mr)
        #time.sleep(0.2)
        for s in self.sensobs:
            s.reset()
        print(self.active_behaviors)
        return False    # Do not halt


def main():
    z = ZumoButton()
    z.wait_for_press()
    time.sleep(0.5)
    bbcon = Bbcon()
    cam_sensob = sensobs.RedandBlueSensob(bbcon)
    ultra_sensob = sensobs.UltrasonicSensob(bbcon)
    reflector = sensobs.ReflectanceSensob(bbcon)
    followlineBehaviour = follow_line(bbcon, [reflector], 0.4, True)
    followRedBehavior = FollowRedInIntersection(bbcon, [cam_sensob, ultra_sensob], 1, False)

    halt = False
    while not halt:
        halt = bbcon.run_one_timestep()


if __name__ == "__main__":
    main()
