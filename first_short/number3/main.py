#
# Main code for number 3 robot
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom


INIT_TG_FLYWHEEL_VELOCITY = 100
INIT_BG_FLYWHEEL_VELOCITY = 34
FLYWHEEL_TORQUE = 100
INTAKE_VELOCITY = 100
INTAKE_TORQUE = 100
DRIVETRAIN_VELOCITY = 100
DRIVETRAIN_TORQUE = 100
column_number = 1

flywheel_tg_velocity = INIT_TG_FLYWHEEL_VELOCITY
flywheel_bg_velocity = INIT_BG_FLYWHEEL_VELOCITY

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
FLYWHEEL_L_PORT = Ports.PORT3
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
brain.screen.new_line()

wait(10, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
flywheel_motor_R = Motor(FLYWHEEL_R_PORT, True)
flywheel_motor_L = Motor(FLYWHEEL_L_PORT, False)
flywheel = MotorGroup(flywheel_motor_R, flywheel_motor_L)
top_intake = Motor(TOP_INTAKE_PORT, False)
bottom_intake = Motor(BOTTOM_INTAKE_PORT, True)

# set up drivetrain
left_drive_smart = Motor(DRIVETRAIN_L_PORT, 1.0, False)
right_drive_smart = Motor(DRIVETRAIN_R_PORT, 1.0, True)
brain_inertial = Inertial()
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 250)


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
    global launcher_speed, in_top_goal_mode, is_flywheel_on, flywheel_tg_velocity, flywheel_bg_velocity, column_number
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

    updated_tg_velocity = flywheel_tg_velocity + 2
    if updated_tg_velocity > 100:
        updated_tg_velocity = 100
    
    flywheel_tg_velocity = updated_tg_velocity
    print_flywheel_veocity()    


def decr_flywheel_tg_velocity():
    global flywheel_tg_velocity

    updated_tg_velocity = flywheel_tg_velocity - 2
    if updated_tg_velocity < 0:
        updated_tg_velocity = 0

    flywheel_tg_velocity = updated_tg_velocity
    print_flywheel_veocity()    

def incr_flywheel_bg_velocity():
    global flywheel_bg_velocity

    updated_bg_velocity = flywheel_bg_velocity + 2
    if updated_bg_velocity > 100:
        updated_bg_velocity = 100

    flywheel_bg_velocity = updated_bg_velocity
    print_flywheel_veocity()    

def decr_flywheel_bg_velocity():
    global flywheel_bg_velocity
    
    updated_bg_velocity = flywheel_bg_velocity - 2
    if updated_bg_velocity < 0:
        updated_bg_velocity = 0

    flywheel_bg_velocity = updated_bg_velocity
    print_flywheel_veocity()    

def print_row(text, row_number, delete_row_before_print=True):
    if delete_row_before_print:
        brain.screen.clear_row(row_number)
    brain.screen.set_cursor(row_number, 1)
    brain.screen.print(text)
                       
def print_flywheel_veocity():
    global flywheel_tg_velocity, flywheel_bg_velocity
    text = "FWV_T_B=" + str(flywheel_tg_velocity) + "," + str(flywheel_bg_velocity)
    print_row(text=text, row_number=5)

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axisA
            # right = axisD
            drivetrain_left_side_speed = controller.axisA.position()
            drivetrain_right_side_speed = controller.axisD.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# Calibrate the Drivetrain
calibrate_drivetrain()

# system event handlers
controller.buttonLUp.pressed(flywheel_on_off) 
controller.buttonLDown.pressed(flywheel_goal_select)
controller.buttonRUp.pressed(bottom_intake_on_off)
controller.buttonRDown.pressed(top_intake_on_off)
controller.buttonFUp.pressed(incr_flywheel_bg_velocity)
controller.buttonFDown.pressed(decr_flywheel_bg_velocity)
controller.buttonEUp.pressed(incr_flywheel_tg_velocity)
controller.buttonEDown.pressed(decr_flywheel_tg_velocity)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started()
remote_control_code_enabled = True
rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

