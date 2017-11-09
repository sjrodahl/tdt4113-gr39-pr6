from behaviour import *

class Arbitrator:
    def __init__(self, bbcon):
        self.bbcon = bbcon

    def choose_action(self):
        """Choose behaviour based on their weights"""
        #TODO: Add stochasticity (weighted randomness)
        chosen = max(self.bbcon.active_behaviors)
        return (chosen.motor_recommendations, chosen.halt_request)