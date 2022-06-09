import numpy as np
from PyQt6.QtGui import QColor

from ca.GameOfLife import GameOfLife


class GameOfLifeWithAge(GameOfLife):
    def __init__(self, width, height, cells=None, rule=None):
        super().__init__(width, height, cells, rule)
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=int)
        else:
            self.cells = np.array(cells)
        cl = [QColor.fromHsl(h, 255, 128) for h in range(0, 240, 1)]
        self.colors = [QColor.fromHsl(0, 0, 0)] + cl
        self.init_states = [0, 1]
        self.changeable_states = [0, 1]

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=int)

    def nextGen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=int)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    neighbors = self.getNeighborsMoore(i, j)
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = 0
                    if (cur_status > 0) and (neighbors in self.rule["S"]):
                        new_status = cur_status + 1
                    else:
                        if cur_status == 0 and (neighbors in self.rule["B"]):
                            new_status = 1
                    if new_status > len(self.colors) - 1: new_status = len(self.colors) - 1
                    new_cells[pos] = new_status
            self.cells = new_cells

        for k in range(n):
            gen()

    def getNeighborsMoore(self, i, j):
        pos = i * self.width + j
        live_neighbors: int = 0
        if self.cells[pos - self.width - 1] > 0: live_neighbors += 1
        if self.cells[pos - self.width] > 0: live_neighbors += 1
        if self.cells[pos - self.width + 1] > 0: live_neighbors += 1
        if self.cells[pos - 1] > 0: live_neighbors += 1
        if self.cells[pos + 1] > 0: live_neighbors += 1
        if self.cells[pos + self.width - 1] > 0: live_neighbors += 1
        if self.cells[pos + self.width] > 0: live_neighbors += 1
        if self.cells[pos + self.width + 1] > 0: live_neighbors += 1
        return live_neighbors
