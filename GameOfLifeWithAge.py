import random

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from GameOfLife import GameOfLife


class GameOfLifeWithAge(GameOfLife):
    def __init__(self, width, height, cells=None, rule=None):
        super().__init__(width, height, cells, rule)
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=int)
        else:
            self.cells = np.array(cells)
        #self.colors = {0: Qt.GlobalColor.black, 1: QColor.fromHsv(120, 255, 230), 2: QColor.fromHsv(120, 255, 200), 3: QColor.fromHsv(120, 255, 120)}
        self.colors = {0: Qt.GlobalColor.black, 1: Qt.GlobalColor.yellow, 2: Qt.GlobalColor.darkYellow,
                       3: Qt.GlobalColor.darkRed}
        # self.colors = {0: Qt.GlobalColor.black, 1: Qt.GlobalColor.red, 2: Qt.GlobalColor.darkRed,
        #                3: Qt.GlobalColor.darkYellow}

    def set_random(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                pos = i * self.width + j
                self.cells[pos] = random.choice([0, 1])

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=int)

    def next_gen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=int)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    neighbors = self.get_neighbors_moore(i, j)
                    pos = i * self.width + j
                    cur_status = self.cells[pos]
                    new_status = 0
                    if (cur_status > 0) and (neighbors in self.rule["S"]):
                        new_status = cur_status + 1
                    else:
                        if cur_status == 0 and (neighbors in self.rule["B"]):
                            new_status = 1
                    if new_status > 3: new_status = 3
                    new_cells[pos] = new_status
            self.cells = new_cells

        for k in range(n):
            gen()

    def get_neighbors_moore(self, i, j):
        pos = i * self.width + j
        live_neighbors: int = 0
        if self.cells[pos - self.width - 1] > 0 : live_neighbors += 1
        if self.cells[pos - self.width] > 0: live_neighbors += 1
        if self.cells[pos - self.width + 1] > 0 : live_neighbors += 1
        if self.cells[pos - 1] > 0: live_neighbors += 1
        if self.cells[pos + 1] > 0: live_neighbors += 1
        if self.cells[pos + self.width - 1] > 0: live_neighbors += 1
        if self.cells[pos + self.width] > 0: live_neighbors += 1
        if self.cells[pos + self.width + 1] > 0: live_neighbors += 1
        return live_neighbors

    def changeCellStatus(self, i, j):
        pos = (i + 1) * self.width + (j + 1)
        new_state = 1
        if self.cells[pos] == 1:
            new_state = 0
        self.cells[pos] = new_state
        return new_state