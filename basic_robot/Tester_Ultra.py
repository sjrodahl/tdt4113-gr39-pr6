from ultrasonic import Ultrasonic


class In_Front():

    def __init__(self):
        self.ultra = Ultrasonic()
        self.Distance = int(round(ultra.get_value()))

    def React(self):
        
        if self.Distance < 10:
            return "PICTURE"
        else:
            return None
    def update(self):
        self.ultra.update()
        self.distance= int(round(self.ultra.get_value()))
