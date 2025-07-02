# MotorController
Python code for graphical user interface (GUI) for wet-spinning device
From Jan Rainey's lab at Dalhouise University
Coding: Donovan Rainey (summer 2024)

This is a GUI for an automated protein wet-spinning device that is configured to
enable both speed and directional control of up to 6 stepper motors. The GUI
is configured to use the Tic T249 Stepper Motor Controllers from Polulu for Motors #1-4
and the DC & Stepper Motor HAT for Raspberry Pi from Adafruit for Motors #5-6

Note: the DC & Stepper Motor HAT for Raspberry Pi from Adafruit controller is limited in maximum rotation
rate achievable, in our hands being accurate and useable up to ~46 rpm

Dependencies:
Requires ticcmd command line tool from Polulu and the Adafruit motor and motorkit (available as part of
the Adafruit library and driver bundle) - both are available through GitHub
