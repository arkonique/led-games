import numpy as np
import time
import sys
import pygame
from games.pong import Pong
from games.snake import Snake

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 400, 800  # Adjust size as needed
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('LED display simulator')

# Colors
black = (0, 0, 0) # background
grey = (128, 128, 128) # 0
green = (0, 255, 0) # 1
red = (255, 0, 0) # 2
blue = (0, 0, 255) # 3
white = (255, 255, 255) # 4

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

def pygame_single_iteration(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(black)

    for row in range(grid_height):
        for col in range(grid_width):
            x = col * (circle_radius * 2 + margin) + circle_radius + margin + x_offset
            y = row * (circle_radius * 2 + margin) + circle_radius + margin + y_offset
            if grid[row, col] == 1:
                color = green
            elif grid[row, col] == 2:
                color = red
            elif grid[row, col] == 3:
                color = blue
            elif grid[row, col] == 4:
                color = white
            else:
                color = grey
            draw_circle(screen, color, (x, y), circle_radius)


# Initialize the GRID array
GRID = np.zeros((20, 10), dtype=int)
pygame_single_iteration(GRID)
pygame.display.flip()

if __name__ == "__main__":
    time.sleep(1)

    if sys.argv[1] == "pong":
        pong = Pong()
        win = pong.check_score() != 0
        while not win:    
            GRID = pong.game_loop()
            pygame_single_iteration(GRID)
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

    elif sys.argv[1] == "snake":
        snake = Snake()
        while not snake.game_over:
            GRID = snake.game_loop()
            pygame_single_iteration(GRID)
            # Display the score at the bottom of the screen
            font = pygame.font.Font(None, 36)
            if snake.game_over:
                text = font.render(f"Game Over! Score: {snake.score}", True, red)
            else:
                text = font.render(f"Score: {snake.score}", True, red)

            text_rect = text.get_rect(center=(width // 2, height - 30))
            screen.blit(text, text_rect)
            time.sleep(0.15)
            pygame.display.flip()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()