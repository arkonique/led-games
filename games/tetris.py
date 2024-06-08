import numpy as np

class Tetris:
    def __init__(self, grid=np.zeros((20, 10), dtype=int), piece=None, piece_pos=(0, 3), score=0, game_over=False):
        self.grid = grid
        self.piece = piece
        self.piece_pos = piece_pos
        self.score = score
        self.game_over = game_over

    def draw_grid(self):
        grid = np.zeros((20, 10), dtype=int)
        if self.piece is not None:
            for row in range(4):
                for col in range(4):
                    if self.piece[row, col] == 1:
                        grid[self.piece_pos[0] + row, self.piece_pos[1] + col] = 1
        self.grid = grid
        return grid

    def move_piece(self, direction):
        piece_pos = self.piece_pos
        if direction == 'down':
            piece_pos = (piece_pos[0] + 1, piece_pos[1])
        elif direction == 'left':
            piece_pos = (piece_pos[0], piece_pos[1] - 1)
        elif direction == 'right':
            piece_pos = (piece_pos[0], piece_pos[1] + 1)
        self.piece_pos = piece_pos

    def rotate_piece(self):
        piece = self.piece
        piece = np.rot90(piece)
        self.piece = piece

    def check_collision(self):
        piece = self.piece
        piece_pos = self.piece_pos
        for row in range(4):
            for col in range(4):
                if piece[row, col] == 1:
                    if piece_pos[0] + row >= 20 or piece_pos[1] + col < 0 or piece_pos[1] + col >= 10 or self.grid[piece_pos[0] + row, piece_pos[1] + col] == 1:
                        return True
        return False

    def clear_rows(self):
        grid = self.grid
        rows_to_clear = []
        for row in range(20):
            if np.all(grid[row, :] == 1):
                rows_to_clear.append(row)
        for row in rows_to_clear:
            grid[row, :] = 0
            grid[1:row + 1, :] = grid[:row, :]
        self.grid = grid
        self.score += len(rows_to_clear)

    def game_loop(self):
        if self.piece is None:
            self.piece = np.random.choice([np.array([[1, 1, 1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1, 1], [0, 1, 0]])])
            self.piece_pos = (0, 3)
            if self.check_collision():
                self.game_over = True
        else:
            self.move_piece('down')
            if self.check_collision():
                self.move_piece('up')
                self.grid = self.draw_grid()
                self.clear_rows()
                self.piece = None
        return self.grid
    
    