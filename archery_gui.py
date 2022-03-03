"""
This module implements the GUI of the Archery game.
"""

from guizero import App, Drawing, Box, PushButton, Text, Picture, Window
from archery import Player, Arrow, Line, Board
from time import sleep
import random

class PlayerGUI:
    """This class builds an interactive game GUI."""

    def __init__(self, app):
        """Instantiates the GUI app."""
        
        #App
        app.title = 'Archery'
        DRAWING_UNIT = 400
        CONTROL_UNIT = 70
        app.width = DRAWING_UNIT * 2
        app.height = DRAWING_UNIT + CONTROL_UNIT
        
        #Control Panel
        control_panel = Box(app, layout='grid', width = DRAWING_UNIT * 2 , height = CONTROL_UNIT)    
        
        #Widgets on Control Panel
        
        #Time Box
        time_box = Box(control_panel, layout='grid', grid = [0,0], width = 200 , height = 30)
        PushButton(time_box, grid = [0,0, 1, 2], text = 'Start', command = self.start, width= 5, height = 4, padx = 0, pady = 0)
        self.pause_button = PushButton(time_box, grid = [1,0], width = 22, height = 22, pady = 0, padx = 0, image = 'PauseButton.png', command = self.pause)
        self.resume_button = PushButton(time_box, grid = [2,0], width = 22, height = 22, pady = 0, padx = 0, image = 'ResumeButton.png', command = self.resume)
        Text(time_box, grid = [1,1,2,1], text= 'Time:', size = 16, align = 'left')
        self.total_time = 60
        self.time_val = Text(time_box, grid = [3,1,3,1], text= str(self.total_time), size = 16)
        
        #Title Box
        title_box = Box(control_panel, layout='grid', grid = [1,0], width = 800 , height = 70)
        empty = Text(title_box, text = '             ', grid = [0,0], size = 45)
        logo = Picture(title_box, grid = [1,0], image = 'Board.png', width = 60, height = 60)
        title = Text(title_box, text = 'Archery               ', grid = [2,0], size = 45 , font = 'Smart Watch')
        
        #Menu Box
        menu_box = Box(control_panel, layout='grid', grid = [2,0], width = 150 , height = 70)
        leader_board = PushButton(menu_box, grid = [0,0], width = 10, height = 1, text = 'Leaderboard', command = self.get_leaderboard, padx =0, pady = 2)
        new_button = PushButton(menu_box, grid = [1,0], width = 22, height = 22, pady = 0, padx = 0, image = "Refresh.png", command = self.refresh)
        quit_button = PushButton(menu_box, grid = [2,0], width = 22, height = 22, pady = 0, padx = 0, image = "Quit.png", command = self.quit_game)
        best = Text(menu_box, grid = [0, 1, 3, 1], text = 'Best:', size = 14)
        self.best_text = Text(menu_box, grid = [1,1], text= '0', size = 14)
        score_board = Text(menu_box, grid = [0, 2, 4, 1], text = 'Score:', size = 16)
        self.score_text = Text(menu_box, grid = [1,2, 2,1], text= '0 ', size = 16)
        
        #Drawing canvas
        canvas = Box(app, layout = 'grid', width=DRAWING_UNIT*2, height=DRAWING_UNIT)
        self.drawing = Drawing(canvas,  grid = [0,0], width=DRAWING_UNIT*2, height=DRAWING_UNIT)
        self.drawing.bg = "#AED4FF"
        
        #Events
        self.drawing.when_left_button_pressed = self.process_mouse_press
        self.drawing.when_mouse_dragged = self.process_mouse_motion
        self.drawing.when_left_button_released = self.process_mouse_release
        self.best_score = 0
        
        self.new_game()
        
        
    def new_game(self):
        """Creates a new game and initializes all attributes."""
        
        newgame = app.yesno("New Game", "Do you want to start a new game?")
        
        if newgame:
            self.total_time = 60
            self.time_val.value = '60'
            
            #Initializes Player, Arrow, Line and Board
            self.player = Player(x=100, y=270)
            self.player_arrow = Arrow(self.player.x - 20, self.player.y + 10)
            self.board = Board(board_x= 500, board_y = 100)
            self.temporary_line = Line((0,0), (1,1))
            
            #Initializes variables
            self.arrow_flying = False
            self.saved_position = None
            self.score = 0
            self.hit = False
            self.resume_button.enabled = False
            
            #Gets best score
            self.get_best()
            
            #Prompts the user to enter player name
            self.playername = app.question("Welcome", "Enter player name.")
            
        
    def start(self):
        """Starts the timer and calls draw_frame."""
        
        app.repeat(1000, self.timer)
        self.paused = False
        
        self.draw_frame()
    
    
    
    def add_arrow(self):
        """Initializes a new arrow."""
        
        self.player_arrow = Arrow(self.player.x - 20, self.player.y + 10)
        
        
    def shoot(self):
        """Adjusts the velocity and starts the arrow shooting animation."""
        
        self.player_arrow.adjust_velocity(self.temporary_line.length, self.temporary_line.end[1], self.temporary_line.start[1])
        self.arrow_flying = True
        app.repeat(20, self.draw_frame)
        
        

    def draw_frame(self):
        """Draws the frame after determining the position of the arrow."""
        
        
        if not self.paused:
            
            self.drawing.clear()
            self.player.draw_player(self.drawing)
            
            self.board.draw_board(self.drawing)
            self.player_arrow.move_arrow(self.drawing)
            self.add_score()
            
            self.check_boundary()
            self.check_time_end()


        
    def check_boundary(self):
        """Checks if the arrow is out of the app screen."""
        
        if (self.player_arrow.x1 <= 0) or (self.player_arrow.x1 >= self.drawing.width) or (self.player_arrow.y1 <= 0) or (self.player_arrow.y1 >= self.drawing.height):
            
            #Create new Arrow and Board instances.
            self.player_arrow = Arrow(self.player.x - 20, self.player.y + 10)
            self.board = Board(board_x= random.randint(400,700), board_y = random.randint(50, 230))
            
            app.cancel(self.draw_frame)
            self.arrow_flying = False
            self.draw_frame()
            
    
    def check_hit(self):
        """Checks if the arrow hits the board and returns the color it hit."""
        
        self.centre_x = self.board.board_x + 15
        self.centre_y = self.board.board_y + 40
        
        if (self.player_arrow.y1 < self.centre_y + 40 and self.player_arrow.y1 > self.centre_y - 40) and self.player_arrow.x1 + 18 >= self.centre_x:
            
            app.cancel(self.draw_frame)
            self.hit = True
            self.arrow_flying = False

                
            if (self.player_arrow.y1 < self.centre_y + 10 and self.player_arrow.y1 > self.centre_y - 10):
                return 'yellow'
            elif (self.player_arrow.y1 < self.centre_y + 22 and self.player_arrow.y1 > self.centre_y - 22):
                return 'red'
            elif (self.player_arrow.y1 < self.centre_y + 32 and self.player_arrow.y1 > self.centre_y - 32):
                return 'blue'
            elif (self.player_arrow.y1 < self.centre_y + 40 and self.player_arrow.y1 > self.centre_y - 40):
                return 'white'
            
        else:
            return None
            
            
    def add_score(self):
        """Checks which color was hit by the arrow and updates the score accordingly. It initializes a new arrow and board if it was hit."""
        
        if self.check_hit() == 'yellow':
            self.score += 10
        elif self.check_hit() == 'red':
            self.score += 5
        elif self.check_hit() == 'blue':
            self.score += 3
        elif self.check_hit() == 'white':
            self.score += 1
        
        self.score_text.value = str(self.score)
        
        if self.hit == True:
            
            app.cancel(self.draw_frame)
            sleep(1)
            self.player_arrow = Arrow(self.player.x - 20, self.player.y + 10)
            self.board = Board(board_x= random.randint(400,700), board_y = random.randint(50, 230))
            self.hit = False
            self.draw_frame()
        
                
    def process_mouse_press(self, event):
        """Starts a new line where the user presses the mouse."""
        
        if not self.arrow_flying and not self.paused:
        
            self.saved_position = (event.x, event.y)
        
        
    def process_mouse_motion(self, event):
        """Displays a temporary version of the line and removes the previous version."""
        
        if not self.arrow_flying and not self.paused:
            self.temporary_line.remove(self.drawing)
            self.temporary_line = Line(self.saved_position, (event.x, event.y))
            self.temporary_line.draw(self.drawing)
            

    def process_mouse_release(self):
        """Calls the shoot() method when the arrow is released."""
        
        if not self.arrow_flying and not self.paused:
            self.shoot()
    
    
    def pause(self):
        """ Stops the arrow animation temporarily. """
        
        self.paused = True
        self.pause_button.enabled = False
        self.resume_button.enabled = True


    def resume(self):
        """Resumes the arrow animation."""
        
        self.paused = False
        self.pause_button.enabled = True
        self.resume_button.enabled = False
        
        
    def timer(self):
        """Decreases the time by 1 and changes the value displayed."""
        
        if self.total_time > 0 and not self.paused:
            self.total_time -= 1
            self.time_val.value = str(self.total_time)
            
            
    def check_time_end(self):
        """Checks if the time runs out and provides comments accordingly."""
        
        if self.total_time == 0:
            self.paused = True
            self.drawing.clear()
            app.info("Game Over", "Time's up! Your score was {}.".format(self.score))
            
            if self.score > self.best_score:
                app.info("New Best", "Congratulations! You reached a new highscore.")
            
            app.cancel(self.timer)
            self.save_leaderboard()
            self.new_game()

    
    
    def quit_game(self):
        """Stops and quits the app."""
        quit_game = app.yesno("Exit Game", "Do you want to quit?")
        
        if quit_game:
            app.destroy()
    
      
        
    def refresh(self):
        """Discards the current game and creates a new game."""
        
        app.cancel(self.timer)
        self.new_game()
            
        
    def get_best(self):
        """Reads from the file to get the best score and display it. """
        
        scores = open("scores_list.txt",'r')
        score_data = scores.readlines()
        self.score_list = []
        line_number = 1
        
        for line in score_data:

            values = line.strip().split(',')
            self.score_list.append([int(values[0]), values[1]])
            
            if line_number == 1:
                self.best_score = int(self.score_list[0][0])
                self.best_text.value = str(self.score_list[0][0])
                
            line_number += 1
        
        scores.close()
        
        
    def save_leaderboard(self):
        """Updates the scores in the score_list and writes it in the file."""
        
        scores = open("scores_list.txt",'w')
        self.score_list.append([int(self.score), str(self.playername)])
        self.score_list.sort(reverse= True)

        for val in self.score_list:
            scores.write(str(val[0]) + ',' + str(val[1]) + '\n')
        scores.close()
        
        
    def get_leaderboard(self):
        """Displays the Leaderboard window by reading from the file."""
        
        self.pause()

        Text(leaderboard, text ='Leaderboard', grid = [0,0], size = 30, font = 'CHAMBRUSH')
        score_board = Box(leaderboard, grid = [0,1], layout='grid' )
        Text(score_board, grid = [0,0], text = 'Player Name', size = 15)
        Text(score_board, grid = [1,0], text = 'Score', size = 15)
        
        # Read from file to display the leader board.
        scores = open("scores_list.txt",'r')
        score_data = scores.readlines()
        i = 1
        for line in score_data:
            values = line.strip().split(',')
            
            if i <= 5:
                values = line.strip().split(',')
                Text(score_board, grid = [0,i], text = str(values[1]))
                Text(score_board, grid = [1,i], text = str(values[0]))
            i += 1
        scores.close()
        leaderboard.show()
        
        
app = App()
PlayerGUI(app)
leaderboard = Window(app, title="Leader Board", layout = 'grid', width = 200, height = 200)
leaderboard.hide()
app.display()
