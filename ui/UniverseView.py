import json
import time

import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QSizePolicy

from ca.BriansBrain import BriansBrain
from ca.GameOfLife import GameOfLife
from ca.GameOfLifeWithAge import GameOfLifeWithAge
from ca.VonNeumann import VonNeumann
from ca.Wireworld import Wireworld
from ui.CellView import CellView


class UniverseView(QGraphicsView):
    def __init__(self, main_widget, type):
        super().__init__()
        self.universe_prev_cells = None
        self.drawer_state = None
        self.cells = None
        self.universe = None
        self.type = type
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.step())
        self.main_widget = main_widget
        self.rule = {"B": [3], "S": [2, 3]}

        rows = 80
        self.rows = rows
        columns = 80
        self.columns = columns
        size = 8
        self.size = size

        self.scene = QGraphicsScene(0, 0, columns * size, rows * size)

        self.initUniverse()
        self.initCellsView()
        self.redrawUniverse()

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setScene(self.scene)

    def initUniverse(self, cells=None):
        if self.type == "GameOfLife":
            self.universe = GameOfLife(self.columns, self.rows, cells=cells, rule=self.rule)
        elif self.type == "GameOfLifeWithAge":
            self.universe = GameOfLifeWithAge(self.columns, self.rows, cells=cells, rule=self.rule)
        elif self.type == "BriansBrain":
            self.universe = BriansBrain(self.columns, self.rows, cells=cells)
        elif self.type == "Wireworld":
            self.universe = Wireworld(self.columns, self.rows, cells=cells)
        elif self.type == "VonNeumann":
            self.universe = VonNeumann(self.columns, self.rows, cells=cells)
        self.universe_prev_cells = None

    def initCellsView(self):
        self.scene.clear()
        cells = np.zeros((self.rows * self.columns), dtype=object)
        for i in range(self.rows):
            for j in range(self.columns):
                x = j
                y = i
                cell = CellView(self, self.universe, self.size, x, y)
                cell.setPos(x * self.size, y * self.size)
                pos = y * self.columns + x
                cells[pos] = cell
                self.scene.addItem(cell)
        self.cells = cells
        self.universe_prev_cells = None
        self.redrawUniverse()

    def setCellViewColor(self, i, j, color):
        pos = i * self.columns + j
        self.cells[pos].setBrush(color)

    def redrawUniverse(self):
        if self.universe_prev_cells is None:
            for i in range(self.rows):
                for j in range(self.columns):
                    state = self.universe.getCellState(i, j)
                    color = self.universe.colors[state]
                    self.setCellViewColor(i, j, color)
        else:
            b = self.universe.cells.reshape((self.rows + 2, self.columns + 2))
            b = b[1:self.rows + 1, 1:self.columns + 1]
            a = self.universe_prev_cells.reshape((self.rows+2, self.columns+2))
            a = a[1:self.rows+1, 1:self.columns+1]
            diff_ind = np.argwhere(a != b)
            for k in diff_ind:
                i = k[0]
                j = k[1]
                state = self.universe.getCellState(i, j)
                color = self.universe.colors[state]
                self.setCellViewColor(i, j, color)
        self.universe_prev_cells = np.copy(self.universe.cells)

    def step(self, n=1, btn=None):
        self.universe_prev_cells = np.copy(self.universe.cells)
        stime = time.time()
        self.universe.nextGen(n)
        etime_calc = time.time() - stime
        self.redrawUniverse()
        if not btn is None:
            btn.setChecked(False)
        etime = time.time() - stime
        print("Gen: {}, Draw: {} All: {}".format(etime_calc, etime-etime_calc, etime))

    def reset(self):
        self.universe.clear()
        self.redrawUniverse()

    def randomize(self):
        self.universe.setRandom()
        self.redrawUniverse()

    def runEvo(self, check):
        if check:
            self.timer.start()
        else:
            self.timer.stop()

    def changeSpeed(self, i: float):
        self.timer.setInterval(1000 // int(i))

    def changeRows(self, rows):
        self.rows = rows
        self.initUniverse()
        self.changeSize(self.size)

    def changeColumns(self, columns):
        self.columns = columns
        self.initUniverse()
        self.changeSize(self.size)

    def changeSize(self, size):
        self.size = size
        self.setFixedSize(self.columns * size + 4, self.rows * size + 4)
        self.scene = QGraphicsScene(0, 0, self.columns * size, self.rows * size)
        self.initCellsView()
        self.setScene(self.scene)
        self.main_widget.setFixedSize(self.main_widget.sizeHint())
        self.redrawUniverse()

    def toJson(self, filename):
        cells = list(map(lambda x: int(x), self.universe.cells))
        data = {"width": self.columns, "height": self.rows, "cells": cells}
        with open(filename, "w") as write_file:
            json.dump(data, write_file)

    def fromJson(self, filename):
        with open(filename, "r") as read_file:
            data = json.load(read_file)
        self.columns = data["width"]
        self.rows = data["height"]
        if self.type == "GameOfLife":
            cells = list(map(lambda x: bool(x), data["cells"]))
        else:
            cells = list(map(lambda x: int(x), data["cells"]))
        self.initUniverse(cells=cells)
        self.changeSize(self.size)
        self.initCellsView()
        self.redrawUniverse()
