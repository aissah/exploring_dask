# module with class for game of life

import dask as da
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    def __init__(self, rows:int=10, columns:int=10, prob: float=0.5, randomize=True):
        self.columns = columns 
        self.rows = rows
        self.prob = prob
        self.current_state = np.zeros((rows, columns), dtype=int)
        if randomize:
            self.randomize()
        self.fig, self.ax = plt.subplots()
        self.im = plt.imshow(self.current_state, cmap='gray', interpolation='nearest')
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=100, interval=50, blit=True)
        plt.show()

    def randomize(self):
        self.current_state = np.random.randint(2, size=(self.rows, self.rows))

    def update(self, frame):
        # new_current_state = np.zeros((self.rows, self.columns), dtype=int)
        # for i in range(self.rows):
        #     for j in range(self.columns):
        #         new_current_state[i, j] = self.update_cell(i, j)
        # self.current_state = new_current_state
        self.life_epoch()
        self.im.set_array(self.current_state)
        return self.im,

    # def update_cell(self, i, j):
    #     count = 0
    #     for x in range(-1, 2):
    #         for y in range(-1, 2):
    #             if x == 0 and y == 0:
    #                 continue
    #             if self.current_state[(i + x) % self.size, (j + y) % self.size] == 1:
    #                 count += 1
    #     if self.current_state[i, j] == 1:
    #         if count < 2 or count > 3:
    #             return 0
    #         else:
    #             return 1
    #     else:
    #         if count == 3:
    #             return 1
    #         else:
    #             return 0
    
    def neighbor_sum(self, row_index: int, column_index: int) -> int:
        '''Returns the sum of the 8 neighbors of the element at row_index, column_index.
        '''

        row_left = max(0,row_index-1)
        row_right = min(row_index+2, self.rows)
        col_up = max(0,column_index-1)
        col_down = min(column_index+2, self.columns)
        
        neighborhood = self.current_state[row_left:row_right, col_up:col_down]

        return np.sum(neighborhood) - self.current_state[row_index, column_index]

    def life_epoch(self) -> np.array:
        '''Returns the next state of the array according to the rules of Conway's Game of Life.
        '''
        next_state = da.zeros((self.rows, self.columns))
        for i in range(self.rows):
            for j in range(self):
                neighbors = self.neighbor_sum(self.current_state, i, j)
                if neighbors == 3:
                    next_state[i,j] = 1
                elif self.current_state[i,j] == 1 and neighbors == 2:
                    next_state[i,j] = 1

        self.current_state = next_state

    def initiate_life(self) -> np.array:
        '''Returns a random 2D array of size row_size x column_size with prob probability of 1s.
        '''
        return np.random.choice([0, 1], size=(self.rows, self.rows), p=[1-self.prob, self.prob])