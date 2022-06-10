import numpy as np
from PyQt6.QtGui import QColor

from ca.CellularAutomaton import CellularAutomaton


class VonNeumann(CellularAutomaton):
    def __init__(self, width, height, cells):
        super().__init__(width, height, cells)
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=int)
        else:
            self.cells = np.array(cells)
        self.colors_def = {"U": QColor(48, 48, 48),
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
                           "OT_N_Q": QColor(106, 106, 255),  # 13
                           "OT_S_Q": QColor(139, 139, 255),
                           "OT_W_Q": QColor(122, 122, 255),
                           "OT_E_Q": QColor(89, 89, 255),
                           "OT_N_E": QColor(36, 200, 36),  # 17
                           "OT_S_E": QColor(106, 255, 106),
                           "OT_W_E": QColor(73, 255, 73),
                           "OT_E_E": QColor(27, 176, 27),
                           "ST_N_Q": QColor(255, 56, 56),
                           "ST_S_Q": QColor(255, 89, 89),
                           "ST_W_Q": QColor(255, 73, 73),
                           "ST_E_Q": QColor(235, 36, 36),
                           "ST_N_E": QColor(191, 73, 255),
                           "ST_S_E": QColor(203, 106, 255),
                           "ST_W_E": QColor(197, 89, 255),
                           "ST_E_E": QColor(185, 56, 255)}
        self.list_states = ["U", "S", "S_0", "S_00", "S_000",
                            "S_01", "S_1", "S_10", "S_11",
                            "C_00", "C_01", "C_10", "C_11",
                            "OT_N_Q", "OT_S_Q", "OT_W_Q", "OT_E_Q",
                            "OT_N_E", "OT_S_E", "OT_W_E", "OT_E_E",
                            "ST_N_Q", "ST_S_Q", "ST_W_Q", "ST_E_Q",
                            "ST_N_E", "ST_S_E", "ST_W_E", "ST_E_E"]
        self.changeable_states = [i for i in range(29)]
        self.colors = [self.colors_def[i] for i in self.list_states]

    def getNeighborsMoore(self, i, j):
        pass

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=int)

    def getNeighborsVonNeumannOr(self, i, j, dir):
        pos = i * self.width + j
        live_ord_neighbors = False
        if dir != "W" and self.cells[pos - 1] == 20: live_ord_neighbors = True
        if dir != "E" and self.cells[pos + 1] == 19: live_ord_neighbors = True
        if dir != "S" and self.cells[pos + self.width] == 17: live_ord_neighbors = True
        if dir != "N" and self.cells[pos - self.width] == 18: live_ord_neighbors = True

        live_spec_neighbors = False
        if dir != "W" and self.cells[pos - 1] == 28: live_spec_neighbors = True
        if dir != "E" and self.cells[pos + 1] == 27: live_spec_neighbors = True
        if dir != "S" and self.cells[pos + self.width] == 25: live_spec_neighbors = True
        if dir != "N" and self.cells[pos - self.width] == 26: live_spec_neighbors = True

        return live_ord_neighbors, live_spec_neighbors

    def getNeighborsVonNeumannAnd(self, i, j, dir):
        pos = i * self.width + j
        ord_quiescent_neighbors = 0
        ord_excited_neighbors = 0
        if dir != "W" and self.cells[pos - 1] == 20: ord_excited_neighbors += 1
        elif dir != "W" and self.cells[pos - 1] == 16: ord_quiescent_neighbors += 1
        if dir != "E" and self.cells[pos + 1] == 19: ord_excited_neighbors += 1
        elif dir != "E" and self.cells[pos + 1] == 15: ord_quiescent_neighbors += 1
        if dir != "S" and self.cells[pos + self.width] == 17: ord_excited_neighbors += 1
        elif dir != "S" and self.cells[pos + self.width] == 13: ord_quiescent_neighbors += 1
        if dir != "N" and self.cells[pos - self.width] == 18: ord_excited_neighbors += 1
        elif dir != "N" and self.cells[pos - self.width] == 14: ord_quiescent_neighbors += 1

        flag = False
        if ord_quiescent_neighbors == 0 and ord_excited_neighbors > 0:
            flag = True
        return flag

    def getLiveConfluents(self, i, j, dir):
        pos = i * self.width + j
        live_confluent_neighbors = 0
        if dir != "W" and self.cells[pos - 1] == 11:
            live_confluent_neighbors += 1
        if dir != "E" and self.cells[pos + 1] == 11:
            live_confluent_neighbors += 1
        if dir != "S" and self.cells[pos + self.width] == 11:
            live_confluent_neighbors += 1
        if dir != "N" and self.cells[pos - self.width] == 11:
            live_confluent_neighbors += 1

    def nextGen(self, n=1):
        def gen():
            new_cells = np.zeros((self.height * self.width), dtype=int)
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    pos = i * self.width + j
                    cur_state = self.cells[pos]
                    new_state = cur_state

                    # Ordinary Transmissions
                    if cur_state == 13 or cur_state == 17:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "N")
                        if live_spec_neighbors:
                            new_state = 0
                        elif live_ord_neighbors:
                            new_state = 17
                        else:
                            new_state = 13
                    if cur_state == 14 or cur_state == 18:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "S")
                        if live_spec_neighbors:
                            new_state = 0
                        elif live_ord_neighbors:
                            new_state = 18
                        else:
                            new_state = 14
                    if cur_state == 15 or cur_state == 19:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "W")
                        if live_spec_neighbors:
                            new_state = 0
                        elif live_ord_neighbors:
                            new_state = 19
                        else:
                            new_state = 15
                    if cur_state == 16 or cur_state == 20:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "E")
                        if live_spec_neighbors:
                            new_state = 0
                        elif live_ord_neighbors:
                            new_state = 20
                        else:
                            new_state = 16

                    # Special Transmission
                    if cur_state == 21 or cur_state == 25:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "N")
                        if live_ord_neighbors:
                            new_state = 0
                        elif live_spec_neighbors:
                            new_state = 25
                        else:
                            new_state = 21
                    if cur_state == 22 or cur_state == 26:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "S")
                        if live_ord_neighbors:
                            new_state = 0
                        elif live_spec_neighbors:
                            new_state = 26
                        else:
                            new_state = 22
                    if cur_state == 23 or cur_state == 27:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "W")
                        if live_ord_neighbors:
                            new_state = 0
                        elif live_spec_neighbors:
                            new_state = 27
                        else:
                            new_state = 23
                    if cur_state == 24 or cur_state == 28:
                        live_ord_neighbors, live_spec_neighbors = self.getNeighborsVonNeumannOr(i, j, "E")
                        if live_ord_neighbors:
                            new_state = 0
                        elif live_spec_neighbors:
                            new_state = 28
                        else:
                            new_state = 24

                    # Confluent States
                    if cur_state == 9:
                        live_ord_neighbors = self.getNeighborsVonNeumannAnd(i, j, "None")
                        if live_ord_neighbors: new_state = 12
                        else: new_state = 9
                    if cur_state == 12:
                        live_ord_neighbors = self.getNeighborsVonNeumannAnd(i, j, "None")
                        if live_ord_neighbors: new_state = 10
                        else: new_state = 11
                    if cur_state == 11:
                        live_ord_neighbors = self.getNeighborsVonNeumannAnd(i, j, "None")
                        if live_ord_neighbors: new_state = 12
                        else: new_state = 9
                    if cur_state == 10:
                        live_ord_neighbors = self.getNeighborsVonNeumannAnd(i, j, "None")
                        if live_ord_neighbors: new_state = 12
                        else: new_state = 12

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
        else:
            new_state = state
        self.cells[pos] = new_state
        return new_state
