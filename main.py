import numpy as np
import time
from pynput import keyboard
from pynput.keyboard import Key
import sys

GRID = np.zeros((20, 10), dtype=int)
dir = "stay"
player = 0

print(GRID)
# Pong

class Pong:
    def __init__(self, ball=(9,4), p1_pad=3, p2_pad=3, speed=(1,1), p1_score=0, p2_score=0):
        self.ball = ball
        self.p1_pad = p1_pad
        self.p2_pad = p2_pad
        self.speed = speed
        self.p1_score = p1_score
        self.p2_score = p2_score
    
    def draw_grid(self):
        grid = np.zeros((20, 10), dtype=int)
        # grid in format a[y coordinate,x coordinate]
        grid[self.ball] = 2
        grid[19,self.p1_pad:self.p1_pad+4] = 1
        grid[0,self.p2_pad:self.p2_pad+4] = 1
        return grid
    
    def move_ball(self):
        ball = self.ball
        speed = self.speed
        ball = (ball[0]+speed[0], ball[1]+speed[1])
        self.ball = ball

        if ball[0] == 0 or ball[0] == 19:
            speed = (speed[0]*-1, speed[1])
            self.speed = speed

        if ball[1] == 0 or ball[1] == 9:
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
            print("Player 1")
            print(direction)
            if direction == "left":
                self.p1_pad -= 1
            elif direction == "right":
                self.p1_pad += 1
        elif player == 2:
            print("Player 2")
            print(direction)
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
    
def on_key_release(key):
    global dir, player
    if key == Key.left:
        dir = "left"
        player = 1
    elif key == Key.right:
        dir = "right"
        player = 1
    elif key == 'A':
        dir = "left"
        player = 2
        print("a")
    elif key == 'd':
        dir = "right"
        player = 2
    elif key == Key.esc:
        sys.exit(0)
    else:
        dir = "stay"
        player = 0
    return False

pong = Pong()

while True:
    
    pong.move_ball()

    # get arrow key input
    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()
    pong.move_paddle(player, dir)
    GRID = pong.draw_grid()
    print(GRID)
    print("-----------------")
