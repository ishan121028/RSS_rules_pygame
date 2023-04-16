import pygame
import numpy as np
import random
from car_class import car


INTERSECTION_END_X = 315
INTERSECTION_END_Y = 265

class responsiblitysafetyrules():
    def __init__(self, car1, car2, advantage_car):

        self.a_brake = car1.dec
        if(advantage_car == "car1"):
            self.advantage = car1
            self.disadvantage = car2
        else:
            self.advantage = car2
            self.disadvantage = car1
        
        self.v_a = self.advantage.vel
        self.v_d = self.disadvantage.vel
        self.acc_d = self.disadvantage.acc
        self.rho = 0.2

    def update(self):

        self.v_a = self.advantage.vel
        self.v_d = self.disadvantage.vel
        self.acc_d = self.disadvantage.acc
    
    def rule(self):

        if(self.advantage.road == "X"):
            d_a_end = INTERSECTION_END_X - self.advantage.x
            d_a_stop = (self.v_a**2)/(2*(self.a_brake))
        
        else:
            d_a_end = INTERSECTION_END_Y - self.advantage.y
            d_a_stop = (self.v_a**2)/(2*(self.a_brake))

        if d_a_end>d_a_stop:
            rho_d = self.v_d*self.rho + 0.5*self.acc_d*(self.rho**2)
            d_d_stop = rho_d + ((self.v_d + self.acc_d*self.rho)**2)/(2*self.a_brake)
            self.d_d_safe = d_d_stop + 50
        else:
            self.d_d_safe = 0 


