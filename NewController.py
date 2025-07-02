# Stepper motor controller for wet-spinning device - Rainey Lab- Dalhousie University
# Program enabling control of Tic T249 Stepper Motor Controllers from Polulu

import subprocess
import yaml
import threading

def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))



motorRPM: float = 5
isReverse: bool = False
step_type: int = 8
motors_on: bool = False

class Controller:
    def __init__(self, rpm, is_active, is_reverse, serial_number, stepper_name):
        self.rpm = rpm
        self.is_active = is_active
        self.is_reverse = is_reverse
        self.serial_number = serial_number
        self.stepper_name = stepper_name

controller_k1 = Controller(motorRPM, False, isReverse, "00392450", "Controller 'M1'")
controller_k2 = Controller(motorRPM, False, isReverse, "00392445", "Controller 'M2'")
controller_k3 = Controller(motorRPM, False, isReverse, "00391970", "Controller 'M3'")
controller_k4 = Controller(motorRPM, False, isReverse, "00392446", "Controller 'M4'")

controllers = [controller_k1, controller_k2, controller_k3, controller_k4]

for cont in controllers:
    status = yaml.safe_load(ticcmd('-d', cont.serial_number,'-s', '--full'))

def stop_motors():
    for cont in controllers:
        ticcmd('-d', cont.serial_number, '--deenergize')
        
        
def motor_thread(cont):
    while motors_on:
        if cont.is_active:
            # step_type can be: 1, 2, 4, 8, 16, 32, 64, 128, or 256. The higher the number the more steps per rotation, so the rotation should be smoother with higher values.
            #print("Setting step-mode to {}.".format(step_type))
            ticcmd('-d', cont.serial_number, '--step-mode', str(step_type))

            # velocity takes in direction through +/-, this essentially checks if motor should be rotated counter clockwise.
            cRPM: float = cont.rpm
            if cont.is_reverse == False:
                cRPM *= -1

            # target velocity is measured in steps per 10 000 seconds
            new_target: int = cRPM * 10000 / 60 * 180 * step_type
            #print("Setting target velocity to {}.".format(new_target))
            ticcmd('-d', cont.serial_number, '--exit-safe-start', '--velocity', str(int(new_target)))
            ticcmd('-d', cont.serial_number, '--energize')
            #print("energized")
        else:
            ticcmd('-d', cont.serial_number, '--deenergize')
            #print("deenergized")

def rotate_motors():
    for cont in controllers:
        x = threading.Thread(target=motor_thread, args=(cont,))
        x.start()
        

def refresh_the_motors():
    stop_motors()
    rotate_motors()
