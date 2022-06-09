from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsRectItem


class CellView(QGraphicsRectItem):
    def __init__(self, universe, size, x, y):
        super().__init__(0, 0, size, size)
        self.x = x
        self.y = y
        self.universe = universe

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            i = self.y
            j = self.x
            new_state = self.universe.changeCellState(i, j)
            print("x: {}, y: {}, state: {}".format(self.x, self.y, new_state))
            brush = QBrush(self.universe.colors[new_state])
            self.setBrush(brush)
        elif e.button() == Qt.MouseButton.RightButton:
            i = self.y
            j = self.x
            new_state = self.universe.changeCellState(i, j, 0)
            brush = QBrush(self.universe.colors[new_state])
            self.setBrush(brush)