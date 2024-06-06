import numpy as np
import keyboard
import time

class Pong:
    def __init__(self, grid= np.zeros((20, 10), dtype=int),ball=(9,4), p1_pad=3, p2_pad=3, speed=(1,1), p1_score=0, p2_score=0,winner = 0,win_score = 11):
        self.grid = grid
        self.ball = ball
        self.p1_pad = p1_pad
        self.p2_pad = p2_pad
        self.speed = speed
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.winner = winner
        self.win_score = win_score
    
    def draw_grid(self):
        grid = np.zeros((20, 10), dtype=int)
        # grid in format a[y coordinate,x coordinate]
        grid[self.ball] = 2
        grid[18,self.p1_pad:self.p1_pad+4] = 1
        grid[1,self.p2_pad:self.p2_pad+4] = 1

        self.grid = grid
        return grid
    
    def move_ball(self):
        ball = self.ball
        speed = self.speed
        ball = (ball[0]+speed[0], ball[1]+speed[1])
        self.ball = ball

        if ball[0] <= 0 or ball[0] >= 19:
            if ball[0] == 0:
                self.p1_score += 1
                time.sleep(0.5)
            else:
                self.p2_score += 1
                time.sleep(0.5)
            speed = (speed[0]*-1, speed[1])
            self.speed = speed
            ball = (9,4)
            self.ball = ball
            

        if ball[1] <= 0 or ball[1] >= 9:
            speed = (speed[0], speed[1]*-1)
            self.speed = speed

        # Check if ball is on paddle
        if ball[0] == 18 and ball[1] in range(self.p1_pad, self.p1_pad+4):
            speed = (speed[0]*-1, speed[1])
            self.speed = speed

        if ball[0] == 1 and ball[1] in range(self.p2_pad, self.p2_pad+4):
            speed = (speed[0]*-1, speed[1])
            self.speed = speed

        return ball
    
    def move_paddle(self, player, direction):
        if player == 1:
            if direction == "left":
                self.p1_pad -= 1
            elif direction == "right":
                self.p1_pad += 1
        elif player == 2:
            if direction == "left":
                self.p2_pad -= 1
            elif direction == "right":
                self.p2_pad += 1

        if self.p1_pad < 0:
            self.p1_pad = 0
        elif self.p1_pad > 6:
            self.p1_pad = 6

        if self.p2_pad < 0:
            self.p2_pad = 0
        elif self.p2_pad > 6:
            self.p2_pad = 6
    
        return self.p1_pad, self.p2_pad
    
    def check_score(self):
        if self.p1_score == self.win_score:
            self.winner = 1
            return 1
        elif self.p2_score == self.win_score:
            self.winner = 2
            return 2
        else:
            return 0
        
    def check_winner(self):
        return self.winner
    
    def reset(self):
        self.ball = (9,4)
        self.p1_pad = 3
        self.p2_pad = 3
        self.speed = (1,1)
        self.p1_score = 0
        self.p2_score = 0
        self.winner = 0
        return self.ball, self.p1_pad, self.p2_pad, self.speed, self.p1_score, self.p2_score, self.winner
    
    def ai_move(self):
        # if ball is in top half try to match the ball's x coordinate with a 40% chance of moving in the opposite direction. If in the bottom half, don't move
        if self.ball[0] < 10:
            if np.random.randint(1,10) < 9:
                if self.ball[1] < self.p2_pad:
                    self.move_paddle(2, "left")
                elif self.ball[1] > self.p2_pad:
                    self.move_paddle(2, "right")
            else:
                if self.ball[1] < self.p2_pad:
                    self.move_paddle(2, "right")
                elif self.ball[1] > self.p2_pad:
                    self.move_paddle(2, "left")

    def game_loop(self):
        self.move_ball()
        if keyboard.is_pressed('left'):
            dir = "left"
            player = 1
        elif keyboard.is_pressed('right'):
            dir = "right"
            player = 1
        elif keyboard.is_pressed('a'):
            dir = "left"
            player = 2
        elif keyboard.is_pressed('d'):
            dir = "right"
            player = 2
        elif not keyboard.is_pressed('left') and not keyboard.is_pressed('right') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
            dir = "stay"
            player = 0
        self.move_paddle(player, dir)
        self.ai_move()
        return self.draw_grid()

