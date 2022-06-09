import numpy as np
from PyQt6.QtGui import QColor

from ca.CellularAutomaton import CellularAutomaton


class VonNeumann(CellularAutomaton):
    def __init__(self, width, height, cells):
        super().__init__(width, height, cells)
        if cells is None:
            self.cells = np.full((self.height * self.width), "U", dtype=object)
        else:
            self.cells = np.array(cells)
        self.colors = {"U": QColor(48, 48, 48),
                       "S": QColor(255, 0, 0),
                       "S_0": QColor(255, 125, 0),
                       "S_00": QColor(255, 175, 50),
                       "S_000": QColor(251, 255, 0),
                       "S_01": QColor(255, 200, 75),
                       "S_1": QColor(255, 150, 25),
                       "S_10": QColor(255, 255, 100),
                       "S_11": QColor(255, 250, 125),
                       "C_00": QColor(0, 255, 128),
                       "C_01": QColor(33, 215, 215),
                       "C_10": QColor(255, 255, 128),
                       "C_11": QColor(255, 128, 64),
                       "OT_N_E": QColor(36, 200, 36),
                       "OT_N_Q": QColor(106, 106, 255),
                       "OT_S_E": QColor(106, 255, 106),
                       "OT_S_Q": QColor(139, 139, 255),
                       "OT_W_E": QColor(73, 255, 73),
                       "OT_W_Q": QColor(122, 122, 255),
                       "OT_E_E": QColor(27, 176, 27),
                       "OT_E_Q": QColor(89, 89, 255),
                       "ST_N_E": QColor(191, 73, 255),
                       "ST_N_Q": QColor(255, 56, 56),
                       "ST_S_E": QColor(203, 106, 255),
                       "ST_S_Q": QColor(255, 89, 89),
                       "ST_W_E": QColor(197, 89, 255),
                       "ST_W_Q": QColor(255, 73, 73),
                       "ST_E_E": QColor(185, 56, 255),
                       "ST_E_Q": QColor(235, 36, 36)}
        # self.colors = [QColor.fromHsl(0, 0, 0), QColor.fromHsl(250, 255, 128), QColor.fromHsl(0, 255, 128), QColor.fromHsl(50, 255, 128)]
        self.changeable_states = ["U", "S", "S_0", "S_00", "S_000", "S_01", "S_1", "S_10", "S_11", "C_00", "C_01",
                                  "C_10", "C_11", "OT_N_E", "OT_N_Q", "OT_S_E", "OT_S_Q", "OT_W_E", "OT_W_Q",
                                  "OT_E_E", "OT_E_Q", "ST_N_E", "ST_N_Q", "ST_S_E", "ST_S_Q", "ST_W_E", "ST_W_Q",
                                  "ST_E_E", "ST_E_Q"]

    def getNeighborsMoore(self, i, j):
        pass

    def clear(self):
        self.cells = np.full((self.height * self.width), "U", dtype=object)

    def getNeighborsVonNeumann(self, i, j):
        pos = i * self.width + j
        live_neighbors: int = 0
        if self.cells[pos - self.width] == 1: live_neighbors += 1
        if self.cells[pos - 1] == 1: live_neighbors += 1
        if self.cells[pos + 1] == 1: live_neighbors += 1
        if self.cells[pos + self.width] == 1: live_neighbors += 1
        return live_neighbors

    def nextGen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=int)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    pos = i * self.width + j
                    cur_state = self.cells[pos]
                    new_state = 0
                    if cur_state == 3:
                        neighbors = self.getNeighborsMoore(i, j)
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

    def changeCellState(self, i, j, state=None):
        pos = (i + 1) * self.width + (j + 1)
        if state is None:
            cur_state = self.cells[pos]
            new_state_ind = self.changeable_states.index(cur_state) + 1
            if new_state_ind == len(self.changeable_states):
                new_state = self.changeable_states[0]
            else:
                new_state = self.changeable_states[new_state_ind]
        elif state == 0:
            new_state = "U"
        self.cells[pos] = new_state
        return new_state