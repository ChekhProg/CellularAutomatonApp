import numpy as np
from PyQt6.QtCore import Qt

from ca.CellularAutomaton import CellularAutomaton


class BriansBrain(CellularAutomaton):
    def __init__(self, width, height, cells=None):
        super().__init__(width, height, cells)
        self.colors = [Qt.GlobalColor.black, Qt.GlobalColor.white, Qt.GlobalColor.red]
        self.init_states = [0, 1]
        self.changeable_states = [0, 1, 2]

    def get_neighbors_moore(self, i, j):
        pos = i * self.width + j
        live_neighbors: int = 0
        if self.cells[pos - self.width - 1] == 1: live_neighbors += 1
        if self.cells[pos - self.width] == 1: live_neighbors += 1
        if self.cells[pos - self.width + 1] == 1: live_neighbors += 1
        if self.cells[pos - 1] == 1: live_neighbors += 1
        if self.cells[pos + 1] == 1: live_neighbors += 1
        if self.cells[pos + self.width - 1] == 1: live_neighbors += 1
        if self.cells[pos + self.width] == 1: live_neighbors += 1
        if self.cells[pos + self.width + 1] == 1: live_neighbors += 1
        return live_neighbors

    def next_gen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=int)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    neighbors = self.get_neighbors_moore(i, j)
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = 0
                    if (cur_status == 0) and (neighbors == 2):
                        new_status = 1
                    else:
                        if cur_status == 1:
                            new_status = 2
                    new_cells[pos] = new_status
            self.cells = new_cells

        for k in range(n):
            gen()