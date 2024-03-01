# module with class for game of life

import dask.array as da
import numpy as np


class GameOfLife:
    def __init__(
        self, rows: int = 10, columns: int = 10, prob: float = 0.5, randomize=True
    ):
        self.columns = columns
        self.rows = rows
        self.prob = prob
        self.current_state = np.zeros((rows, columns), dtype=int)
        self.previous_state = np.zeros((rows, columns), dtype=int)
        if randomize:
            self.randomize()

    def randomize(self):
        self.current_state = np.random.randint(2, size=(self.rows, self.columns))

    def neighbor_sum(self, row_index: int, column_index: int) -> int:
        """Returns the sum of the 8 neighbors of the element at row_index, column_index."""

        row_left = max(0, row_index - 1)
        row_right = min(row_index + 2, self.rows)
        col_up = max(0, column_index - 1)
        col_down = min(column_index + 2, self.columns)

        neighborhood = self.current_state[row_left:row_right, col_up:col_down]

        return np.sum(neighborhood) - self.current_state[row_index, column_index]

    def life_epoch(self) -> np.array:
        """Returns the next state of the array according to the rules of Conway's Game of Life."""
        next_state = da.zeros((self.rows, self.columns))
        for i in range(self.rows):
            for j in range(self.columns):
                neighbors = self.neighbor_sum(i, j)
                if neighbors == 3:
                    next_state[i, j] = 1
                elif self.current_state[i, j] == 1 and neighbors == 2:
                    next_state[i, j] = 1

        self.previous_state = self.current_state
        self.current_state = next_state.compute()

