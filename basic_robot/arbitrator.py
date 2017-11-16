from behaviour import *
from random import random

class Arbitrator:
    def __init__(self, bbcon):
        self.bbcon = bbcon

    def choose_action(self):
        """Choose behaviour based on their weights"""
        #TODO: Add stochasticity (weighted randomness)
        chosen = max(self.bbcon.active_behaviors)
        return (chosen.motor_recommendations, chosen.halt_request)

    def choose_action_stochastically(self):
        w = [b.weight for b in self.bbcon.active_behaviors]
        part_sums = w[0:1]
        for i in range(1,len(w)):
            part_sums += [w[i] + part_sums[i-1]]
        total = sum(w);
        choice = random()*total
        for i in range(len(part_sums)):
            if choice <= part_sums[i]:
                return [self.bbcon.active_behaviors[i].motor_recommendations, self.bbcon.active_behaviors[i].halt_request]


