"""CS 108 Final Project

This module implements helper functions.

@author: Aishwarya Joshi (aj37)
@date: Fall, 2021
"""

from random import randint
import math


def distance(x1, y1, x2, y2):
    """ Compute the distance between two points. """
    
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def maxheight_of_parabola(x, y, vel):
    """Computes the maximum height of the parabola."""
    
    angle = math.atan(y/x)
    return ((vel * math.sin(angle))**2)/2*9.81

