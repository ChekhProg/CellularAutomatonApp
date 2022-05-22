from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QWidget, \
    QHBoxLayout, QLayout

from ui.ToolBar import ToolBar
from ui.ToolBarGol import ToolBarGol
from ui.ToolBarWireworld import ToolBarWireworld
from ui.UniverseView import UniverseView
from PyQt6.QtWidgets import QWidget, \
    QHBoxLayout, QLayout

from ui.ToolBar import ToolBar
from ui.ToolBarGol import ToolBarGol
from ui.ToolBarWireworld import ToolBarWireworld
from ui.UniverseView import UniverseView


class GolWindow(QWidget):
    def __init__(self, selection_window):
        super().__init__()
        self.setWindowTitle("Game Of Life")

        self.view = UniverseView(self, "GameOfLife")
        self.tools = ToolBarGol(self.view, selection_window)

        gl = QOpenGLWidget()

        form = QSurfaceFormat()
        form.setSamples(4)
        gl.setFormat(form)
        self.view.setViewport(gl)

        hbox = QHBoxLayout(self)
        hbox.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        hbox.addWidget(self.tools)
        hbox.addWidget(self.view)

        self.setLayout(hbox)
        self.setFixedSize(self.sizeHint())


class BriansBrainWindow(QWidget):
    def __init__(self, selection_window):
        super().__init__()
        self.setWindowTitle("Brian's Brain")

        self.view = UniverseView(self, "BriansBrain")
        self.view.initCellsView()
        self.view.redrawUniverse()
        self.tools = ToolBar(self.view, selection_window)

        hbox = QHBoxLayout(self)
        hbox.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        hbox.addWidget(self.tools)
        hbox.addWidget(self.view)

        self.setLayout(hbox)
        self.setFixedSize(self.sizeHint())


class WireworldWindow(QWidget):
    def __init__(self, selection_window):
        super().__init__()
        self.setWindowTitle("Wireworld")

        self.view = UniverseView(self, "Wireworld")
        self.view.initCellsView()
        self.view.redrawUniverse()
        self.tools = ToolBarWireworld(self.view, selection_window)

        hbox = QHBoxLayout(self)
        hbox.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        hbox.addWidget(self.tools)
        hbox.addWidget(self.view)

        self.setLayout(hbox)
        self.setFixedSize(self.sizeHint())
