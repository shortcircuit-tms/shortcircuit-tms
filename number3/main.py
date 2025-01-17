#
# Main code for number 3 robot
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom


INIT_TG_FLYWHEEL_VELOCITY = 100
INIT_BG_FLYWHEEL_VELOCITY = 60
FLYWHEEL_TORQUE = 100
INTAKE_VELOCITY = 100
INTAKE_TORQUE = 100
DRIVETRAIN_VELOCITY = 100
DRIVETRAIN_TORQUE = 100

flywheel_tg_velocity = INIT_TG_FLYWHEEL_VELOCITY
flywheel_bg_velocity = INIT_BG_FLYWHEEL_VELOCITY

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
FLYWHEEL_L_PORT = Ports.PORT6
FLYWHEEL_R_PORT = Ports.PORT12 
DRIVETRAIN_L_PORT = Ports.PORT5
DRIVETRAIN_R_PORT = Ports.PORT11
BOTTOM_INTAKE_PORT = Ports.PORT4
TOP_INTAKE_PORT = Ports.PORT10

# Brain should be defined by default
brain=Brain()
brain.screen.print("N3-MAIN\n")
brain.screen.next_row()
brain.screen.print("FW_R_L:12,6")
brain.screen.next_row()
brain.screen.print("DT_R_L:11,5")
brain.screen.next_row()
brain.screen.print("IT_T_B;10,4")

wait(10, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
flywheel_motor_R = Motor(FLYWHEEL_R_PORT, True)
flywheel_motor_L = Motor(FLYWHEEL_L_PORT, False)
flywheel = MotorGroup(flywheel_motor_R, flywheel_motor_L)
top_intake = Motor(TOP_INTAKE_PORT, False)
bottom_intake = Motor(BOTTOM_INTAKE_PORT, True)
drivetrain_motor_L = Motor(DRIVETRAIN_L_PORT, False)
drivetrain_motor_R = Motor(DRIVETRAIN_R_PORT, True)
drivetrain = DriveTrain(drivetrain_motor_L, drivetrain_motor_R, 319.19, 295, 40, MM, 1)


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
is_top_intake_on = False 
is_bottom_intake_on = False


def when_started():
    global launcher_speed, in_top_goal_mode, is_flywheel_on, flywheel_tg_velocity, flywheel_bg_velocity
    global top_intake, bottom_intake, is_top_intake_on, is_bottom_intake_on
    flywheel_tg_velocity = INIT_TG_FLYWHEEL_VELOCITY
    flywheel_bg_velocity = INIT_BG_FLYWHEEL_VELOCITY
    flywheel.set_max_torque(FLYWHEEL_TORQUE, PERCENT)
    flywheel.set_velocity(flywheel_tg_velocity, PERCENT)
    top_intake.set_max_torque(INTAKE_TORQUE, PERCENT)
    top_intake.set_velocity(INTAKE_VELOCITY, PERCENT)
    bottom_intake.set_max_torque(INTAKE_TORQUE, PERCENT)
    bottom_intake.set_velocity(INTAKE_VELOCITY, PERCENT)   
    in_top_goal_mode = True
    is_flywheel_on = False
    is_top_intake_on = False
    is_bottom_intake_on = False

def flywheel_on_off():
    global flywheel, is_flywheel_on
    if is_flywheel_on:
        flywheel.stop()
        is_flywheel_on = False
    else:
        flywheel.spin(FORWARD)
        is_flywheel_on = True

def flywheel_goal_select():
    global launcher_speed, in_top_goal_mode, flywheel_bg_velocity, flywheel_tg_velocity
    if in_top_goal_mode:
        flywheel.set_max_torque(FLYWHEEL_TORQUE, PERCENT)
        flywheel.set_velocity(flywheel_tg_velocity, PERCENT)
        in_top_goal_mode = False
    else:
        flywheel.set_max_torque(FLYWHEEL_TORQUE, PERCENT)
        flywheel.set_velocity(flywheel_bg_velocity, PERCENT)
        in_top_goal_mode = True

def top_intake_on_off():
    global top_intake, is_top_intake_on
    if is_top_intake_on:
        top_intake.stop()
        is_top_intake_on = False
    else:
        top_intake.spin(FORWARD)
        is_top_intake_on = True

def bottom_intake_on_off():
    global bottom_intake, is_bottom_intake_on
    if is_bottom_intake_on:
        bottom_intake.stop()
        is_bottom_intake_on = False
    else:
        bottom_intake.spin(FORWARD)
        is_bottom_intake_on = True

def incr_flywheel_tg_velocity():
    global flywheel_tg_velocity

    updated_tg_velocity = flywheel_tg_velocity + 10
    if updated_tg_velocity > 100:
        updated_tg_velocity = 100
    
    flywheel_tg_velocity = updated_tg_velocity

def decr_flywheel_tg_velocity():
    global flywheel_tg_velocity

    updated_tg_velocity = flywheel_tg_velocity - 10
    if updated_tg_velocity < 0:
        updated_tg_velocity = 0

    flywheel_tg_velocity = updated_tg_velocity

def incr_flywheel_bg_velocity():
    global flywheel_bg_velocity

    updated_bg_velocity = flywheel_bg_velocity + 10
    if updated_bg_velocity > 100:
        updated_bg_velocity = 100

        flywheel_bg_velocity = updated_bg_velocity

def decr_flywheel_bg_velocity():
    global flywheel_bg_velocity
    
    updated_bg_velocity = flywheel_bg_velocity - 10
    if updated_bg_velocity < 0:
        updated_bg_velocity = 0

        flywheel_bg_velocity = updated_bg_velocity

# system event handlers
controller.buttonLUp.pressed(flywheel_on_off) 
controller.buttonLDown.pressed(flywheel_goal_select)
controller.buttonRUp.pressed(bottom_intake_on_off)
controller.buttonRDown.pressed(top_intake_on_off)
controller.buttonEUp.pressed(incr_flywheel_bg_velocity)
controller.buttonEDown.pressed(decr_flywheel_bg_velocity)
controller.buttonFUp.pressed(incr_flywheel_tg_velocity)
controller.buttonFDown.pressed(decr_flywheel_tg_velocity)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started()