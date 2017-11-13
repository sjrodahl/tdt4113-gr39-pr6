from behaviour import DriveMode
from motors import Motors
from math import fabs
from time import sleep


class Motob:
    RADIUS = 0.5
    SPEED = 0.5

    def __init__(self):
        self.value = None
        self.motor = Motors()

    def update(self, motor_recommendation):  # hi and lo given only for testing purposes
        # MR follows (Mode, rotation_degrees, speed)
        self.value = motor_recommendation
        self.operationalize()

    def operationalize(self):
        mode, rotation_degrees = self.value

        if mode == DriveMode.DRIVE:
            if rotation_degrees == 0:  # going straight
                self.motor.set_value([self.SPEED, self.SPEED])
            else:
                duration = self.calculate_duration(mode, rotation_degrees)  # 3 and 0.7 works at normal speeds
                turn_speed = [self.RADIUS * self.SPEED, (1 + self.RADIUS) * self.SPEED]
                if rotation_degrees < 0:
                    turn_speed.reverse()
                self.motor.set_value(turn_speed)  # no dur given to maintain movement after turn
                sleep(duration)
                self.motor.set_value([self.SPEED, self.SPEED])  # Zumo continues straight after turn
        elif mode == DriveMode.ROTATE:
            self.motor.left()
            duration = self.calculate_duration(mode, rotation_degrees)  # 0.8 and 0.23 works at normal speeds
            self.motor.left(self.SPEED, duration) if rotation_degrees > 0 else self.motor.right(self.SPEED, duration)


    def calculate_duration(self, mode, rotation_degrees):
        #TODO: simplify with global SPEED value
        if mode == DriveMode.ROTATE:
            return self.transform(0, 1, rotation_degrees)
        elif mode == DriveMode.DRIVE:
            return self.transform(0, 0.8, rotation_degrees)
    
    # gives a duration for a given angle(inp) and a range output for 0 deg turn(out_min) and 90 deg turn(out_max)
    @staticmethod
    def transform(out_min, out_max, inp):
        in_min = 0
        in_max = 90
        inp = fabs(inp)
        return (((inp - in_min) * (out_max - out_min)) / (in_max - in_min)) + out_min

    def halt(self):
        self.motor.stop()
