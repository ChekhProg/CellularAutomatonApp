from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout

from ui.AutomatonWindows import GolWindow, BriansBrainWindow, WireworldWindow, VonNeumannWindow


class SelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton")
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        # self.setFixedWidth(200)
        self.setFixedWidth(280)

        btn_Gof = QPushButton("Game Of Life")
        btn_Gof.clicked.connect(self.selectGof)

        btn_Bb = QPushButton("Brian's Brain")
        btn_Bb.clicked.connect(self.selectBb)

        btn_Ww = QPushButton("Wireworld")
        btn_Ww.clicked.connect(self.selectWw)

        btn_Vn = QPushButton("Von Neumann Automaton")
        btn_Vn.clicked.connect(self.selectVn)

        vbox.addWidget(btn_Gof)
        vbox.addWidget(btn_Bb)
        vbox.addWidget(btn_Ww)
        vbox.addWidget(btn_Vn)

        self.setLayout(vbox)

    def selectGof(self):
        self.hide()
        self.w = GolWindow(self)
        self.w.show()

    def selectBb(self):
        self.hide()
        w = BriansBrainWindow(self)
        w.show()

    def selectWw(self):
        self.hide()
        w = WireworldWindow(self)
        w.show()

    def selectVn(self):
        self.hide()
        w = VonNeumannWindow(self)
        w.show()