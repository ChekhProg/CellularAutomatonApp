import abc
import random

import numpy as np

from abc import *


class CellularAutomaton:
    __metaclass__ = abc.ABCMeta

    def __init__(self, width, height, cells=None):
        self.width = width + 2
        self.height = height + 2
        self.colors = None
        self.init_states = None
        self.changeable_states = None
        if cells is None:
            self.cells = np.zeros((self.height * self.width), dtype=int)
        else:
            self.cells = np.array(cells)

    def set_random(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                pos = i * self.width + j
                self.cells[pos] = random.choice(self.init_states)

    def clear(self):
        self.cells = np.zeros((self.height * self.width), dtype=int)

    @abstractmethod
    def get_neighbors_moore(self, i, j):
        pass

    @abstractmethod
    def next_gen(self, n):
        pass

    def getCellStatus(self, i, j):
        pos = (i + 1) * self.width + (j + 1)
        return self.cells[pos]

    def changeCellStatus(self, i, j, state=None):
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
