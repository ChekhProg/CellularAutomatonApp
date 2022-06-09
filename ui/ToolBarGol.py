import json

import numpy as np
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpinBox, QComboBox, \
    QLineEdit, QRadioButton, QCheckBox, QFileDialog


class ToolBarGol(QWidget):
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
        # End Run

        # Rows Horizontal Layout
        lbl_rows = QLabel("Rows: ")
        self.spinbox_rows = QSpinBox()
        self.spinbox_rows.setRange(10, 150)
        self.spinbox_rows.setValue(view.rows)
        self.spinbox_rows.valueChanged.connect(lambda x: self.changeRows(x))

        rows_layout = QHBoxLayout()
        rows_layout.addWidget(lbl_rows)
        rows_layout.addWidget(self.spinbox_rows)
        # End Rows Layout

        # Rows Horizontal Layout
        lbl_columns = QLabel("Columns: ")
        self.spinbox_columns = QSpinBox()
        self.spinbox_columns.setRange(10, 150)
        self.spinbox_columns.setValue(view.columns)
        self.spinbox_columns.valueChanged.connect(lambda x: self.changeColumns(x))

        columns_layout = QHBoxLayout()
        columns_layout.addWidget(lbl_columns)
        columns_layout.addWidget(self.spinbox_columns)
        # End Rows Layout

        # Size Horizontal Layout
        lbl_size = QLabel("Size: ")
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(4, 13)
        spinbox_steps.setValue(view.size)
        spinbox_steps.lineEdit().setDisabled(True)
        spinbox_steps.valueChanged.connect(lambda s: view.changeSize(s))

        size_layout = QHBoxLayout()
        size_layout.addWidget(lbl_size)
        size_layout.addWidget(spinbox_steps)

        # Size Step Layout

        # Rule Layout
        combobox_rule = QComboBox()
        combobox_rule.addItem("B3/S23 : Life")
        combobox_rule.addItem("B1357/S1357 : Replicator")
        combobox_rule.addItem("B35678/S5678 : Diamoeba")
        combobox_rule.addItem("B4678/S35678 : Anneal")
        combobox_rule.addItem("B2/S12345 : Maze")
        combobox_rule.addItem("B3/S012345678 : Life without Death")
        combobox_rule.addItem("B34/S34 : 34 Life")
        combobox_rule.addItem("B36/S125 : 2x2")
        combobox_rule.addItem("B36/S23 : HighLife")
        combobox_rule.addItem("B3678/S34678 : Day & Night")
        combobox_rule.addItem("B368/S245 : Morley")
        combobox_rule.addItem("B2/S : Seeds")
        combobox_rule.addItem("B25/S4")

        combobox_rule.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combobox_rule.currentTextChanged.connect(lambda s: self.ruleChanged(s))

        lbl_b = QLabel("B:")
        ledit_b = QLineEdit()
        lbl_s = QLabel("S:")
        ledit_s = QLineEdit()
        ledit_s.textChanged.connect(lambda: self.getCustomRule(ledit_b, ledit_s))
        ledit_b.textChanged.connect(lambda: self.getCustomRule(ledit_b, ledit_s))

        regexp = QRegularExpression("1?2?3?4?5?6?7?8?")
        validator = QRegularExpressionValidator(regexp)
        ledit_s.setValidator(validator)
        ledit_b.setValidator(validator)

        radio_btn_fixed_rule = QRadioButton("Fixed Rule:")
        radio_btn_fixed_rule.clicked.connect(lambda: self.setFixedRule(combobox_rule, ledit_b, ledit_s))
        radio_btn_custom_rule = QRadioButton("Custom Rule:")
        radio_btn_custom_rule.clicked.connect(lambda: self.setCustomRule(combobox_rule, ledit_b, ledit_s))

        radio_btn_fixed_rule.setChecked(True)
        self.setFixedRule(combobox_rule, ledit_b, ledit_s)

        rule_fixed_layout = QHBoxLayout()
        rule_fixed_layout.addWidget(radio_btn_fixed_rule)
        rule_fixed_layout.addWidget(combobox_rule)

        rule_custom_layout = QHBoxLayout()
        rule_custom_layout.addWidget(radio_btn_custom_rule)
        rule_custom_layout.addWidget(lbl_b)
        rule_custom_layout.addWidget(ledit_b)
        rule_custom_layout.addWidget(lbl_s)
        rule_custom_layout.addWidget(ledit_s)

        rule_layout = QVBoxLayout()
        rule_layout.addLayout(rule_fixed_layout)
        rule_layout.addLayout(rule_custom_layout)
        # End Rule Layout

        # Age Layout
        age_layout = QHBoxLayout()
        checkbox_age = QCheckBox("With Age")
        age_layout.addWidget(checkbox_age)
        checkbox_age.stateChanged.connect(lambda s: self.ageChanged(s))
        # End Age Layout

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(lambda: self.clear())

        btn_rand = QPushButton("Randomize")
        btn_rand.clicked.connect(lambda: self.randomize())

        # Step Horizontal Layout
        spinbox_steps = QSpinBox()
        spinbox_steps.setRange(1, 1000)
        btn_step = QPushButton("Step")
        btn_step.setCheckable(True)
        btn_step.clicked.connect(lambda: view.step(spinbox_steps.value(), btn_step))

        step_layout = QHBoxLayout()
        step_layout.addWidget(btn_step)
        step_layout.addWidget(spinbox_steps)
        # End Step Layout

        # Open
        btn_open = QPushButton("Open")
        btn_open.clicked.connect(lambda: self.openFile())
        # End Open

        # Save
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(lambda: self.saveFile())
        # End Save

        btn_type = QPushButton("Choose Automaton Type")
        btn_type.clicked.connect(lambda: self.changeType())

        layout.addLayout(rows_layout)
        layout.addLayout(columns_layout)
        layout.addLayout(size_layout)
        layout.addLayout(rule_layout)
        layout.addLayout(age_layout)
        layout.addWidget(btn_clear)
        layout.addWidget(btn_rand)
        layout.addLayout(step_layout)
        layout.addWidget(lbl_fps)
        layout.addWidget(lbl_ms)
        layout.addWidget(slider_speed)
        layout.addWidget(self.btn_start)
        layout.addStretch()
        layout.addWidget(btn_type)
        layout.addStretch()
        layout.addWidget(btn_open)
        layout.addWidget(btn_save)

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

    def ruleChanged(self, s):
        rule = s.split(" ")[0]
        rule = ''.join(filter(lambda c: not str.isalpha(c), rule))
        rule = rule.split("/")
        birth = [int(s) for s in rule[0]]
        survive = [int(s) for s in rule[1]]
        rule = {"B": birth, "S": survive}
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.view.universe.rule = rule
        self.view.rule = rule

    def setFixedRule(self, combobox, b, s):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        combobox.setDisabled(False)
        b.setDisabled(True)
        s.setDisabled(True)
        rule = combobox.currentText()
        self.ruleChanged(rule)

    def setCustomRule(self, combobox, b, s):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        combobox.setDisabled(True)
        b.setDisabled(False)
        s.setDisabled(False)
        self.getCustomRule(b, s)

    def getCustomRule(self, b, s):
        b_rule = b.text()
        s_rule = s.text()
        self.ruleChanged("B{}/S{}".format(b_rule, s_rule))

    def ageChanged(self, s):
        def mappingToBool(v):
            if v > 0:
                return True
            else:
                return False

        def mappingFromBool(v):
            if v:
                return 1
            else:
                return 0

        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        if s:
            cells = np.vectorize(mappingFromBool)(self.view.universe.cells).astype(int)
            self.view.type = "GameOfLifeWithAge"
            self.view.initUniverse(cells=cells)
            self.view.initCellsView()
            self.view.redrawUniverse()
        else:
            cells = np.vectorize(mappingToBool)(self.view.universe.cells).astype(bool)
            self.view.type = "GameOfLife"
            self.view.initUniverse(cells=cells)
            self.view.initCellsView()
            self.view.redrawUniverse()

    def changeType(self):
        self.view.runEvo(False)
        self.btn_start.setChecked(False)
        self.selection_window.show()
        self.parent().close()
