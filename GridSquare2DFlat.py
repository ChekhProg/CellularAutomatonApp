import json
import random
import time

import numpy as np
from PyQt6.QtCore import Qt

from GridSquare2D import GridSquare2D


class GridSquare2DFlat:
    def __init__(self, width, height, cells=None):
        self.width = width + 2
        self.height = height + 2
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=bool)
        else:
            self.cells = np.array(cells)
        self.colors = {False: Qt.GlobalColor.black, True: Qt.GlobalColor.darkGreen}

    def set_random(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                pos = i * self.width + j
                self.cells[pos] = random.choice([True, False])

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=bool)

    def get_neighbors_moore(self, i, j):
        pos = i * self.width + j
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
            new_cells = np.zeros((self.height * self.width), dtype=bool)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    neighbors = self.get_neighbors_moore(i, j)
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = False
                    if cur_status and (neighbors == 3 or neighbors == 2):
                        new_status = True
                    else:
                        if neighbors == 3 and not cur_status:
                            new_status = True
                    new_cells[pos] = new_status
            self.cells = new_cells

        for k in range(n):
            gen()

    def getCellStatus(self, i, j):
        pos = (i + 1) * self.width + (j + 1)
        return self.cells[pos]

    def changeCellStatus(self, i, j):
        pos = (i + 1) * self.width + (j + 1)
        new_state = True
        if self.cells[pos]:
            new_state = False
        self.cells[pos] = new_state
        return new_state
