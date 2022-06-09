import json

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpinBox, QFileDialog, \
    QGridLayout, QLayout


class ToolBar(QWidget):
    def __init__(self, view, selection_window):
        super().__init__()
        self.selection_window = selection_window
        self.view = view
        self.setFixedWidth(280)
        layout = QVBoxLayout()

        # Run
        self.btn_start = QPushButton("Run")
        self.btn_start.setCheckable(True)
        self.btn_start.clicked.connect(lambda c: view.runEvo(c))

        self.lbl_fps = QLabel()
        self.lbl_ms = QLabel()

        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setRange(2, 60)
        self.slider_speed.setSliderPosition(10)
        view.timer.setInterval(1000 // self.slider_speed.value())
        self.slider_speed.valueChanged.connect(lambda i: view.changeSpeed(i))
        self.slider_speed.valueChanged.connect(lambda i: self.lbl_fps.setText("FPS: " + str(i)))
        self.slider_speed.valueChanged.connect(lambda i: self.lbl_ms.setText("ms: " + str(1000 // i)))

        self.lbl_fps.setText("FPS: " + str(self.slider_speed.value()))
        self.lbl_ms.setText("ms: " + str(1000 // self.slider_speed.value()))
        # End Run

        # Rows Horizontal Layout
        lbl_rows = QLabel("Rows: ")
        self.spinbox_rows = QSpinBox()
        self.spinbox_rows.setRange(40, 100)
        self.spinbox_rows.setValue(view.rows)
        self.spinbox_rows.valueChanged.connect(lambda x: self.changeRows(x))

        self.rows_layout = QHBoxLayout()
        self.rows_layout.addWidget(lbl_rows)
        self.rows_layout.addWidget(self.spinbox_rows)
        # End Rows Layout

        # Rows Horizontal Layout
        lbl_columns = QLabel("Columns: ")
        self.spinbox_columns = QSpinBox()
        self.spinbox_columns.setRange(40, 100)
        self.spinbox_columns.setValue(view.columns)
        self.spinbox_columns.valueChanged.connect(lambda x: self.changeColumns(x))

        self.columns_layout = QHBoxLayout()
        self.columns_layout.addWidget(lbl_columns)
        self.columns_layout.addWidget(self.spinbox_columns)
        # End Rows Layout

        # Size Horizontal Layout
        lbl_size = QLabel("Size: ")
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(5, 13)
        spinbox_steps.setValue(view.size)
        spinbox_steps.lineEdit().setDisabled(True)
        spinbox_steps.valueChanged.connect(lambda s: view.changeSize(s))

        self.size_layout = QHBoxLayout()
        self.size_layout.addWidget(lbl_size)
        self.size_layout.addWidget(spinbox_steps)
        # End Size Horizontal Layout

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(lambda: self.clear())

        self.btn_rand = QPushButton("Randomize")
        self.btn_rand.clicked.connect(lambda: self.randomize())

        # Step Horizontal Layout
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(1, 1000)
        btn_step = QPushButton("Step")
        btn_step.setCheckable(True)
        btn_step.clicked.connect(lambda: view.step(spinbox_steps.value(), btn_step))

        self.step_layout = QHBoxLayout()
        self.step_layout.addWidget(btn_step)
        self.step_layout.addWidget(spinbox_steps)
        # End Step Layout

        # Open
        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(lambda: self.openFile())
        # End Open

        # Save
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(lambda: self.saveFile())
        # End Save

        # State Layout
        state_widget = QWidget()
        state_label = QLabel("Cell drawer state:")
        self.state_btns = []
        btn_0 = QPushButton("0")
        btn_0.setCheckable(True)
        btn_0.setFixedSize(QSize(25, 25))
        btn_0.clicked.connect(lambda e: self.changeDrawerState(e, 0))
        btn_0.setStyleSheet("background-color: black; color: white")
        btn_0.click()
        self.state_btns.append(btn_0)
        btn_1 = QPushButton("1")
        btn_1.setCheckable(True)
        btn_1.setFixedSize(QSize(25, 25))
        btn_1.clicked.connect(lambda e: self.changeDrawerState(e, 1))
        btn_1.setStyleSheet("background-color: rgb(255,255,255); color: black")
        self.state_btns.append(btn_1)

        btn_2 = QPushButton("2")
        btn_2.setCheckable(True)
        btn_2.setFixedSize(QSize(25, 25))
        btn_2.clicked.connect(lambda e: self.changeDrawerState(e, 2))
        btn_2.setStyleSheet("background-color: rgb(255,0,0); color: black")
        self.state_btns.append(btn_2)

        state_layout = QGridLayout()
        state_layout.addWidget(btn_0, 0, 0)
        state_layout.addWidget(btn_1, 0, 1)
        state_layout.addWidget(btn_2, 0, 2)
        state_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        state_widget.setLayout(state_layout)
        # End State Layout

        btn_type = QPushButton("Choose Automaton Type")
        btn_type.clicked.connect(lambda: self.changeType())

        layout.addLayout(self.rows_layout)
        layout.addLayout(self.columns_layout)
        layout.addLayout(self.size_layout)
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_rand)
        layout.addLayout(self.step_layout)
        layout.addWidget(self.lbl_fps)
        layout.addWidget(self.lbl_ms)
        layout.addWidget(self.slider_speed)
        layout.addWidget(self.btn_start)
        layout.addWidget(state_label)
        layout.addWidget(state_widget)
        layout.addStretch()
        layout.addWidget(btn_type)
        layout.addStretch()
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def changeRows(self, x):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.view.changeRows(x)

    def changeColumns(self, x):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.view.changeColumns(x)

    def clear(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.view.reset()

    def randomize(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.view.randomize()

    def openFile(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        filename = QFileDialog.getOpenFileName(caption="Open File", filter="*.json")[0]
        if filename != '':
            with open(filename, "r") as read_file:
                data = json.load(read_file)
            self.spinbox_columns.setValue(data["width"])
            self.spinbox_rows.setValue(data["height"])
            self.view.fromJson(filename)

    def saveFile(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        filename = QFileDialog.getSaveFileName(caption="Save File", filter="*.json")[0]
        if filename != '':
            self.view.toJson(filename)

    def changeType(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.selection_window.show()
        self.parent().close()

    def changeDrawerState(self, e, btn_ind):
        if e:
            self.view.drawer_state = btn_ind
            for i, b in enumerate(self.state_btns):
                if not i == btn_ind:
                    b.setChecked(False)
        else:
            self.state_btns[btn_ind].setChecked(True)