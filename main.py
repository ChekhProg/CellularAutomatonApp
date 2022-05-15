import sys
import time

from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QBrush, QPen, QPalette, QColor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QMainWindow, QWidget, \
    QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSlider, QLabel

from GridSquare2D import GridSquare2D
from GridSquare2DFlat import GridSquare2DFlat


class UniverseView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.step())

        rows = 100
        self.rows = rows
        columns = 100
        self.columns = columns
        size = 4
        self.size = size

        self.scene = QGraphicsScene(0, 0, columns * size, rows * size)

        # test
        self.universe = GridSquare2DFlat(self.rows, self.columns)
        self.redrawUniverse()
        # test

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setScene(self.scene)

    def drawGrid(self):
        rows = self.rows
        columns = self.columns
        size = self.size
        for x in range(rows):
            self.scene.addLine(0, x * size, columns * size, x * size, QPen(Qt.GlobalColor.black))

        for y in range(columns):
            self.scene.addLine(y * size, 0, y * size, rows * size, QPen(Qt.GlobalColor.black))

    def drawCellColor(self, x, y, color):
        cell = QGraphicsRectItem(0, 0, self.size, self.size)
        cell.setPos(x * self.size, y * self.size)
        brush = QBrush(color)
        cell.setBrush(brush)
        self.scene.addItem(cell)

    def redrawUniverse(self):
        self.scene.clear()
        self.drawGrid()
        self.drawLife()

    def drawLife(self):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.universe.getCellStatus(i, j) == 1:
                    self.drawCellColor(i, j, Qt.GlobalColor.black)

    def step(self):
        stime = time.time()
        self.universe.next_gen()
        etime = time.time() - stime
        self.redrawUniverse()

        print(etime)

    def reset(self):
        self.universe.clear()
        self.redrawUniverse()

    def randomize(self):
        self.universe.set_random()
        self.redrawUniverse()

    def startEvo(self):
        self.timer.start()

    def stopEvo(self):
        self.timer.stop()

    def changeSpeed(self, i: float):
        self.timer.setInterval(1000//int(i))



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

        btn_start = QPushButton("Start")
        layout.addWidget(btn_start)
        btn_start.clicked.connect(lambda: view.startEvo())

        lbl_fps = QLabel()

        lbl_ms = QLabel()

        slider_speed = QSlider(Qt.Orientation.Horizontal)
        slider_speed.setRange(1, 25)
        #slider_speed.setSingleStep(1)
        view.timer.setInterval(1000//slider_speed.value())
        slider_speed.valueChanged.connect(lambda i: view.changeSpeed(i))
        slider_speed.valueChanged.connect(lambda i: lbl_fps.setText("FPS: "+str(i)))
        slider_speed.valueChanged.connect(lambda i: lbl_ms.setText("ms: " + str(1000//i)))

        lbl_fps.setText("FPS: "+str(slider_speed.value()))
        lbl_ms.setText("ms: " + str(1000//slider_speed.value()))

        layout.addWidget(lbl_fps)
        layout.addWidget(lbl_ms)
        layout.addWidget(slider_speed)


        btn_stop = QPushButton("Stop")
        layout.addWidget(btn_stop)
        btn_stop.clicked.connect(lambda: view.stopEvo())

        btn = QPushButton("Draw One")
        layout.addWidget(btn)
        btn.clicked.connect(lambda: view.drawCellColor(1, 1, Qt.GlobalColor.black))

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
