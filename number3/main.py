#
# Main code for number 3 robot
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom


TOP_GOAL_VELOCITY = 100
TOP_GOAL_TORQUE = 100
BOTTOM_GOAL_VELOCITY = 20
BOTTOM_GOAL_TORQUE = 20

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
FLYWHEEL_L_PORT = Ports.PORT6
FLYWHEEL_R_PORT = Ports.PORT12
INTAKE_PORT = Ports.PORT5
DRIVETRAIN_R_PORT = Ports.PORT7
DRIVETRAIN_L_PORT = Ports.PORT1

# Brain should be defined by default
brain=Brain()
brain.screen.print("N3-MAIN\n")
brain.screen.next_row()
brain.screen.print("FW_R_L:12,6")
brain.screen.next_row()
brain.screen.print("IT:5")
brain.screen.next_row()
brain.screen.print("DT_R_L:7,1")


wait(10, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
flywheel_motor_R = Motor(FLYWHEEL_R_PORT, True)
flywheel_motor_L = Motor(FLYWHEEL_L_PORT, False)
flywheel = MotorGroup(flywheel_motor_R, flywheel_motor_L)

intake = Motor(INTAKE_PORT, True)

Drivetrain_motor_L = Motor(DRIVETRAIN_L_PORT, True)
Drivetrain_motor_R = Motor(DRIVETRAIN_R_PORT, True)
Drivetrain = MotorGroup(Drivetrain_motor_R, Drivetrain_motor_L)


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
in_top_goal_mode = True
is_flywheel_on = False
is_intake_on = False

def when_started1():
    global myVariable, launcher_speed, in_top_goal_mode, is_flywheel_on, is_intake_on
    flywheel.set_max_torque(TOP_GOAL_TORQUE, PERCENT)
    flywheel.set_velocity(TOP_GOAL_VELOCITY, PERCENT)
    in_top_goal_mode = True
    is_flywheel_on = False
    is_intake_on = False


def flywheel_on_off():
    global myVariable, launcher_speed, is_flywheel_on
    if is_flywheel_on:
        flywheel.stop()
        is_flywheel_on = False
    else:
        flywheel.spin(FORWARD)
        is_flywheel_on = True

def flywheel_goal_select():
    global myVariable, launcher_speed, in_top_goal_mode
    if in_top_goal_mode:
        flywheel.set_max_torque(BOTTOM_GOAL_TORQUE, PERCENT)
        flywheel.set_velocity(BOTTOM_GOAL_VELOCITY, PERCENT)
        in_top_goal_mode = False
    else:
        flywheel.set_max_torque(TOP_GOAL_TORQUE, PERCENT)
        flywheel.set_velocity(TOP_GOAL_VELOCITY, PERCENT)
        in_top_goal_mode = True

def onevent_controllerbuttonLUp_pressed_0():
    global myVariable, launcher_speed
    flywheel.spin(FORWARD)

def intake_on_off():
    global intake, is_intake_on
    if is_intake_on:
        intake.stop()
        is_intake_on = False 
    else:
        intake.spin(FORWARD)
        is_intake_on = True


def onevent_controllerbuttonLDown_pressed_0():
    pass

# system event handlers
controller.buttonLUp.pressed(intake_on_off)
controller.buttonLDown.pressed(onevent_controllerbuttonLDown_pressed_0)
controller.buttonRUp.pressed(flywheel_on_off)
controller.buttonRDown.pressed(flywheel_goal_select)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()