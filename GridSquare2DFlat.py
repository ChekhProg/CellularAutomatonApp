import random
import time

import numpy as np

from GridSquare2D import GridSquare2D


class GridSquare2DFlat(GridSquare2D):
    def __init__(self, width, height):
        width = width + 1
        height = height + 1
        super().__init__(width, height)
        self.cells = np.zeros((height * width), dtype=bool)

    def set_random(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                pos = i * self.width + j
                self.cells[pos] = random.choice([True, False])

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=bool)

    def get_neighbors_moore(self, x, y):
        pos = x * self.width + y
        live_neighbors: int = 0
        if self.cells[pos - self.width - 1]: live_neighbors += 1
        if self.cells[pos - self.width]: live_neighbors += 1
        if self.cells[pos - self.width + 1]: live_neighbors += 1
        if self.cells[pos - 1]: live_neighbors += 1
        if self.cells[pos + 1]: live_neighbors += 1
        if self.cells[pos + self.width - 1]: live_neighbors += 1
        if self.cells[pos + self.width]: live_neighbors += 1
        if self.cells[pos + self.width + 1]: live_neighbors += 1
        return live_neighbors

    def next_gen(self, n=1):
        def gen():
            #neighbors_time = 0.0
            #other_time = 0.0
            new_cells = np.zeros((self.height * self.width), dtype=bool)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    #stime = time.time()
                    neighbors = self.get_neighbors_moore(i, j)
                    #neighbors_time += time.time() - stime
                    #stime = time.time()
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = False
                    if cur_status and (neighbors == 3 or neighbors == 2):
                        new_status = True
                    else:
                        if neighbors == 3 and not cur_status:
                            new_status = True
                    new_cells[pos] = new_status
                    #other_time += time.time() - stime

            self.cells = new_cells
            # print("Neighbors:", neighbors_time)
            # print("Other:    ", other_time)
            # print("Total:    ", neighbors_time+other_time)

        for i in range(n):
            gen()

    def getCellStatus(self, x, y):
        pos = (x + 1) * self.width + (y + 1)
        return self.cells[pos]
