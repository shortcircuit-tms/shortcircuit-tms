#
# Main code for number 3 robot
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom


INTAKE_VELOCITY = 100
INTAKE_TORQUE = 100
DRIVETRAIN_VELOCITY = 100
DRIVETRAIN_TORQUE = 100
DRIVETRAIN_TURN_VELOCITY = 45
CATAPULT_VELOCITY = 100
CATAPULT_TORQUE = 100
CONVEYOR_VELOCITY = 100
CONVEYOR_TORQUE = 100

AT_THE_GOAL_FRONT_S_DIST_TH = 30
AT_THE_GOAL_LEFT_S_DIST_TH = 500
AWAY_FROM_GOAL_FRONT_S_DIST_TH = 200 

FROM_GOAL_X_DISTANCE  = 1450
FROM_GOAL_X_ANGLE = 30
FROM_GOAL_I_DISTANCE = 1450
FROM_GOAL_MOVE_BACK = 250
X_PATH_VELOCITY_HIGH = 100
X_PATH_VELOCITY_LOW = 60
I_PATH_VELOCITY_HIGH = 100
I_PATH_VELOCITY_LOW = 97

CONVEYOR_INIT = 0
CONVEYOR_UNLOADING = 1
CONVEYOR_UNLOADED = 2
CONVEYOR_LOADING = 3
CONVEYOR_LOADED = 4

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
 
CONVEYER_L_PORT = Ports.PORT1
CATAPULT_PORT = Ports.PORT2
INTAKE_PORT = Ports.PORT4
CONVEYER_R_PORT = Ports.PORT5
OPTICAL_SENSOR_PORT = Ports.PORT6
RIGHT_DISTANCE_SENSOR_PORT = Ports.PORT7
CATAPULT_SENSOR_PORT = Ports.PORT8
DRIVETRAIN_L_PORT = Ports.PORT9
DRIVETRAIN_R_PORT = Ports.PORT10
FRONT_DISTANCE_SENSOR_PORT = Ports.PORT11
LEFT_DISTANCE_SENSOR_PORT = Ports.PORT12

# Brain should be defined by default
brain=Brain()
brain.screen.print("SH_N3: Teamwork\n")
brain.screen.next_row()
brain.screen.new_line()

wait(10, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
conveyor_motor_r = Motor(CONVEYER_R_PORT, False)
conveyor_motor_l = Motor(CONVEYER_L_PORT, True)
conveyor = MotorGroup(conveyor_motor_r, conveyor_motor_l)
intake_motor = Motor(INTAKE_PORT, True)
catapult_motor = Motor(CATAPULT_PORT, False)
catapult_sensor = Bumper(CATAPULT_SENSOR_PORT)
optical_sensor = Optical(OPTICAL_SENSOR_PORT)
front_distance = Distance(FRONT_DISTANCE_SENSOR_PORT)
left_distance = Distance(LEFT_DISTANCE_SENSOR_PORT)
#right_distance = Distance(RIGHT_DISTANCE_SENSOR_PORT)

# set up drivetrain
left_drive_smart = Motor(DRIVETRAIN_L_PORT, 1.0, False)
right_drive_smart = Motor(DRIVETRAIN_R_PORT, 1.0, True)
brain_inertial = Inertial()
drivetrain = SmartDrive(lm=left_drive_smart, rm=right_drive_smart, g=brain_inertial, wheelBase=200, externalGearRatio=2)

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
conveyer_state = CONVEYOR_INIT 
is_intake_on = False
is_catapult_loaded = False
is_catapult_on = False
at_the_goal = False
at_the_right_goal = False
at_the_left_goal = False
is_match_started = False
is_intake_forward = True
#If value is true, it's on the left, and if it's false, it's on the right

def when_started():
    global conveyor_state, conveyor
    global is_intake_on, intake_motor, is_intake_forward
    global is_catapult_on, catapult_motor, is_catapult_loaded
    global drivetrain_l_distance_sensor, drivetrain_r_distance_sensor
    global at_the_goal, at_the_left_goal, at_the_right_goal
    global from_goal_x_angle, from_goal_x_dist, from_goal_I_dist

    conveyor_state = CONVEYOR_INIT
    conveyor.set_max_torque(CONVEYOR_TORQUE, PERCENT)
    conveyor.set_velocity(CONVEYOR_VELOCITY, PERCENT)
    is_intake_on = False
    is_intake_forward = True
    intake_motor.set_max_torque(INTAKE_TORQUE, PERCENT)
    intake_motor.set_velocity(INTAKE_VELOCITY, PERCENT)
    is_catapult_on = False
    is_catapult_loaded = False
    catapult_motor.set_max_torque(CATAPULT_TORQUE, PERCENT)
    catapult_motor.set_velocity(CATAPULT_VELOCITY, PERCENT)
    catapult_motor.set_stopping(HOLD)
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)
    at_the_goal = False
    at_the_right_goal = False
    at_the_left_goal = False
    if not is_catapult_loaded:
        catapult_motor.spin(FORWARD)
        is_catapult_on = True
    wait(2000, MSEC)
    intake_motor.spin(FORWARD)
    wait(5000, MSEC)
    intake_motor.stop()


def conveyor_load():
    global conveyor, conveyor_state
    if conveyor_state == CONVEYOR_INIT or conveyor_state == CONVEYOR_UNLOADED or conveyor_state == CONVEYOR_UNLOADING:
        conveyor.spin(FORWARD)
        conveyor_state = CONVEYOR_LOADING

def conveyor_unload():
    global conveyor, conveyor_state
    if front_distance.object_distance() < AT_THE_GOAL_FRONT_S_DIST_TH:
        conveyor.spin(FORWARD)
        conveyor_state = CONVEYOR_UNLOADING

def conveyor_hold():
    global conveyor, conveyor_state
    if conveyor_state == CONVEYOR_LOADING:
        conveyor.stop()
        conveyor_state = CONVEYOR_LOADED       

def catapult_unload():
    global is_catapult_on, catapult_motor, at_the_goal
    global at_the_right_goal, at_the_left_goal

    if front_distance.object_distance() < AT_THE_GOAL_FRONT_S_DIST_TH:
        catapult_motor.spin(FORWARD)
        is_catapult_on = True
        at_the_goal = True
        if left_distance.object_distance() < AT_THE_GOAL_LEFT_S_DIST_TH:
            at_the_left_goal = True
        else:
            at_the_right_goal = True
        wait(1750, MSEC)
        conveyor_unload()

def ball_passed_through_conveyor():
    global at_the_goal, at_the_right_goal, at_the_left_goal
    if front_distance.object_distance() < AT_THE_GOAL_FRONT_S_DIST_TH:
        at_the_goal = True
        if left_distance.object_distance() < AT_THE_GOAL_LEFT_S_DIST_TH:
            at_the_left_goal = True
        else:
            at_the_right_goal = True

def away_from_goal():
    global at_the_goal, conveyor_state, at_the_right_goal, at_the_left_goal
    while True:
        if front_distance.object_distance() > AWAY_FROM_GOAL_FRONT_S_DIST_TH and at_the_goal:
            at_the_goal = False
            at_the_left_goal = False
            at_the_right_goal = False
            conveyor_state = CONVEYOR_LOADING

def catapult_bumper_pressed():
    global is_catapult_loaded, catapult_motor, is_catapult_on
    catapult_motor.stop()
    is_catapult_on = False
    is_catapult_loaded = True

def catapult_bumper_released():
    global is_catapult_loaded
    is_catapult_loaded = False

def intake_on_off():
    global is_intake_on, intake_motor
    if is_intake_on:
        intake_motor.stop()
        is_intake_on = False
    else:
        intake_motor.spin(FORWARD)
        is_intake_on = True

def toggle_intake_direction():
    global is_intake_forward
    
    if is_intake_forward:
        intake_motor.spin(REVERSE)
        is_intake_forward = False
    else:
        intake_motor.spin(FORWARD)
        is_intake_forward = True

def init_go_to_goal():
    left_drive_smart.spin(FORWARD, 100)
    right_drive_smart.spin(FORWARD, 100)
    wait(550, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()
    wait(500, MSEC)
    drivetrain.turn_for(direction=RIGHT,
                        angle=85,
                        units=DEGREES,
                        velocity=30,
                        units_v=PERCENT,
                        wait=True)
    wait(200, MSEC)
    left_drive_smart.spin(REVERSE, 100)
    right_drive_smart.spin(REVERSE, 100)
    wait(900, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()

def go_to_left_back_q():
    global at_the_right_goal, at_the_left_goal

    if at_the_left_goal == True:
        left_drive_smart.spin(FORWARD, I_PATH_VELOCITY_HIGH)
        right_drive_smart.spin(FORWARD, I_PATH_VELOCITY_LOW)
        wait(1600, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
        

    elif at_the_right_goal == True:
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        wait(900, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        wait(1000, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        wait(200, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        wait(100, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
    
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)


def go_to_right_back_q():
    global at_the_right_goal, at_the_left_goal

    if at_the_right_goal == True:
        left_drive_smart.spin(FORWARD, I_PATH_VELOCITY_LOW)
        right_drive_smart.spin(FORWARD, I_PATH_VELOCITY_HIGH)
        wait(1600, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop() 

    else:
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        wait(900, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        wait(1000, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_HIGH)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        wait(200, MSEC)
        left_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        right_drive_smart.spin(FORWARD, X_PATH_VELOCITY_LOW)
        wait(100, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
    
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)

        
 
## Strat of drivetrain code that was derived from VEX IQ
## Do not touch this code unless you know what you are doing
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
remote_control_code_enabled = False
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, remote_control_code_enabled
    global is_match_started
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
                is_match_started = True
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
                is_match_started = True
        # wait before repeating the process
        wait(20, MSEC)


# Calibrate the Drivetrain
calibrate_drivetrain()

## End of the drivetrain code

def conveyor_unload_no_check():

    global conveyor, conveyor_state
    conveyor.spin(FORWARD)
    conveyor_state  = CONVEYOR_LOADING

# system event handlers
controller.buttonLUp.pressed(catapult_unload)
#controller.buttonLDown.pressed()
controller.buttonLDown.pressed(toggle_intake_direction)
controller.buttonRUp.pressed(conveyor_unload)
controller.buttonRDown.pressed(conveyor_unload_no_check)
controller.buttonEUp.pressed(go_to_left_back_q)
controller.buttonEDown.pressed(go_to_right_back_q)
optical_sensor.object_detected(conveyor_hold)
catapult_sensor.pressed(catapult_bumper_pressed)
catapult_sensor.released(catapult_bumper_released)
optical_sensor.object_lost(ball_passed_through_conveyor)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started()

away_from_goal_thread = Thread(away_from_goal)
remote_control_code_enabled = True
rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

while not is_match_started:
    wait(20, MSEC)

intake_motor.spin(FORWARD)
is_intake_forward = True


# wait(60, SECONDS)

# remote_control_code_enabled = False
# drivetrain.stop()
# intake_motor.stop()
# conveyor.stop()
# catapult_motor.stop()

