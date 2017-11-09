from basic_robot.basic_robot.ultrasonic import Ultrasonic()


class In_Front():

    def __init__(self):

        self.Distance = int(round(Ultrasonic.get_value()))

    def React(self):
        
        if self.Distance < 10:
            return "PICTURE"
        else:
            return None