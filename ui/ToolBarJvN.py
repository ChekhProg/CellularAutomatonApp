import json

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpinBox, QFileDialog, \
    QGridLayout, QLayout


class ToolBarJvN(QWidget):
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
        self.spinbox_rows.setRange(25, 100)
        self.spinbox_rows.setValue(view.rows)
        self.spinbox_rows.valueChanged.connect(lambda x: self.changeRows(x))

        self.rows_layout = QHBoxLayout()
        self.rows_layout.addWidget(lbl_rows)
        self.rows_layout.addWidget(self.spinbox_rows)
        # End Rows Layout

        # Rows Horizontal Layout
        lbl_columns = QLabel("Columns: ")
        self.spinbox_columns = QSpinBox()
        self.spinbox_columns.setRange(25, 100)
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

        # Size Step Layout
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(lambda: self.clear())

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

        btn_state_size = QSize(40, 40)

        btn_u = QPushButton("U")
        btn_u.setCheckable(True)
        btn_u.setFixedSize(btn_state_size)
        btn_u.clicked.connect(lambda e: self.changeDrawerState(e, 0))
        btn_u.setStyleSheet("background-color: rgb(48,48,48); color: white")
        btn_u.click()
        self.state_btns.append(btn_u)

        btn_s = QPushButton("S")
        btn_s.setCheckable(True)
        btn_s.setFixedSize(btn_state_size)
        btn_s.clicked.connect(lambda e: self.changeDrawerState(e, 1))
        btn_s.setStyleSheet("background-color: rgb(255,0,0); color: black")
        self.state_btns.append(btn_s)

        btn_s_0 = QPushButton("S_0")
        btn_s_0.setCheckable(True)
        btn_s_0.setFixedSize(btn_state_size)
        btn_s_0.clicked.connect(lambda e: self.changeDrawerState(e, 2))
        btn_s_0.setStyleSheet("background-color: rgb(255,125,0); color: black")
        self.state_btns.append(btn_s_0)

        btn_s_00 = QPushButton("S_00")
        btn_s_00.setCheckable(True)
        btn_s_00.setFixedSize(btn_state_size)
        btn_s_00.clicked.connect(lambda e: self.changeDrawerState(e, 3))
        btn_s_00.setStyleSheet("background-color: rgb(255, 175, 50); color: black")
        self.state_btns.append(btn_s_00)

        btn_s_000 = QPushButton("S_000")
        btn_s_000.setCheckable(True)
        btn_s_000.setFixedSize(btn_state_size)
        btn_s_000.clicked.connect(lambda e: self.changeDrawerState(e, 4))
        btn_s_000.setStyleSheet("background-color: rgb(251, 255, 0); color: black")
        self.state_btns.append(btn_s_000)

        btn_s_01 = QPushButton("S_01")
        btn_s_01.setCheckable(True)
        btn_s_01.setFixedSize(btn_state_size)
        btn_s_01.clicked.connect(lambda e: self.changeDrawerState(e, 5))
        btn_s_01.setStyleSheet("background-color: rgb(255, 200, 75); color: black")
        self.state_btns.append(btn_s_01)

        btn_s_1 = QPushButton("S_1")
        btn_s_1.setCheckable(True)
        btn_s_1.setFixedSize(btn_state_size)
        btn_s_1.clicked.connect(lambda e: self.changeDrawerState(e, 6))
        btn_s_1.setStyleSheet("background-color: rgb(255, 150, 25); color: black")
        self.state_btns.append(btn_s_1)

        btn_s_10 = QPushButton("S_10")
        btn_s_10.setCheckable(True)
        btn_s_10.setFixedSize(btn_state_size)
        btn_s_10.clicked.connect(lambda e: self.changeDrawerState(e, 7))
        btn_s_10.setStyleSheet("background-color: rgb(255, 255, 100); color: black")
        self.state_btns.append(btn_s_10)

        btn_s_11 = QPushButton("S_11")
        btn_s_11.setCheckable(True)
        btn_s_11.setFixedSize(btn_state_size)
        btn_s_11.clicked.connect(lambda e: self.changeDrawerState(e, 8))
        btn_s_11.setStyleSheet("background-color: rgb(255, 250, 125); color: black")
        self.state_btns.append(btn_s_11)

        btn_c_00 = QPushButton("C_00")
        btn_c_00.setCheckable(True)
        btn_c_00.setFixedSize(btn_state_size)
        btn_c_00.clicked.connect(lambda e: self.changeDrawerState(e, 9))
        btn_c_00.setStyleSheet("background-color: rgb(0, 255, 128); color: black")
        self.state_btns.append(btn_c_00)

        btn_c_01 = QPushButton("C_01")
        btn_c_01.setCheckable(True)
        btn_c_01.setFixedSize(btn_state_size)
        btn_c_01.clicked.connect(lambda e: self.changeDrawerState(e, 10))
        btn_c_01.setStyleSheet("background-color: rgb(33, 215, 215); color: black")
        self.state_btns.append(btn_c_01)

        btn_c_10 = QPushButton("C_10")
        btn_c_10.setCheckable(True)
        btn_c_10.setFixedSize(btn_state_size)
        btn_c_10.clicked.connect(lambda e: self.changeDrawerState(e, 11))
        btn_c_10.setStyleSheet("background-color: rgb(255, 255, 128); color: black")
        self.state_btns.append(btn_c_10)

        btn_c_11 = QPushButton("C_11")
        btn_c_11.setCheckable(True)
        btn_c_11.setFixedSize(btn_state_size)
        btn_c_11.clicked.connect(lambda e: self.changeDrawerState(e, 12))
        btn_c_11.setStyleSheet("background-color: rgb(255, 128, 64); color: black")
        self.state_btns.append(btn_c_11)

        btn_ot_n_q = QPushButton("OT_N_Q")
        btn_ot_n_q.setCheckable(True)
        btn_ot_n_q.setFixedSize(btn_state_size)
        btn_ot_n_q.clicked.connect(lambda e: self.changeDrawerState(e, 13))
        btn_ot_n_q.setStyleSheet("background-color: rgb(106, 106, 255); color: black")
        self.state_btns.append(btn_ot_n_q)

        btn_ot_s_q = QPushButton("OT_S_Q")
        btn_ot_s_q.setCheckable(True)
        btn_ot_s_q.setFixedSize(btn_state_size)
        btn_ot_s_q.clicked.connect(lambda e: self.changeDrawerState(e, 14))
        btn_ot_s_q.setStyleSheet("background-color: rgb(139, 139, 255); color: black")
        self.state_btns.append(btn_ot_s_q)

        btn_ot_w_q = QPushButton("OT_W_Q")
        btn_ot_w_q.setCheckable(True)
        btn_ot_w_q.setFixedSize(btn_state_size)
        btn_ot_w_q.clicked.connect(lambda e: self.changeDrawerState(e, 15))
        btn_ot_w_q.setStyleSheet("background-color: rgb(122, 122, 255); color: black")
        self.state_btns.append(btn_ot_w_q)

        btn_ot_e_q = QPushButton("OT_E_Q")
        btn_ot_e_q.setCheckable(True)
        btn_ot_e_q.setFixedSize(btn_state_size)
        btn_ot_e_q.clicked.connect(lambda e: self.changeDrawerState(e, 16))
        btn_ot_e_q.setStyleSheet("background-color: rgb(89, 89, 255); color: black")
        self.state_btns.append(btn_ot_e_q)

        btn_ot_n_e = QPushButton("OT_N_E")
        btn_ot_n_e.setCheckable(True)
        btn_ot_n_e.setFixedSize(btn_state_size)
        btn_ot_n_e.clicked.connect(lambda e: self.changeDrawerState(e, 17))
        btn_ot_n_e.setStyleSheet("background-color: rgb(36, 200, 36); color: black")
        self.state_btns.append(btn_ot_n_e)

        btn_ot_s_e = QPushButton("OT_S_E")
        btn_ot_s_e.setCheckable(True)
        btn_ot_s_e.setFixedSize(btn_state_size)
        btn_ot_s_e.clicked.connect(lambda e: self.changeDrawerState(e, 18))
        btn_ot_s_e.setStyleSheet("background-color: rgb(106, 255, 106); color: black")
        self.state_btns.append(btn_ot_s_e)

        btn_ot_w_e = QPushButton("OT_W_E")
        btn_ot_w_e.setCheckable(True)
        btn_ot_w_e.setFixedSize(btn_state_size)
        btn_ot_w_e.clicked.connect(lambda e: self.changeDrawerState(e, 19))
        btn_ot_w_e.setStyleSheet("background-color: rgb(73, 255, 73); color: black")
        self.state_btns.append(btn_ot_w_e)

        btn_ot_e_e = QPushButton("OT_E_E")
        btn_ot_e_e.setCheckable(True)
        btn_ot_e_e.setFixedSize(btn_state_size)
        btn_ot_e_e.clicked.connect(lambda e: self.changeDrawerState(e, 20))
        btn_ot_e_e.setStyleSheet("background-color: rgb(27, 176, 27); color: black")
        self.state_btns.append(btn_ot_e_e)

        btn_st_n_q = QPushButton("ST_N_Q")
        btn_st_n_q.setCheckable(True)
        btn_st_n_q.setFixedSize(btn_state_size)
        btn_st_n_q.clicked.connect(lambda e: self.changeDrawerState(e, 21))
        btn_st_n_q.setStyleSheet("background-color: rgb(255, 56, 56); color: black")
        self.state_btns.append(btn_st_n_q)

        btn_st_s_q = QPushButton("ST_S_Q")
        btn_st_s_q.setCheckable(True)
        btn_st_s_q.setFixedSize(btn_state_size)
        btn_st_s_q.clicked.connect(lambda e: self.changeDrawerState(e, 22))
        btn_st_s_q.setStyleSheet("background-color: rgb(255, 89, 89); color: black")
        self.state_btns.append(btn_st_s_q)

        btn_st_w_q = QPushButton("ST_W_Q")
        btn_st_w_q.setCheckable(True)
        btn_st_w_q.setFixedSize(btn_state_size)
        btn_st_w_q.clicked.connect(lambda e: self.changeDrawerState(e, 23))
        btn_st_w_q.setStyleSheet("background-color: rgb(255, 73, 73); color: black")
        self.state_btns.append(btn_st_w_q)

        btn_st_e_q = QPushButton("ST_E_Q")
        btn_st_e_q.setCheckable(True)
        btn_st_e_q.setFixedSize(btn_state_size)
        btn_st_e_q.clicked.connect(lambda e: self.changeDrawerState(e, 24))
        btn_st_e_q.setStyleSheet("background-color: rgb(235, 36, 36); color: black")
        self.state_btns.append(btn_st_e_q)

        btn_st_n_e = QPushButton("ST_N_E")
        btn_st_n_e.setCheckable(True)
        btn_st_n_e.setFixedSize(btn_state_size)
        btn_st_n_e.clicked.connect(lambda e: self.changeDrawerState(e, 25))
        btn_st_n_e.setStyleSheet("background-color: rgb(191, 73, 255); color: black")
        self.state_btns.append(btn_st_n_e)

        btn_st_s_e = QPushButton("ST_S_E")
        btn_st_s_e.setCheckable(True)
        btn_st_s_e.setFixedSize(btn_state_size)
        btn_st_s_e.clicked.connect(lambda e: self.changeDrawerState(e, 26))
        btn_st_s_e.setStyleSheet("background-color: rgb(203, 106, 255); color: black")
        self.state_btns.append(btn_st_s_e)

        btn_st_w_e = QPushButton("ST_W_E")
        btn_st_w_e.setCheckable(True)
        btn_st_w_e.setFixedSize(btn_state_size)
        btn_st_w_e.clicked.connect(lambda e: self.changeDrawerState(e, 27))
        btn_st_w_e.setStyleSheet("background-color: rgb(197, 89, 255); color: black")
        self.state_btns.append(btn_st_w_e)

        btn_st_e_e = QPushButton("ST_E_E")
        btn_st_e_e.setCheckable(True)
        btn_st_e_e.setFixedSize(btn_state_size)
        btn_st_e_e.clicked.connect(lambda e: self.changeDrawerState(e, 28))
        btn_st_e_e.setStyleSheet("background-color: rgb(185, 56, 255); color: black")
        self.state_btns.append(btn_st_e_e)

        # for btn in self.state_btns:
        #     btn.setFont(QFont('Arial', 7))
        #     btn.setCheckable(True)
        #     btn.setFixedSize(btn_state_size)

        state_layout = QGridLayout()
        state_layout.addWidget(btn_u, 0, 0)

        state_layout.addWidget(btn_s, 1, 0)
        state_layout.addWidget(btn_s_0, 1, 1)
        state_layout.addWidget(btn_s_00, 1, 2)
        state_layout.addWidget(btn_s_000, 1, 3)

        state_layout.addWidget(btn_s_01, 2, 0)
        state_layout.addWidget(btn_s_1, 2, 1)
        state_layout.addWidget(btn_s_10, 2, 2)
        state_layout.addWidget(btn_s_11, 2, 3)

        state_layout.addWidget(btn_c_00, 3, 0)
        state_layout.addWidget(btn_c_01, 3, 1)
        state_layout.addWidget(btn_c_10, 3, 2)
        state_layout.addWidget(btn_c_11, 3, 3)

        state_layout.addWidget(btn_ot_n_q, 4, 0)
        state_layout.addWidget(btn_ot_s_q, 4, 1)
        state_layout.addWidget(btn_ot_w_q, 4, 2)
        state_layout.addWidget(btn_ot_e_q, 4, 3)

        state_layout.addWidget(btn_ot_n_e, 5, 0)
        state_layout.addWidget(btn_ot_s_e, 5, 1)
        state_layout.addWidget(btn_ot_w_e, 5, 2)
        state_layout.addWidget(btn_ot_e_e, 5, 3)

        state_layout.addWidget(btn_st_n_q, 6, 0)
        state_layout.addWidget(btn_st_s_q, 6, 1)
        state_layout.addWidget(btn_st_w_q, 6, 2)
        state_layout.addWidget(btn_st_e_q, 6, 3)

        state_layout.addWidget(btn_st_n_e, 7, 0)
        state_layout.addWidget(btn_st_s_e, 7, 1)
        state_layout.addWidget(btn_st_w_e, 7, 2)
        state_layout.addWidget(btn_st_e_e, 7, 3)

        state_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        state_widget.setLayout(state_layout)
        # End State Layout

        btn_type = QPushButton("Choose Automaton Type")
        btn_type.clicked.connect(lambda: self.changeType())

        layout.addLayout(self.rows_layout)
        layout.addLayout(self.columns_layout)
        layout.addLayout(self.size_layout)
        layout.addWidget(self.btn_clear)
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
        self.view.reset()
        self.btn_start.setChecked(False)

    def randomize(self):
        self.view.runEvo(False)
        self.view.randomize()
        self.btn_start.setChecked(False)

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