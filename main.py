import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLayout, QWidget

from ui.SelectionWindow import SelectionWindow
from ui.ToolBar import ToolBar
from ui.UniverseView import UniverseView

app = QApplication(sys.argv)

window = SelectionWindow()
window.show()

app.exec()
