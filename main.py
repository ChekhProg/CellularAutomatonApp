import sys
import time

import numpy as np
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QBrush, QPen, QPalette, QColor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QMainWindow, QWidget, \
    QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSlider, QLabel, QGridLayout

from GridSquare2D import GridSquare2D
from GridSquare2DFlat import GridSquare2DFlat


class CellView(QGraphicsRectItem):
    def __init__(self, universe, size, x, y):
        super().__init__(0, 0, size, size)
        self.x = x
        self.y = y
        self.universe = universe

    def mousePressEvent(self, e):
        new_state = self.universe.changeCellStatus(self.x, self.y)
        print(new_state)
        brush = QBrush(self.universe.colors[new_state])
        self.setBrush(brush)


class UniverseView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.step())

        rows = 50
        self.rows = rows
        columns = 50
        self.columns = columns
        size = 10
        self.size = size

        self.scene = QGraphicsScene(0, 0, columns * size, rows * size)

        # test
        self.universe = GridSquare2DFlat(self.rows, self.columns)
        cells = np.zeros((self.rows * self.columns), dtype=object)
        for i in range(self.rows):
            for j in range(self.columns):
                cell = CellView(self.universe, self.size, i, j)
                cell.setPos(i * self.size, j * self.size)
                pos = i * self.columns + j
                cells[pos] = cell
                self.scene.addItem(cell)
        self.cells = cells
        self.redrawUniverse()
        # test

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setScene(self.scene)

    # def drawGrid(self):
    #     print("!")
    #     rows = self.rows
    #     columns = self.columns
    #     size = self.size
    #     for x in range(rows):
    #         self.scene.addLine(0, x * size, columns * size, x * size, QPen(Qt.GlobalColor.black))
    #
    #     for y in range(columns):
    #         self.scene.addLine(y * size, 0, y * size, rows * size, QPen(Qt.GlobalColor.black))

    def setCellViewColor(self, x, y, color):
        pos = x * self.columns + y
        brush = QBrush(color)
        self.cells[pos].setBrush(brush)

    def redrawUniverse(self):
        for i in range(self.columns):
            for j in range(self.rows):
                self.setCellViewColor(i, j, self.universe.colors[self.universe.getCellStatus(i, j)])

    def step(self):
        stime = time.time()
        self.universe.next_gen()
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


class ToolBar(QWidget):
    def __init__(self, view):
        super().__init__()
        layout = QVBoxLayout()

        btn_clear = QPushButton("Clear")
        layout.addWidget(btn_clear)
        btn_clear.clicked.connect(lambda: view.reset())

        btn_rand = QPushButton("Randomize")
        layout.addWidget(btn_rand)
        btn_rand.clicked.connect(lambda: view.randomize())

        btn_step = QPushButton("Step")
        layout.addWidget(btn_step)
        btn_step.clicked.connect(lambda: view.step())

        btn_start = QPushButton("Run")
        btn_start.setCheckable(True)
        btn_start.clicked.connect(lambda c: view.runEvo(c))

        lbl_fps = QLabel()
        #lbl_fps.setMaximumHeight(10)
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

        layout.addWidget(lbl_fps)
        layout.addWidget(lbl_ms)
        layout.addWidget(slider_speed)
        layout.addWidget(btn_start)

        layout.addStretch()

        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("GOL")

        self.view = UniverseView()
        self.tools = ToolBar(self.view)

        hbox = QHBoxLayout(self)

        hbox.addWidget(self.view)
        hbox.addWidget(self.tools)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
