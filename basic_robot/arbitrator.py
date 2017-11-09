from behaviour import *

class Arbitrator:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def choose_action(self):
        """Choose behaviour based on their weights"""
        #TODO: Add stochasticity (weighted randomness)
        chosen = max(self.behaviors)
        return (chosen.motor_recommendations, chosen.halt_request)