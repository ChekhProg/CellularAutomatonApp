import numpy as np
from PyQt6.QtCore import Qt

from ca.CellularAutomaton import CellularAutomaton


class GameOfLife(CellularAutomaton):
    def __init__(self, width, height, cells=None, rule=None):
        super().__init__(width, height, cells)
        if rule is None:
            rule = {"B": [3], "S": [2, 3]}
        self.rule = rule
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=bool)
        else:
            self.cells = np.array(cells)
        self.colors = {False: Qt.GlobalColor.black, True: Qt.GlobalColor.green}
        self.init_states = [True, False]
        self.changeable_states = [False, True]

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=bool)

    def getNeighborsMoore(self, i, j):
        pos = i * self.width + j
        live_neighbors: int = 0
        if self.cells[pos - self.width - 1]:live_neighbors += 1
        if self.cells[pos - self.width]: live_neighbors += 1
        if self.cells[pos - self.width + 1]: live_neighbors += 1
        if self.cells[pos - 1]: live_neighbors += 1
        if self.cells[pos + 1]: live_neighbors += 1
        if self.cells[pos + self.width - 1]: live_neighbors += 1
        if self.cells[pos + self.width]: live_neighbors += 1
        if self.cells[pos + self.width + 1]: live_neighbors += 1
        return live_neighbors

    def nextGen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=bool)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    neighbors = self.getNeighborsMoore(i, j)
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = False
                    if cur_status and (neighbors in self.rule["S"]):
                        new_status = True
                    else:
                        if not cur_status and (neighbors in self.rule["B"]):
                            new_status = True
                    new_cells[pos] = new_status
            self.cells = new_cells

        for k in range(n):
            gen()
