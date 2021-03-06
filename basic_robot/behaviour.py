from enum import Enum
#from sensobs import *


class DriveMode(Enum):
    DRIVE = 1
    ROTATE = 2
    HALT = 3

class Behaviour:
    ROTATE_DEGREES = 10

    

    def __init__(self, bbcon, sensobs, priority, active_flag = True):
        self.motor_recommendations = None
        self.halt_request = False
        self.match_degree = 0
        self.weight = 0      #priority * match_degreeself.bbcon = bbcon
        self.sensobs = sensobs
        self.bbcon = bbcon
        for s in self.sensobs:
            s.add_behavior(self)
        self.priority = priority
        self.active_flag = active_flag
        self.bbcon.add_behavior(self)
    
    def __str__(self):
        return(str(self.__class__.__name__))

    def consider_deactivation(self):
        """Use the sensobs-values to determine activation. This method should always be overridden"""
        pass

    def consider_activation(self):
        print("fuck")
        """Use the sensobs-values to determine deactivation. This method should always be overridden"""
        pass

    def sense_and_act(self):
        """Update self.motor_recommendations and self.match_degree. This method should always be overridden"""
        pass

    def update(self):
        """Activates/Deactivates the behaviour. Act on the current sensor values and updates the behaviours weight"""
        #self.consider_deactivation() if self.active_flag else self.consider_activation()
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree*self.priority

    def calculate_match_degree(self):
        return 0

    def __gt__(self, other):
        return self.weight > other.weight



class AvoidWalls(Behaviour):
    # self.sensobs is i single sensob for for ir-proximity sensor
    last_rotate_was_clockwise = True  # To toggle the turndirection in case of no walls detected

    def update(self):
        """Activates/Deactivates the behaviour. Act on the current sensor values and updates the behaviours weight"""
        #self.consider_deactivation() if self.active_flag else self.consider_activation()
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree*self.priority

    def consider_deactivation(self):
        self.active_flag = True
        return False
    def consider_activation(self):
        self.active_flag = True
        return True

    def calculate_match_degree(self):
        left_ir, right_ir = self.sensobs[0].get_value()
        if left_ir != right_ir:
            return 1.0
        elif left_ir and right_ir:
            return 0.25
        else:
            return 0.5

    def sense_and_act(self):
        left_ir, right_ir = self.sensobs[0].get_value()
        self.match_degree = self.calculate_match_degree()

        if left_ir and not right_ir:
            #Turn slightly to the right
            self.motor_recommendations = (DriveMode.DRIVE, -self.ROTATE_DEGREES)
            self.last_rotate_was_clockwise = False
        elif right_ir and not left_ir:
            #Turn slightly to the left
            self.motor_recommendations = (DriveMode.DRIVE, self.ROTATE_DEGREES)
            self.last_rotate_was_clockwise = True
        elif left_ir and right_ir:
            #Continue directly forward we don't know any better
            #Drive at half speed (?)
            self.motor_recommendations = (DriveMode.DRIVE, 0)
        else:
            #No walls detected. Wiggle from side to side
            rotate_direction = -1 if self.last_rotate_was_clockwise else 1
            self.motor_recommendations = (DriveMode.DRIVE, rotate_direction * self.ROTATE_DEGREES)
            self.last_rotate_was_clockwise = not self.last_rotate_was_clockwise


class FollowRedInIntersection(Behaviour):
    # Sensobs: The camera sensob looking for red and blue to determine direction
    # and the ulrasound to determine when to activate.
    LEFT = 1
    RIGHT = -1
    ROTATE_DEGREES = 90
    just_activated = False

    def update(self):

        """Activates/Deactivates the behaviour. Act on the current sensor values and updates the behaviours weight"""
        #self.consider_deactivation() if self.active_flag else self.consider_activation()
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree*self.priority
    
    def determine_direction(self):
        """Return self.LEFT or self.RIGHT based on the camera-sensob value"""
        # TODO: Implement when the format from the sensob is ready
        content = self.sensobs[0].content
        size = len(content)
        redCount = [0,0]
        for i in range(size):
            if i<=size/2:
                if content[i] == "Red":
                    redCount[0]+=1
            if i>size/2:
                if content[i] == "Red":
                    redCount[1]+=1
        if redCount[0]> redCount[1]:
            return self.LEFT
        elif redCount[0] < redCount[1]:
            return self.RIGHT
        else:
            #Same amount of red on both sides
            self.match_degree = 0.1
            return self.LEFT



    def calculate_match_degree(self):
        ultrasonic_distance = self.sensobs[1].get_value()
        return 1.0 - 0.02 * ultrasonic_distance


    def consider_deactivation(self):
        ultrasonic_distance = self.sensobs[1].get_value()
        print(ultrasonic_distance)
        if ultrasonic_distance > 10:  # Less than 10 centimeters away from the wall
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        ultrasonic_distance = self.sensobs[1].get_value()
        print(ultrasonic_distance)
        if ultrasonic_distance <= 10:    #Less than 10 centimeters away from the wall
            self.active_flag = True
            self.just_activated = True
            self.bbcon.activate_behavior(self)

    def sense_and_act(self):
        if self.just_activated:
            self.motor_recommendations = (DriveMode.HALT, 4)
            self.match_degree = 1.0
            self.just_activated = False
        else:
            self.match_degree = self.calculate_match_degree()
            direction = self.determine_direction()
            self.motor_recommendations = (DriveMode.ROTATE, direction*self.ROTATE_DEGREES)


class follow_line(Behaviour):
    # self.sensobs is 1 single sensob for for reflectance sensor
    ROTATION_WEIGHTS = [30, 20, 10, -10, -20, -30]

    def update(self):
        """Activates/Deactivates the behaviour. Act on the current sensor values and updates the behaviours weight"""
        #self.consider_deactivation() if self.active_flag else self.consider_activation()
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree*self.priority
    
    def consider_deactivation(self):
        self.active_flag = True
        return False

    def consider_activation(self):
        self.active_flag = True
        return True

    def calculate_match_degree(self):
        if any(self.sensobs[0].get_value()):
            return 1.0
        else:
            return 0.5

    def sense_and_act(self):
        reflectance_array = self.sensobs[0].get_value()
        #print(reflectance_array)
        rotations = [self.ROTATION_WEIGHTS[x] for x in range(6) if reflectance_array[x]]
        active = len(rotations)
        rotation = sum(rotations) / active if active else 0
        self.motor_recommendations = (DriveMode.DRIVE, rotation)
