import numpy as np
import keyboard

class Snake:
    def __init__(self,grid = np.zeros((20,10),dtype=int),snake=[(9,4)], direction="left", food=(2,2), score=0, game_over=0):
        self.grid = grid
        self.snake = snake
        self.direction = direction
        self.food = food
        self.score = score
        self.game_over = game_over

    def draw_grid(self):
        grid = np.zeros((20, 10), dtype=int)
        # grid in format a[y coordinate,x coordinate]
        for i in self.snake:
            grid[i] = 1
        grid[self.food] = 2
        self.grid = grid
        return grid
    
    def food_spawn(self):
        x = np.random.randint(0,9)
        y = np.random.randint(0,19)
        self.food = (y,x)

    def move_snake(self):
        snake = self.snake
        direction = self.direction
        head = snake[0]
        flag = 0
        if len(snake) == 1:
            second = head
        else:
            second = snake[1]
        if direction == "left":
            new_head = (head[0],head[1]-1)
        elif direction == "right":
            new_head = (head[0],head[1]+1)
        elif direction == "up":
            new_head = (head[0]-1,head[1])
        elif direction == "down":
            new_head = (head[0]+1,head[1])
        if new_head in snake or new_head[0] < 0 or new_head[0] > 19 or new_head[1] < 0 or new_head[1] > 9:
            self.game_over = 1
        else:
            snake.insert(0,new_head)
            if new_head == self.food:
                self.score += 1
                self.food_spawn()
            else:
                snake.pop()
        self.snake = snake
        return snake
    
    def game_loop(self):
        if keyboard.is_pressed('up'):
            self.direction = "up"
        elif keyboard.is_pressed('down'):
            self.direction = "down"
        elif keyboard.is_pressed('left'):
            self.direction = "left"
        elif keyboard.is_pressed('right'):
            self.direction = "right"
        self.move_snake()

        return self.draw_grid()