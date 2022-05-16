import sys
import time

import numpy as np
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QBrush, QPen, QPalette, QColor, QWindow
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QMainWindow, QWidget, \
    QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSlider, QLabel, QGridLayout, QSpinBox, QLineEdit, QLayout

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
        columns = 80
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
        print(self.cells.size)
        print(self.rows)
        print(self.columns)
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
        #print(etime)

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


class ToolBar(QWidget):
    def __init__(self, view):
        super().__init__()
        self.setFixedWidth(150)
        layout = QVBoxLayout()

        # Rows Horizontal Layout
        rows_layout = QHBoxLayout()

        lbl_rows = QLabel("Rows: ")
        spinbox_rows = QSpinBox()
        spinbox_rows.setRange(40, 200)
        spinbox_rows.setValue(view.rows)
        spinbox_rows.lineEdit().setDisabled(True)
        spinbox_rows.valueChanged.connect(lambda x: view.changeRows(x))

        rows_layout.addWidget(lbl_rows)
        rows_layout.addWidget(spinbox_rows)
        # End Rows Layout

        # Rows Horizontal Layout
        columns_layout = QHBoxLayout()

        lbl_columns = QLabel("Columns: ")
        spinbox_columns = QSpinBox()
        spinbox_columns.setRange(40, 200)
        spinbox_columns.setValue(view.columns)
        spinbox_columns.lineEdit().setDisabled(True)
        spinbox_columns.valueChanged.connect(lambda x: view.changeColumns(x))

        columns_layout.addWidget(lbl_columns)
        columns_layout.addWidget(spinbox_columns)
        # End Rows Layout

        # Size Horizontal Layout
        size_layout = QHBoxLayout()

        lbl_size = QLabel("Size: ")
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(1, 20)
        spinbox_steps.setValue(view.size)
        spinbox_steps.lineEdit().setDisabled(True)
        spinbox_steps.valueChanged.connect(lambda s: view.changeSize(s))

        size_layout.addWidget(lbl_size)
        size_layout.addWidget(spinbox_steps)
        # Size Step Layout

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(lambda: view.reset())

        btn_rand = QPushButton("Randomize")
        btn_rand.clicked.connect(lambda: view.randomize())

        # Step Horizontal Layout
        step_layout = QHBoxLayout()
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(1, 1000)
        btn_step = QPushButton("Step")
        btn_step.clicked.connect(lambda: view.step(spinbox_steps.value()))
        step_layout.addWidget(btn_step)
        step_layout.addWidget(spinbox_steps)

        btn_start = QPushButton("Run")
        btn_start.setCheckable(True)
        btn_start.clicked.connect(lambda c: view.runEvo(c))
        # End Step Layout

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

        layout.addLayout(rows_layout)
        layout.addLayout(columns_layout)
        layout.addLayout(size_layout)
        layout.addWidget(btn_clear)
        layout.addWidget(btn_rand)
        layout.addLayout(step_layout)
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
