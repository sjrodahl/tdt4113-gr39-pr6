
from basic_robot.irproximity_sensor import IRProximitySensor


class StayLeft():

    def __init__(self):

        self.Is_Left = IRProximitySensor.get_value()[1]

    def What_to_do(self):
         if self.Is_Left == True:
             return "Right"
         else:
             return "Left"

class StayRight():
    def __init__(self):

        self.Is_Right = IRProximitySensor.get_value()[0]

    def What_to_do(self):
        if self.Is_Right == True:
            return "Left"
        else:
            return "Right"

class Staybetween():

    def __init__(self):

        self.Between = IRProximitySensor.get_value()

    def What_to_do(self):
        if (self.Between[0] ==True) and (self.Between[1] == True):
            return "Straight"
        elif (self.Between[0] == False) and (self.Between[1] == True):
            return "Right"
        elif (self.Between[0] ==True) and (self.Between[1] == False):
            return "Left"
        else:
            #YEAH WHAT NOW??
            pass



