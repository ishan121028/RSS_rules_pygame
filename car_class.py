import random
import time
import numpy as np
import pygame

class car:
    def __init__(self, road, x, y):
        self.start = time.time()
        self.road = road
        self.x = x
        self.y = y
        self.vel = 20*random.random()
        self.acc = 5*random.random()
        self.dec = -10
        # self.waypoints = np.linspace(0,600, 1000, axis=1)

    def coordinate_update(self, dt, B = False):
        if B:
            a = self.dec
        else:
            a = self.acc
            # print(self.vel)
        if(self.vel>0):
            self.end = time.time()
            self.t = self.end - self.start
            if(self.road == "X"):
                self.vel += a*dt
                self.x += self.vel*dt + 0.5*a*(dt**2)
            if(self.road == "Y"):
                self.vel += a*dt
                self.y += self.vel*dt + 0.5*a*(dt**2)
        

    







                
            



        
