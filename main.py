import sys

from PyQt6.QtWidgets import QApplication

from ui.SelectionWindow import SelectionWindow

app = QApplication(sys.argv)

window = SelectionWindow()
window.show()

app.exec()
