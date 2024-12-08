#
# This code is to set up the flywheels independently
#
# The position from the goal base is : XXXX
#
# The speeds for top and bottom goals are:
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom

TOP_GOAL_VELOCITY = 100
BOTTOM_GOAL_VELOCITY = 100

# Brain should be defined by default
brain=Brain()
brain.screen.print("Starting FW")
wait(1000, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
Ball_Launcher_motor_a = Motor(Ports.PORT6, True)
Ball_Launcher_motor_b = Motor(Ports.PORT12, False)
Ball_Launcher = MotorGroup(Ball_Launcher_motor_a, Ball_Launcher_motor_b)



# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime))

# Initialize random seed
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration

myVariable = 0
launcher_speed = 0

def when_started1():
    global myVariable, launcher_speed
    Ball_Launcher.set_max_torque(100, PERCENT)
    Ball_Launcher.set_velocity(TOP_GOAL_VELOCITY, PERCENT)

def onevent_controllerbuttonLUp_pressed_0():
    global myVariable, launcher_speed
    Ball_Launcher.stop()

def onevent_controllerbuttonLDown_pressed_0():
    global myVariable, launcher_speed
    Ball_Launcher.spin(FORWARD)

# system event handlers
controller.buttonLUp.pressed(onevent_controllerbuttonLUp_pressed_0)
controller.buttonLDown.pressed(onevent_controllerbuttonLDown_pressed_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()