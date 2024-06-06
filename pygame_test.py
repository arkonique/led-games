import numpy as np
import time
import sys
import pygame

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
            else:
                color = grey
            draw_circle(screen, color, (x, y), circle_radius)

    pygame.display.flip()  # Update the display

# Initialize the GRID array with some values for testing
GRID = np.zeros((20, 10), dtype=int)
GRID[10, 5] = 1  # Example green circle
GRID[15, 3] = 2  # Example red circle

clock = pygame.time.Clock()  # Initialize a clock to control the frame rate

while True:
    pygame_single_iteration(GRID)
    #clock.tick(30)  # Run the loop at 30 frames per second
