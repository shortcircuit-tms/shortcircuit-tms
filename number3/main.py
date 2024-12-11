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
BALL_LAUNCHER_L_PORT = Ports.PORT6
BALL_LAUNCHER_R_PORT = Ports.PORT12

# Brain should be defined by default
brain=Brain()
brain.screen.print("Starting FW")
wait(1000, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
Ball_Launcher_motor_R = Motor(BALL_LAUNCHER_R_PORT, True)
Ball_Launcher_motor_L = Motor(BALL_LAUNCHER_L_PORT, False)
Ball_Launcher = MotorGroup(Ball_Launcher_motor_R, Ball_Launcher_motor_L)

Intake_motor = Motor(Ports.PORT1, True)

Drivetrain_motor_a = Motor(Ports.PORT5, True)
Drivetrain_motor_b = Motor(Ports.PORT7, True)
Drivetrain = MotorGroup(Drivetrain_motor_a,Drivetrain_motor_b)


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

def when_started1():
    global myVariable, launcher_speed, in_top_goal_mode, is_flywheel_on
    Ball_Launcher.set_max_torque(TOP_GOAL_TORQUE, PERCENT)
    Ball_Launcher.set_velocity(TOP_GOAL_VELOCITY, PERCENT)
    in_top_goal_mode = True
    is_flywheel_on = False


def flywheel_on_off():
    global myVariable, launcher_speed, is_flywheel_on
    if is_flywheel_on:
        Ball_Launcher.stop()
        is_flywheel_on = False
    else:
        Ball_Launcher.spin(FORWARD)
        is_flywheel_on = True

def fly_wheel_goal_select():
    global myVariable, launcher_speed, in_top_goal_mode
    if in_top_goal_mode:
        Ball_Launcher.set_max_torque(BOTTOM_GOAL_TORQUE, PERCENT)
        Ball_Launcher.set_velocity(BOTTOM_GOAL_VELOCITY, PERCENT)
        in_top_goal_mode = False
    else:
        Ball_Launcher.set_max_torque(TOP_GOAL_TORQUE, PERCENT)
        Ball_Launcher.set_velocity(TOP_GOAL_VELOCITY, PERCENT)
        in_top_goal_mode = True

def onevent_controllerbuttonLUp_pressed_0():
    global myVariable, launcher_speed
    Ball_Launcher.spin(FORWARD)

def onevent_controllerbuttonLDown_pressed_0():
    pass

# system event handlers
controller.buttonLUp.pressed(onevent_controllerbuttonLUp_pressed_0)
controller.buttonLDown.pressed(onevent_controllerbuttonLDown_pressed_0)
controller.buttonRUp.pressed(flywheel_on_off)
controller.buttonRDown.pressed(fly_wheel_goal_select)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()