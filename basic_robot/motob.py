from behaviour import DriveMode
from motors import Motors
from math import fabs
from time import sleep


class Motob:
    RADIUS = 0.5

    def __init__(self):
        self.value = None
        self.motor = Motors()

    def update(self, motor_recommendation, hi, lo):  # hi and lo given only for testing purposes
        # MR follows (Mode, rotation_degrees, speed)
        self.value = motor_recommendation
        self.operationalize(hi, lo)

    def operationalize(self, hi, lo):
        mode, rotation_degrees, speed = self.value

        if speed == 0:
            self.motor.stop()
        elif mode == DriveMode.DRIVE:
            if rotation_degrees == 0:  # going straight
                self.motor.set_value([speed, speed])
            else:
                duration = self.calculate_duration(rotation_degrees, speed, hi, lo)  # 3 and 0.7 works at normal speeds
                turn_speed = [self.RADIUS * speed, (1 + self.RADIUS) * speed]
                if rotation_degrees < 0:
                    turn_speed.reverse()
                self.motor.set_value(turn_speed)  # no dur given to maintain movement after turn
                sleep(duration)
                self.motor.set_value([speed, speed])  # Zumo continues straight after turn
        elif mode == DriveMode.ROTATE:
            self.motor.left()
            duration = self.calculate_duration(rotation_degrees, speed, hi, lo)  # 0.8 and 0.23 works at normal speeds
            self.motor.left(speed, duration) if rotation_degrees > 0 else self.motor.right(speed, duration)

    @staticmethod
    def calculate_duration(rotation_degrees, speed, hi, lo):
        # hi and lo are time of 90 deg turn at hi/lo speed
        # calculation becomes difficult given two variables. Global speed should be considered later
        delta_hi = hi / 90
        delta_lo = lo / 90
        return fabs(rotation_degrees) * (delta_hi - (delta_hi - delta_lo) * fabs(speed))
