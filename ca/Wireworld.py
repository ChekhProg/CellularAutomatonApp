from abc import ABC

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ca.CellularAutomaton import CellularAutomaton
from abc import *


class Wireworld(CellularAutomaton):
    def __init__(self, width, height, cells):
        super().__init__(width, height, cells)
        self.colors = [Qt.GlobalColor.black, Qt.GlobalColor.blue, Qt.GlobalColor.red, Qt.GlobalColor.yellow]
        self.colors = [QColor.fromHsl(0, 0, 0), QColor.fromHsl(250, 255, 128), QColor.fromHsl(0, 255, 128), QColor.fromHsl(50, 255, 128)]
        self.init_states = [0, 3]
        self.changeable_states = [0, 3, 1, 2]

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
                    pos = i * self.width + j
                    cur_state = self.cells[pos]
                    new_state = 0
                    if cur_state == 3:
                        neighbors = self.get_neighbors_moore(i, j)
                        if neighbors == 1 or neighbors == 2:
                            new_state = 1
                        else:
                            new_state = 3
                    elif cur_state == 1:
                        new_state = 2
                    elif cur_state == 2:
                        new_state = 3
                    new_cells[pos] = new_state
            self.cells = new_cells

        for k in range(n):
            gen()