"""CS 108 Final Project

This module implements model of a Player, Arrow, Board and Line.

@author: Aishwarya Joshi (aj37)
@date: Fall, 2021
"""

from helpers import distance, maxheight_of_parabola
import math


class Player:
    """Player models a player object and its methods."""

    def __init__(self, x, y):
        """Instantiates a Player object with the given x and y coordinates. """
        self.x = x 
        self.y = y    
        
    def draw_player(self, drawing):
        """Draws a stickman figure on the drawing canvas."""
        
        #Head and Body
        drawing.oval(self.x, self.y, self.x + 20, self.y + 20,
                         color='black')
        drawing.line(self.x +10, self.y +20, self.x +10, self.y +50, width = 3)
        
        #Shadow
        drawing.oval(self.x - 5, self.y + 66, self.x + 25, self.y + 75, color = '#819DCB')
         
        #Legs
        drawing.line(self.x +10, self.y + 50, self.x, self.y + 70, width = 3)
        drawing.line(self.x +10, self.y + 50, self.x +20, self.y + 70, width = 3)
        
        # Hand
        
        drawing.line(self.x +10, self.y + 30, self.x + 20, self.y + 45, width = 3)
        drawing.line(self.x +10, self.y + 30, self.x, self.y + 25, width = 3)
        
        
        
class Arrow:
    """Arrow models an arrow object and its methods."""
    
    def __init__(self, x, y, vel_x = 20, vel_y = 16):
        """Instantiates an arrow object with the given x and y coordinates, and velocity x and velocity y. """
        
        self.initial_x = x
        self.initial_y = y
        self.x1 = x
        self.y1 = y
        self.vel_x = vel_x
        self.vel_y = vel_y


        self.max_height = maxheight_of_parabola(self.x1, self.y1, self.vel_y)
        
    
        
    def draw_arrow(self, drawing, x1, y1):
        """Draws an arrow on the drawing canvas."""
        
        distance_of_arrow = distance(self.initial_x, self.initial_y, x1, y1)
        
        if distance_of_arrow < 1.5 * self.max_height:
        
            drawing.line(x1 - 20, y1 + 6, x1 + 15, y1 - 6, width = 2, color = "brown")
            drawing.triangle(x1 + 13, y1 - 9, x1 + 17, y1 - 3, x1 + 20, y1 -8 , color = "white", outline=True)
            
            
        elif distance_of_arrow < 2 * self.max_height:
            
            drawing.line(x1 - 17, y1 + 3, x1 + 15, y1 - 3, width = 2, color = "brown")
            drawing.triangle(x1 + 14, y1 - 8, x1 + 16, y1 +1, x1 + 19, y1 -4 , color = "white", outline=True)
            
        else:
            drawing.line(x1 - 17, y1, x1 + 17, y1, width = 2, color = "brown")
            drawing.triangle(x1 + 17, y1 + 4, x1 + 17, y1 -4 , x1 + 22, y1, color = "white", outline=True)
        
        
        
    def move_arrow(self, drawing):
        """Changes the x and y coordinates of the arrow according to the velocity and max_height."""
        
        self.x1 += self.vel_x
        
        if distance(self.initial_x, self.initial_y, self.x1, self.y1) < 1.5 * self.max_height:
            self.y1 += self.vel_y
        elif distance(self.initial_x, self.initial_y, self.x1, self.y1) > 2 * self.max_height:
            self.vel_y -= 1
                 
        self.draw_arrow(drawing, self.x1, self.y1)
        
    def adjust_velocity(self,length, y1, y2):
        """Changes the velocity according to the length and angle of the line drawn by the player."""
        
        self.vel_x = length/10
        self.vel_y = -(y1 - y2) / 5
        self.max_height = maxheight_of_parabola(self.x1, self.y1, self.vel_y)
        
class Line:
    """Line models a line object and its methods."""
    
    def __init__(self, start, end):
        """Instantiates a Line object with the start and end position of the line drawn by the player."""
        
        self.start = start
        self.end = end
        self.length = distance(self.start[0], self.start[1], self.end[0], self.end[1])
        
        if self.end[0] != self.start[0]:
            self.angle = math.atan((self.end[1] - self.start[1])/ (self.end[0] - self.start[0]))
        else:
            self.angle = 0
            
        self.ref = None

        
    def draw(self, drawing):
        """Draws a line on the drawing canvas."""
        
        self.ref = drawing.line(self.start[0], self.start[1], self.end[0], self.end[1])
    
    
    def remove(self,drawing):
        """Deletes the line."""
        
        drawing.delete(self.ref)
        
        
class Board:
    """Board models a board object and its methods."""
    
    def __init__(self, board_x, board_y):
        """Instantiates a Board object with the given x and y coordinates."""
        
        self.board_x = board_x
        self.board_y = board_y
        
    def draw_board(self, drawing):
        """Draws a board on the drawing canvas."""
        
        self.white = drawing.oval(self.board_x, self.board_y, self.board_x+ 40, self.board_y + 80, color = 'white', outline=True)
        self.blue = drawing.oval(self.board_x + 3, self.board_y + 8, self.board_x+ 33, self.board_y + 72, color = 'blue')
        self.red = drawing.oval(self.board_x + 7, self.board_y + 18, self.board_x+ 27, self.board_y + 62, color = 'red')
        self.yellow = drawing.oval(self.board_x + 11, self.board_y + 30, self.board_x+ 21, self.board_y + 50, color = 'yellow')
        drawing.oval(self.board_x + 13, 330, self.board_x + 33, 340, color = '#819DCB')

