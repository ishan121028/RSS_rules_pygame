import pygame
import random
import time
from car_class import car
import numpy as np
import math
from responsiblity_safety_rules import responsiblitysafetyrules

INTERSECTION_END_X = 315
INTERSECTION_END_Y = 265
INTERSECTION_START_X = 315-80
INTERSECTION_START_Y = 265-80
(CAR1X, CAR1Y) = (10, 225)
(CAR2X, CAR2Y) = (275, 10)

car1 = car("X", CAR1X, CAR1Y)
car2 = car("Y", CAR2X, CAR2Y)

CAR1_DISTANCE = 265
CAR2_DISTANCE = 215

WIDTH, HEIGHT = (600, 500)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Car Simulator')
CAR_IMAGE = pygame.image.load('car_image.jpg')
SCALED_CAR = pygame.transform.scale(CAR_IMAGE, (50,50))
CAR1 = pygame.transform.rotate(SCALED_CAR, -90)
CAR2 = pygame.transform.rotate(SCALED_CAR, 180)

INTERSECTION_IMAGE = pygame.image.load('road.png')
INTERSECTION = pygame.transform.scale(INTERSECTION_IMAGE, (600,600))
WHITE = (255, 255, 255)
FPS = 60

def findAdvantage(car1, car2):

    time1 = (math.sqrt(car1.vel**2 + 2*car1.acc*CAR1_DISTANCE) - car1.vel)/car1.acc
    time2 = (math.sqrt(car2.vel**2 + 2*car2.acc*CAR2_DISTANCE) - car2.vel)/car2.acc
    
    if time1<time2:
        return "car1"
    else:
        return "car2"
    
def main():
    rect1 = pygame.Rect(CAR1X, CAR1Y, 60, 50)
    rect2 = pygame.Rect(CAR2X, CAR2Y, 60, 50)
    TARGET_FPS = 60

    clock = pygame.time.Clock()
    run = True
    advantage_car = findAdvantage(car1, car2)
    print("Car with advantage", advantage_car)

    RSS = responsiblitysafetyrules(car1, car2, advantage_car)

    brake = False
    i = -1
    while run:
        if rect1.colliderect(rect2):
            print("Collision Occured")
        dt = clock.tick(FPS)*(.001)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_b]:
            brake = True
            i = 0
            isSafe(RSS, advantage_car, car1, car2)
            
        # i is used to count the number of times the loop is run, if after brake the loop is run
        # more than 12 times (which roughly results in 0.2 sec) the disadvantaged car starts applying brakes,
        # This models the time delay in communication between the cars.

        if i>=0: i+=1  
        coordinate_update(dt, brake, advantage_car, car1, car2, i)

        rect1.x = car1.x
        rect2.y = car2.y
        draw_window(rect1, rect2)
    pygame.quit()

def coordinate_update(dt, brake, advantage_car, car1, car2, i):

    # Updates the coordinates of the both cars with the help of the coordinate_upfdate function in 
    # the car class.

    if  advantage_car == "car1":
        car1.coordinate_update(dt, brake)
        if(i>12):
            car2.coordinate_update(dt, True)
        else:
            car2.coordinate_update(dt, False)
    if advantage_car == "car2":
        car2.coordinate_update(dt, brake)
        if i>12:
            car1.coordinate_update(dt, True)
        else:
            car1.coordinate_update(dt, False)

def draw_window(car1, car2):
    WIN.fill(WHITE)
    WIN.blit(INTERSECTION,(0,-50))
    WIN.blit(CAR1, (car1.x,car1.y))
    WIN.blit(CAR2, (car2.x,car2.y))
    pygame.display.update()

def isSafe(RSS, advantage_car, car1, car2):
    RSS.update()
    RSS.rule()
    print("The safe distance is", RSS.d_d_safe)
    if advantage_car == "car1":
        print("Car 2 distance", car2.y)
        print("The distance of disadvantaged car from intersection: ",INTERSECTION_START_Y - car2.y)

        if(RSS.d_d_safe>INTERSECTION_START_Y - car2.y):
            print("Car might collide")
        else:
            print("We are good to go!")
    else:
        print("Car 1 distance", car1.x)
        print("The distance of disadvantaged car from intersection: ",INTERSECTION_START_X - car1.x)
        if(RSS.d_d_safe>INTERSECTION_START_X - car1.x):
            print("Car might collide")
        else:
            print("We are good to go!")

if __name__ == "__main__":
    main()


