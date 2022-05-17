import json
import sys
import time

import numpy as np
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QBrush, QPen, QPalette, QColor, QWindow
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QMainWindow, QWidget, \
    QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSlider, QLabel, QGridLayout, QSpinBox, QLineEdit, QLayout, \
    QFileDialog

from GridSquare2D import GridSquare2D
from GridSquare2DFlat import GridSquare2DFlat


class CellView(QGraphicsRectItem):
    def __init__(self, universe, size, x, y):
        super().__init__(0, 0, size, size)
        self.x = x
        self.y = y
        self.universe = universe

    def mousePressEvent(self, e):
        i = self.y
        j = self.x
        new_state = self.universe.changeCellStatus(i, j)
        print("x: {}, y: {}".format(self.x, self.y))
        brush = QBrush(self.universe.colors[new_state])
        self.setBrush(brush)


class UniverseView(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        self.cells = None
        self.universe = None
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.step())
        self.main_widget = main_widget

        rows = 40
        self.rows = rows
        columns = 40
        self.columns = columns
        size = 10
        self.size = size

        self.scene = QGraphicsScene(0, 0, columns * size, rows * size)

        self.universe = GridSquare2DFlat(self.columns, self.rows)
        self.initCellsView()
        self.redrawUniverse()

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setScene(self.scene)

    def initCellsView(self):
        cells = np.zeros((self.rows * self.columns), dtype=object)
        for i in range(self.rows):
            for j in range(self.columns):
                x = j
                y = i
                cell = CellView(self.universe, self.size, x, y)
                cell.setPos(x * self.size, y * self.size)
                pos = y * self.columns + x
                cells[pos] = cell
                self.scene.addItem(cell)
        self.cells = cells
        self.redrawUniverse()

    def setCellViewColor(self, x, y, color):
        pos = y * self.columns + x
        brush = QBrush(color)
        self.cells[pos].setBrush(brush)

    def redrawUniverse(self):
        for i in range(self.rows):
            for j in range(self.columns):
                x = j
                y = i
                self.setCellViewColor(x, y, self.universe.colors[self.universe.getCellStatus(i, j)])

    def step(self, n=1):
        stime = time.time()
        self.universe.next_gen(n)
        self.redrawUniverse()
        etime = time.time() - stime
        print(etime)

    def reset(self):
        self.universe.clear()
        self.redrawUniverse()

    def randomize(self):
        self.universe.set_random()
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
        self.universe = GridSquare2DFlat(self.columns, self.rows)
        self.changeSize(self.size)

    def changeColumns(self, columns):
        self.columns = columns
        self.universe = GridSquare2DFlat(self.columns, self.rows)
        self.changeSize(self.size)

    def changeSize(self, size):
        self.size = size
        self.setFixedSize(self.columns * size + 4, self.rows * size + 4)
        self.scene = QGraphicsScene(0, 0, self.columns * size, self.rows * size)
        self.initCellsView()
        self.setScene(self.scene)
        self.main_widget.centralWidget().setFixedSize(self.main_widget.centralWidget().sizeHint())
        self.main_widget.setFixedSize(self.main_widget.sizeHint())
        self.redrawUniverse()

    def toJson(self, filename):
        cells = map(lambda x: int(x), self.universe.cells)
        data = {"width": self.columns, "height": self.rows, "cells": list(cells)}
        with open(filename, "w") as write_file:
            json.dump(data, write_file)

    def fromJson(self, filename):
        with open(filename, "r") as read_file:
            data = json.load(read_file)
        self.columns = data["width"]
        self.rows = data["height"]
        cells = list(map(lambda x: bool(x), data["cells"]))
        self.universe = GridSquare2DFlat(self.columns, self.rows, cells)
        self.initCellsView()
        self.changeSize(self.size)
        self.redrawUniverse()


class ToolBar(QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setFixedWidth(150)
        layout = QVBoxLayout()

        # Rows Horizontal Layout
        lbl_rows = QLabel("Rows: ")
        self.spinbox_rows = QSpinBox()
        self.spinbox_rows.setRange(40, 200)
        self.spinbox_rows.setValue(view.rows)
        #spinbox_rows.lineEdit().setDisabled(True)
        self.spinbox_rows.valueChanged.connect(lambda x: self.changeRows(x))

        rows_layout = QHBoxLayout()
        rows_layout.addWidget(lbl_rows)
        rows_layout.addWidget(self.spinbox_rows)
        # End Rows Layout

        # Rows Horizontal Layout
        lbl_columns = QLabel("Columns: ")
        self.spinbox_columns = QSpinBox()
        self.spinbox_columns.setRange(40, 200)
        self.spinbox_columns.setValue(view.columns)
        #spinbox_columns.lineEdit().setDisabled(True)
        self.spinbox_columns.valueChanged.connect(lambda x: self.changeColumns(x))

        columns_layout = QHBoxLayout()
        columns_layout.addWidget(lbl_columns)
        columns_layout.addWidget(self.spinbox_columns)
        # End Rows Layout

        # Size Horizontal Layout
        lbl_size = QLabel("Size: ")
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(4, 20)
        spinbox_steps.setValue(view.size)
        spinbox_steps.lineEdit().setDisabled(True)
        spinbox_steps.valueChanged.connect(lambda s: view.changeSize(s))

        size_layout = QHBoxLayout()
        size_layout.addWidget(lbl_size)
        size_layout.addWidget(spinbox_steps)
        # Size Step Layout

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(lambda: self.clear())

        btn_rand = QPushButton("Randomize")
        btn_rand.clicked.connect(lambda: self.randomize())

        # Step Horizontal Layout
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(1, 1000)
        btn_step = QPushButton("Step")
        btn_step.clicked.connect(lambda: view.step(spinbox_steps.value()))

        step_layout = QHBoxLayout()
        step_layout.addWidget(btn_step)
        step_layout.addWidget(spinbox_steps)
        # End Step Layout

        # Run
        self.btn_start = QPushButton("Run")
        self.btn_start.setCheckable(True)
        self.btn_start.clicked.connect(lambda c: view.runEvo(c))

        lbl_fps = QLabel()
        lbl_ms = QLabel()

        slider_speed = QSlider(Qt.Orientation.Horizontal)
        slider_speed.setRange(2, 25)
        slider_speed.setSliderPosition(10)
        view.timer.setInterval(1000 // slider_speed.value())
        slider_speed.valueChanged.connect(lambda i: view.changeSpeed(i))
        slider_speed.valueChanged.connect(lambda i: lbl_fps.setText("FPS: " + str(i)))
        slider_speed.valueChanged.connect(lambda i: lbl_ms.setText("ms: " + str(1000 // i)))

        lbl_fps.setText("FPS: " + str(slider_speed.value()))
        lbl_ms.setText("ms: " + str(1000 // slider_speed.value()))
        # End Run

        # Open
        btn_open = QPushButton("Open")
        btn_open.clicked.connect(lambda: self.openFile())
        # End Open

        # Save
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(lambda: self.saveFile())
        # End Save

        layout.addLayout(rows_layout)
        layout.addLayout(columns_layout)
        layout.addLayout(size_layout)
        layout.addWidget(btn_clear)
        layout.addWidget(btn_rand)
        layout.addLayout(step_layout)
        layout.addWidget(lbl_fps)
        layout.addWidget(lbl_ms)
        layout.addWidget(slider_speed)
        layout.addWidget(self.btn_start)
        layout.addStretch()
        layout.addWidget(btn_open)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def changeRows(self, x):
        self.view.runEvo(False)
        self.view.changeRows(x)
        self.btn_start.setChecked(False)

    def changeColumns(self, x):
        self.view.runEvo(False)
        self.view.changeColumns(x)
        self.btn_start.setChecked(False)

    def clear(self):
        self.view.runEvo(False)
        self.view.reset()
        self.btn_start.setChecked(False)

    def randomize(self):
        self.view.runEvo(False)
        self.view.randomize()
        self.btn_start.setChecked(False)

    def openFile(self):
        filename = QFileDialog.getOpenFileName(caption="Open File", filter="*.json")[0]
        with open(filename, "r") as read_file:
            data = json.load(read_file)
        self.spinbox_columns.setValue(data["width"])
        self.spinbox_rows.setValue(data["height"])
        self.view.fromJson(filename)

    def saveFile(self):
        filename = QFileDialog.getSaveFileName(caption="Save File", filter="*.json")[0]
        self.view.toJson(filename)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("GOL")

        self.view = UniverseView(self)
        self.tools = ToolBar(self.view)

        hbox = QHBoxLayout(self)
        hbox.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        hbox.addWidget(self.tools)
        hbox.addWidget(self.view)

        widget = QWidget()
        widget.setLayout(hbox)

        # widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.setCentralWidget(widget)

        # widget.setAutoFillBackground(True)
        # palette = widget.palette()
        # palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.red)
        # widget.setPalette(palette)
        #
        # self.tools.setAutoFillBackground(True)
        # palette = widget.palette()
        # palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.green)
        # self.tools.setPalette(palette)
        #
        # self.view.setAutoFillBackground(True)
        # palette = widget.palette()
        # palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.blue)
        # self.view.setPalette(palette)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
