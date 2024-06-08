import numpy as np
import keyboard
import time

# Generate a random list of integers that sum to n between.
def randomSum(n):
    num_bricks = np.random.randint(2,8)
    arr = [2]*num_bricks
    while sum(arr) < n:
        x = np.random.randint(0,n) % num_bricks
        if arr[x] < 5:
            arr[x] += 1
    return arr

def unique_consecutive_random_numbers(n, a, b):
    if n > 1 and (b - a) == 0:
        raise ValueError("Range is too narrow to generate unique consecutive numbers")
    
    arr = [np.random.randint(a, b+1)]
    while len(arr) < n:
        next_num = np.random.randint(a, b+1)
        while next_num == arr[-1]:
            next_num = np.random.randint(a, b+1)
        arr.append(next_num)
    return arr

class Breakout:
    def __init__ (self, grid = np.zeros((20,10),dtype=int), ball = (18,4), paddle = 3, bricks = [], score = 0, level = 1, lives = 10,game_over = False,speed = (1,1)):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.score = score
        self.level = level
        self.lives = lives
        self.grid = grid
        self.game_over = game_over
        self.speed = speed
        self.generate_bricks()

    def draw_grid(self):
        grid = np.zeros((20,10),dtype=int)
        grid[self.ball] = 4
        grid[19,self.paddle:self.paddle+3] = 4
        grid[0,9-self.lives+1:10] = 4
        for brick in self.bricks:           
            grid[brick[0],brick[1]:brick[1]+brick[2]] = brick[3]
        self.grid = grid
        return grid
    
    def generate_bricks(self):
        bricks = []
        for row in range(2,2+self.level):
            bricks_in_row = randomSum(10)
            colors = unique_consecutive_random_numbers(len(bricks_in_row),1,3)
            for i in range(0,len(bricks_in_row)):
                y_coord = row
                x_coord = sum(bricks_in_row[:i])
                brick = (y_coord,x_coord,bricks_in_row[i],colors[i])
                bricks.append(brick)

        self.bricks = bricks
        return bricks
    
    def move_paddle(self, direction):
        if direction == "left" and self.paddle > 0:
            self.paddle -= 1
        if direction == "right" and self.paddle < 7:
            self.paddle += 1

    def ball_hit_brick(self):
        ball = self.ball
        for brick in self.bricks:
            if ball[0] == brick[0]+1 and ball[1] in range(brick[1],brick[1]+brick[2]):
                self.bricks.remove(brick)
                self.score += self.scoring(brick)
                return True
        return False

    def move_ball(self):
        # ball speed depends on level
        speed = self.speed
        ball = self.ball
        ball = (ball[0]-speed[0], ball[1]+speed[1])
        # check if ball hits wall at 0,18 and 0,9
        if ball[0] <= 1:
            speed = (speed[0]*-1, speed[1])
            ball = (1,ball[1])
        if ball[1] < 0 or ball[1] > 9:
            speed = (speed[0], speed[1]*-1)
            ball = (ball[0],1) if ball[1] <= 0 else (ball[0],8)

        # check if ball hits paddle
        if ball[0] == 18 and ball[1] in range(self.paddle-1,self.paddle+4):
            speed = (speed[0]*-1, speed[1])
            pos = np.random.randint(0,3)
            ball = (18,self.paddle+pos)

        # check if ball hits brick
        if self.ball_hit_brick():
            speed = (speed[0]*-1, speed[1]*-1)
            ball = (ball[0],ball[1])

        # check if ball hits bottom wall
        if ball[0] > 19:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            # choose a random position on the paddle to start the ball
            pos = np.random.randint(0,3)
            ball = (18,self.paddle+pos)
            speed = (1,1)
            time.sleep(1)

        self.ball = ball
        self.speed = speed
        return ball, speed
    
    def scoring(self,brick):
        return int(10/brick[2])
    
    def advance_level(self):
        if self.grid[2:11,0:10].sum() == 0 and self.grid.sum() != 0:
            self.level += 1
            self.generate_bricks()
            self.speed = (1,1)
            self.paddle = 3
            self.ball = (18,4)
            return True

    def game_loop(self):
        self.move_ball()
        if keyboard.is_pressed('left'):
            dir = "left"
        elif keyboard.is_pressed('right'):
            dir = "right"
        elif keyboard.is_pressed('a'):
            dir = "left"
        elif keyboard.is_pressed('d'):
            dir = "right"
        elif not keyboard.is_pressed('left') and not keyboard.is_pressed('right') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
            dir = "stay"

        self.move_paddle(dir)
        self.advance_level()
        return self.draw_grid()

