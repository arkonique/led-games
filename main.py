import numpy as np
import time
import sys
import pygame
from games.pong import Pong


# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 400, 800  # Adjust size as needed
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('LED display simulator')

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
green = (0, 255, 0)

# Circle parameters
circle_radius = 15
margin = 5
grid_width, grid_height = 10, 20

# Calculate grid size
grid_total_width = grid_width * (circle_radius * 2 + margin) - margin
grid_total_height = grid_height * (circle_radius * 2 + margin) - margin

# Calculate offsets to center the grid
x_offset = (width - grid_total_width) // 2
y_offset = (height - grid_total_height) // 2

def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)

# Initialize the GRID array
GRID = np.zeros((20, 10), dtype=int)

if __name__ == "__main__":
    if sys.argv[1] == "pong":
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
                    if GRID[row, col] == 1:
                        color = green
                    elif GRID[row, col] == 2:
                        color = red
                    else:
                        color = grey
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