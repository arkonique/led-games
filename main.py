import numpy as np
import time
import keyboard
import sys
import pygame


# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 400, 800  # Adjust size as needed
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('10x20 Grid of Circles')

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)

# Circle parameters
circle_radius = 15
margin = 5
grid_width, grid_height = 10, 20

# Create the GRID array
GRID = np.zeros((20, 10), dtype=int)

# pong variables
dir = "stay"
player = 0

# Pong

class Pong:
    def __init__(self, ball=(9,4), p1_pad=3, p2_pad=3, speed=(1,1), p1_score=0, p2_score=0,winner = 0,win_score = 11):
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
        grid[self.ball] = 1
        grid[18,self.p1_pad:self.p1_pad+4] = 1
        grid[1,self.p2_pad:self.p2_pad+4] = 1
        return grid
    
    def move_ball(self):
        ball = self.ball
        speed = self.speed
        ball = (ball[0]+speed[0], ball[1]+speed[1])
        self.ball = ball

        if ball[0] == 0 or ball[0] == 19:
            if ball[0] == 0:
                self.p1_score += 1
            else:
                self.p2_score += 1
            speed = (speed[0]*-1, speed[1])
            self.speed = speed
            ball = (9,4)
            self.ball = ball
            

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
        if self.ball[1] < 4:
            if self.ball[0] > 10:
                self.move_paddle(2, "right")
            elif self.ball[0] < 10:
                self.move_paddle(2, "left")
        return self.p2_pad
    
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

## Pygame definitions

# Calculate grid size
grid_total_width = grid_width * (circle_radius * 2 + margin) - margin
grid_total_height = grid_height * (circle_radius * 2 + margin) - margin

# Calculate offsets to center the grid
x_offset = (width - grid_total_width) // 2
y_offset = (height - grid_total_height) // 2

def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)



pong = Pong()
win = pong.check_score() != 0

while not win:    
    
    GRID = pong.game_loop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    for row in range(grid_height):
        for col in range(grid_width):
            x = col * (circle_radius * 2 + margin) + circle_radius + margin + x_offset
            y = row * (circle_radius * 2 + margin) + circle_radius + margin + y_offset
            color = red if GRID[row][col] == 1 else grey
            draw_circle(screen, color, (x, y), circle_radius)

    # Display the numbers at the bottom of the screen
    font = pygame.font.Font(None, 36)

    if pong.check_score():
        winner_text = font.render(f"Player {pong.check_winner()} wins!", True, red)
        winner_rect = winner_text.get_rect(center=(width // 2, height - 30))
        screen.blit(winner_text, winner_rect)
    else:
        text = font.render(f"{pong.p1_score}:{pong.p2_score}", True, red)
        text_rect = text.get_rect(center=(width // 2, height - 30))
        screen.blit(text, text_rect)

    pygame.display.flip()

    time.sleep(0.1)
    win = pong.check_score() != 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()