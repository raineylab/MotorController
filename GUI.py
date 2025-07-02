# GUI for Stepper Motor Controller for wet-spinning device - Rainey Lab - Dalhousie University
# Controls up to 6 stepper motors in terms of both speed and direction
# See readme for exact stepper motor controller configuration
# Motor control requires Controller.py and/or NewController.py plus associated motor 
# controller specific-dependencies as detailed in readme
# GUI uses PyQt5, freely available from pypi.org

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout, QComboBox, QTabWidget, \
    QLineEdit, QInputDialog

import sys
import Controller # Used for motors controlled by Adafruit DC & Stepper Motor HAT for Raspberry Pi (speed limited)
import NewController # Used for motors controlled by Tic T249 Stepper Motor Controllers from Polulu

current_motor: Controller.SingleMotor

GUI_to_lock = []
GUI_to_change = []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pb_is_checked = True

        self.setWindowTitle("Motor Controller")

        tabs = QTabWidget()

        count: int = 0

        class ContClass:
            def __init__(self, name, is_new):
                self.name = name
                self.is_new = is_new

        cont_names = []

        for cont in NewController.controllers:
            cont_names.append(ContClass(cont.stepper_name, True))

        for smotor in Controller.motors:
            cont_names.append(ContClass(smotor.stepper_name, False))

        for conts in cont_names:
            layout = QWidget()
            layout.layout = QGridLayout()

            self.isNew = conts.is_new

            self.power_button = QPushButton("Motors Off")
            GUI_to_change.append(self.power_button)
            self.power_button.setCheckable(True)

            self.power_button.clicked.connect(self.pb_toggled)
            self.power_button.setChecked(self.pb_is_checked)

            self.dir_label = QLabel("Motor direction")

            self.dir_is_checked = True

            self.dir_button = QPushButton("Clockwise")
            self.dir_button.setObjectName(str(count))
            GUI_to_lock.append(self.dir_button)
            self.dir_button.setCheckable(True)
            self.dir_button.clicked.connect(self.dir_toggled)
            self.dir_button.setChecked(self.dir_is_checked)

            self.activity_label = QLabel("Motor power")

            self.isActive_is_checked = False

            self.activity_button = QPushButton("Inactive")
            self.activity_button.setObjectName(str(count))
            GUI_to_lock.append(self.activity_button)
            self.activity_button.setCheckable(True)
            self.activity_button.clicked.connect(self.activity_toggled)
            self.activity_button.setChecked(self.isActive_is_checked)

            self.RPM_label = QLabel("Motor RPM")

            self.RPM_text = QComboBox()
            self.RPM_text.setObjectName(str(count))
            GUI_to_lock.append(self.RPM_text)
            if conts.is_new:
                self.RPM_text.addItems(
                    ["1: RPM 5", "2: RPM 6", "3: RPM 9", "4: RPM 18", "5: RPM 20", "6: RPM 23", "7: RPM 26",
                    "8: RPM 30", "9: RPM 37", "10: RPM 46", "11: RPM 60", "12: RPM 90"])
            else:
                self.RPM_text.addItems(
                    ["1: RPM 5", "2: RPM 6", "3: RPM 9", "4: RPM 18", "5: RPM 20", "6: RPM 23", "7: RPM 26",
                    "8: RPM 30", "9: RPM 37", "10: RPM 46", "11: RPM 60 Not Calibrated", "12: RPM 90 Not Calibrated"])

            self.RPM_text.currentIndexChanged.connect(self.RPM_changed)

            self.RPM_custom_text = QPushButton("Custom")
            self.RPM_custom_text.setObjectName(str(count))
            GUI_to_lock.append(self.RPM_custom_text)
            self.RPM_custom_text.clicked.connect(self.RPM_custom_changed)

            layout.layout.addWidget(self.power_button, 0, 0)
            layout.layout.addWidget(self.dir_label, 1, 0)
            layout.layout.addWidget(self.dir_button, 1, 1)
            layout.layout.addWidget(self.RPM_label, 2, 0)
            layout.layout.addWidget(self.RPM_text, 2, 1)
            layout.layout.addWidget(self.RPM_custom_text, 2, 2)
            layout.layout.addWidget(self.activity_label, 3, 0)
            layout.layout.addWidget(self.activity_button, 3, 1)
            layout.setLayout(layout.layout)
            tabs.addTab(layout, conts.name)

            count += 1

        # Set the central widget of the Window.
        self.setCentralWidget(tabs)

    def enable_buttons(self):
        for GUI_element in GUI_to_lock:
            GUI_element.setEnabled(True)

    def disable_buttons(self):
        for GUI_element in GUI_to_lock:
            GUI_element.setDisabled(True)

    def pb_toggled(self, checked):
        self.pb_is_checked = checked
        if self.pb_is_checked:
            for GUI_stuff in GUI_to_change:
                GUI_stuff.setText("Motors Off")
                GUI_stuff.setStyleSheet("background-color: white")
                GUI_stuff.setChecked(self.pb_is_checked)
                self.enable_buttons()
            NewController.motors_on = False
            NewController.stop_motors()
            Controller.turnOffMotors()
            Controller.motors_on = False
        else:
            for GUI_stuff in GUI_to_change:
                GUI_stuff.setText("Motors On")
                GUI_stuff.setStyleSheet("background-color:#ECFFC7;")
                GUI_stuff.setChecked(self.pb_is_checked)
                self.disable_buttons()
            NewController.motors_on = True
            NewController.rotate_motors()
            Controller.motors_on = True
            Controller.refresh_motors()

    def dir_toggled(self, checked):
        self.dir_is_checked = checked
        sending_button = self.sender()
        motor_int = int(sending_button.objectName())
        motor_calc_int = motor_int - 4

        if self.dir_is_checked:
            sending_button.setText("Clockwise")
            if motor_int < len(NewController.controllers):
                print(NewController.controllers[motor_int].stepper_name + " direction set to Clockwise")
                NewController.controllers[motor_int].is_reverse = False
            else:
                print(Controller.motors[motor_calc_int].stepper_name + " direction set to Clockwise")
                Controller.motors[motor_calc_int].isForward = True
        else:
            sending_button.setText("Counterclockwise")
            if motor_int < len(NewController.controllers):
                print(NewController.controllers[motor_int].stepper_name + " direction set to Counterclockwise")
                NewController.controllers[motor_int].is_reverse = True
            else:
                print(Controller.motors[motor_calc_int].stepper_name + " direction set to Counterclockwise")
                Controller.motors[motor_calc_int].isForward = False

    def activity_toggled(self, checked):
        self.isActive_is_checked = checked
        sending_button = self.sender()
        motor_int = int(sending_button.objectName())
        motor_calc_int = motor_int - 4

        if self.isActive_is_checked:
            sending_button.setText("Active")
            if motor_int < len(NewController.controllers):
                print(NewController.controllers[motor_int].stepper_name + " is active")
                NewController.controllers[motor_int].is_active = True
            else:
                print(Controller.motors[motor_calc_int].stepper_name + " is active")
                Controller.motors[motor_calc_int].isActive = True
        else:
            sending_button.setText("Inactive")
            if motor_int < len(NewController.controllers):
                print(NewController.controllers[motor_int].stepper_name + " is inactive")
                NewController.controllers[motor_int].is_active = False
            else:
                print(Controller.motors[motor_calc_int].stepper_name + " is inactive")
                Controller.motors[motor_calc_int].isActive = False

    def RPM_changed(self, i):
        sending_button = self.sender()
        RPM_list = [5, 6, 9, 18, 20, 23, 26, 30, 37, 46, 60, 90]
        RPM_calibrated_list = [5.8, 6.9, 11.1, 30.8, 37, 43, 60, 90, 140, 290, 60, 90]
        motor_int = int(sending_button.objectName())
        motor_calc_int = motor_int - 4

        if motor_int < len(NewController.controllers):
            print(NewController.controllers[motor_int].stepper_name + " RPM set to " + str(RPM_list[i]))
            NewController.controllers[motor_int].rpm = float(RPM_list[i])
        else:
            print(Controller.motors[motor_calc_int].stepper_name + " RPM set to " + str(RPM_list[i]))
            Controller.motors[motor_calc_int].RPM = float(RPM_list[i])
            Controller.motors[motor_calc_int].calibrated_RPM = float(RPM_calibrated_list[i])
    def RPM_custom_changed(self):
        sending_button = self.sender()
        rpm_value, ok = QInputDialog.getDouble(self,
                                                'Custom RPM',
                                                'Set Custom RPM',
                                                0,
                                                0,
                                                500,
                                                2)
        rpm: float = 1
        if ok and rpm_value:
            sending_button.setText("Custom RPM: " + str(rpm_value))
            rpm = rpm_value

        motor_int = int(sending_button.objectName())
        motor_calc_int = motor_int - 4
        if motor_int < len(NewController.controllers):
            print(NewController.controllers[motor_int].stepper_name + " RPM set to " + str(rpm))
            NewController.controllers[motor_int].rpm = rpm
        else:
            print(Controller.motors[motor_calc_int].stepper_name + " RPM set to " + str(rpm))
            Controller.motors[motor_calc_int].RPM = rpm
            Controller.motors[motor_calc_int].calibrated_RPM = rpm


app = QApplication(sys.argv)

window = MainWindow()
window.resize(1000, 400)
window.show()

app.exec()

Controller.exit_script()
