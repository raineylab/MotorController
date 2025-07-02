# MotorController
Python code for wet-spinning device stepper motor controller

This GUI is configured to control Motors 1-4 Tic T249 Stepper Motor Controllers from Polulu
and Motors 5-6 using DC & Stepper Motor HAT for Raspberry Pi from Adafruit

Requires ticcmd command line tool from Polulu and the Adafruit motor and motorkit (available as part of
the Adafruit library and driver bundle). 

Note: the DC & Stepper Motor HAT for Raspberry Pi from Adafruit controller is limited in maximum rotation
rate achievable, in our hands being accurate and useable up to ~46 rpm
