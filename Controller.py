# Stepper motor controller for wet-spinning device - Rainey Lab- Dalhousie University
# Program enabling control of Adafruit DC & Stepper Motor HAT for Raspberry Pi

import board
import time
import atexit
import threading

from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit


# creating default objects
#kit1 = MotorKit(i2c=board.I2C(), address=0x60)
#kit2 = MotorKit(i2c=board.I2C(), address=0x61)
#kit3 = MotorKit(i2c=board.I2C(), address=0x62)
#kit4 = MotorKit(i2c=board.I2C(), address=0x63)
kit5 = MotorKit(i2c=board.I2C(), address=0x64)
kit6 = MotorKit(i2c=board.I2C(), address=0x65)


motors_on: bool = True
motors_forward: bool = True
motors_RPM: float = 5
motors_RPM_calibrated: float = 5.8


class SingleMotor:
    def __init__(self, RPM, calibrated_RPM, isActive, isForward, motor_kit, thread, stepper_name):
        self.RPM = RPM
        self.calibrated_RPM = calibrated_RPM
        self.isActive = isActive
        self.isForward = isForward
        self.motor_kit = motor_kit
        self.thread = thread
        self.stepper_name = stepper_name


#motor_c1 = SingleMotor(motors_RPM, motors_RPM_calibrated, False, motors_forward, kit1, threading.Thread(),
 #                 "Motor c1 'M1'")
#motor_c2 = SingleMotor(motors_RPM, motors_RPM_calibrated, False, motors_forward, kit2, threading.Thread(),
 #                 "Motor c2 'M2'")
motor_c3 = SingleMotor(motors_RPM, motors_RPM_calibrated, False, motors_forward, kit5, threading.Thread(),
                  "Hat 'M5'")
motor_c4 = SingleMotor(motors_RPM, motors_RPM_calibrated, False, motors_forward, kit6, threading.Thread(),
                  "Hat 'M6'")
# motor_c5 = SingleMotor(motors_RPM, motors_RPM_calibrated, True, motors_forward, kit5, threading.Thread(),
#                  "Motor c5")
# motor_c6 = SingleMotor(motors_RPM, motors_RPM_calibrated, True, motors_forward, kit6, threading.Thread(),
#                  "Motor c6")

motors = [motor_c3, motor_c4]


def turnOffMotors():
    print("releasing motors\n")
    for stmotor in motors:
        stmotor.motor_kit.stepper1.release()
        stmotor.motor_kit.stepper2.release()


def exit_script():
    global motors_on
    motors_on = False
    turnOffMotors()
    print("exiting")
    raise SystemExit(0)


# atexit.register(exit_script)


def stepper_worker(motor_kit, RPM, display_RPM, direction, direction_str, stepper_name):
    print(stepper_name + "  " + str(display_RPM) + direction_str)
    while motors_on:
        stepsize: float = 0.9
        delaytime: float = 60 / ((360 / stepsize) * RPM)
        motor_kit.stepper1.onestep(direction=direction, style=STEPPER.INTERLEAVE)
        motor_kit.stepper2.onestep(direction=direction, style=STEPPER.INTERLEAVE)
        time.sleep(delaytime)


def start_motors():
    print("\nSTARTING MOTORS")
    for smotor in motors:
        if smotor.isActive:
            if not smotor.thread.is_alive():
                if smotor.isForward:
                    stepperdir = STEPPER.FORWARD
                    stepper_dir_str = "  CLOCKWISE"
                else:
                    stepperdir = STEPPER.BACKWARD
                    stepper_dir_str = "  COUNTERCLOCKWISE"
                smotor.thread.thread = threading.Thread(
                    target=stepper_worker,
                    args=(
                        smotor.motor_kit,
                        smotor.calibrated_RPM,
                        smotor.RPM,
                        stepperdir,
                        stepper_dir_str,
                        smotor.stepper_name
                    )
                )
                # smotor.thread.thread.daemon = True  # Dies when main thread dies
                smotor.thread.thread.start()


def refresh_motors():
    turnOffMotors()
    start_motors()
