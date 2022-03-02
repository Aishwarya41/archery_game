"""CS 108 Final Project

This module tests some of the basic functionality of the archer model.

@author: Aishwarya Joshi (aj37)
@date: Fall, 2021
"""

from archery import Player, Arrow, Line, Board


arrow1 = Arrow(600, 200, vel_x = 20, vel_y = 16)

#The values should be initialized properly.
assert arrow1.initial_x == arrow1.x1
assert arrow1.initial_y == arrow1.y1
assert arrow1.max_height == 125.56800000000001

#The velocities and max_height should change according to the arguments provided.
arrow1.adjust_velocity(100, 200, 300)
assert arrow1.vel_x == 10
assert arrow1.vel_y == 20
assert arrow1.max_height == 196.20000000000005


#The angle should be calculated, except for the exceptional case of x1 = x2 (for which, angle == 0).
line1 = Line((500,200), (500,300))
assert line1.angle == 0
line2 = Line((500,200), (300,300))
assert line2.angle == -0.46364760900080615