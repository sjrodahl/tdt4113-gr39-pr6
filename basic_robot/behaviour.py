
class Behaviour:

    halt_request = False
    match_degree = 0
    weight = 0      #priority * match_degree

    def __init__(self, bbcon, sensobs, priority, active_flag):
        self.bbcon = bbcon
        self.sensobs = sensobs
        self.priority = priority
        self.active_flag = active_flag

    def consider_deactivation(self):
        #Override this method: use the values from the sensobs to determine if you should deactivate
        pass

    def consider_activation(self):
        #Override this method: use the values from the sensobs to determine if you should activate
        pass

    def sense_and_act(self):
        #Override this method to produce motor recommendations based on sensob values
        # This method should update self.motor_recommendations and self.match_degree
        pass

    def update(self):
        self.consider_deactivation() if self.active_flag else self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree*self.priority