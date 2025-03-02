#
# Main code for number 3 robot
# 

#region VEXcode Generated Robot Configuration
from vex import *
import urandom


INTAKE_VELOCITY = 75
INTAKE_TORQUE = 100
DRIVETRAIN_VELOCITY = 100
DRIVETRAIN_TORQUE = 100
DRIVETRAIN_TURN_VELOCITY = 45
CATAPULT_VELOCITY = 100
CATAPULT_TORQUE = 100
CONVEYOR_VELOCITY = 100
CONVEYOR_TORQUE = 100

CONVEYOR_INIT = 0
CONVEYOR_UNLOADING = 1
CONVEYOR_LOADING = 2
CONVEYOR_LOADED = 3

DRIVE_MAX_VELOCITY = 100
START_TURN_ANGLE = 25
START_FORWARD_DIST = 34
START_LOAD_DIST = 6
START_TO_I_GOAL_ANGLE = 124
START_TO_I_GOAL_DIST = 34
BALL_PICKUP_ZONE_DISTANCE = 28
BALL_PICKUP_ZONE_VELOCITY = 100
BALL_PICKUP_LOAD_DISTACE = 14
BALL_PICKUP_LOAD_VELOCITY = 40
RETURN_TO_I_GOAL_DISTANCE = BALL_PICKUP_ZONE_DISTANCE + BALL_PICKUP_LOAD_DISTACE + 4
RETURN_TO_I_GOAL_VELOCITY = 100
ADJUST_TO_GOAL_TIME_1 = 300
ADJUST_TO_GOAL_TIME_2 = 200
ADJUST_TO_GOAL_VELOCITY = 85
X_GOAL_ANGLE = 40
RETURN_TO_X_GOAL_VELOCITY = 100
RETURN_TO_X_GOAL_DISTANCE = 32

CONVEYOR_TOP_UNLOAD_TIME = 750
CONVEYOR_BOTTOM_UNLOAD_TIME = 1500
CATAPULT_WAIT_TIME = 500
LEFT_WHEEL_SCALE_DOWN = 0.965

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
 
CONVEYOR_L_PORT = Ports.PORT1
CATAPULT_OPTICAL_SENSOR_PORT = Ports.PORT3
CATAPULT_PORT = Ports.PORT2
INTAKE_PORT = Ports.PORT4
CONVEYOR_R_PORT = Ports.PORT5
OPTICAL_SENSOR_PORT = Ports.PORT6
DRIVETRAIN_L_PORT = Ports.PORT9
DRIVETRAIN_R_PORT = Ports.PORT10
DISTANCE_SENSOR_PORT = Ports.PORT11

# Brain should be defined by default
brain=Brain()
brain.screen.print("SH_N3: Auton\n")
brain.screen.next_row()
brain.screen.new_line()

wait(10, MSEC)

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
conveyor_motor_r = Motor(CONVEYOR_R_PORT, False)
conveyor_motor_l = Motor(CONVEYOR_L_PORT, True)
conveyor = MotorGroup(conveyor_motor_r, conveyor_motor_l)
intake_motor = Motor(INTAKE_PORT, True)
catapult_motor = Motor(CATAPULT_PORT, False)
catapult_sensor = Optical(CATAPULT_OPTICAL_SENSOR_PORT)
optical_sensor = Optical(OPTICAL_SENSOR_PORT)

# set up drivetrain
left_drive_smart = Motor(DRIVETRAIN_L_PORT, 1, False)
right_drive_smart = Motor(DRIVETRAIN_R_PORT, 1, True)
brain_inertial = Inertial()
drivetrain = SmartDrive(lm=left_drive_smart, rm=right_drive_smart, g=brain_inertial, wheelTravel=200, trackWidth=200, wheelBase=200, externalGearRatio=2)


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

## Caliberation and calculation for time based distance
dist_calib_data = [[0, 0, 0],
                    [250, 4.75, 0],
                    [375, 9.5, 0],
                    [500, 14.5, 0],
                    [625, 18.5, 0],
                    [750, 22.5, 0],
                    [875, 26, 0],
                    [1000, 29, 0],
                    [1125, 31.75, 0],
                    [1250, 34.25, 0]]

for i in range(0,len(dist_calib_data)-1):
    y1, x1, m1 = dist_calib_data[i+1]
    y0, x0, m0 = dist_calib_data[i]
    m0 = (y1-y0)/(x1-x0)
    dist_calib_data[i][2] = m0
    
dist_calib_data[len(dist_calib_data)-1][2] = dist_calib_data[len(dist_calib_data)-2][2]

def get_drive_time_for_distance(distance):
    drive_time = 0
    for y0, x0, m in dist_calib_data:
        if distance < x0:
            break
        else:
            drive_time = y0 + (distance-x0)*m
    return drive_time

def drive_staight(direction, distance, velocity, use_smart_drive = False, do_wait=True):
    if use_smart_drive:
        drivetrain.drive_for(direction=direction,
                             distance=distance,
                             units=INCHES,
                             velocity=velocity,
                             units_v=PERCENT,
                             wait=do_wait)
    else:
        corrected_distance = distance
        if direction is FORWARD:
            corrected_distance = distance + 0.5
        driving_time = get_drive_time_for_distance(corrected_distance)
        left_drive_smart.spin(direction, velocity*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(direction, velocity)
        wait(int(driving_time), MSEC)
        pid_stop()

def adjust_to_goal_f():
    left_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    right_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    wait(int(ADJUST_TO_GOAL_TIME_1), MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()
    left_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    right_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    wait(int(ADJUST_TO_GOAL_TIME_2), MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()

def adjust_to_goal_r():
    left_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    right_drive_smart.spin(REVERSE, ADJUST_TO_GOAL_VELOCITY)
    wait(int(ADJUST_TO_GOAL_TIME_1), MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()

myVariable = 0
launcher_speed = 0
conveyor_state = CONVEYOR_LOADED 
is_intake_on = False
is_catapult_loaded = False
is_catapult_on = False
start_auton = False
stop_auton = False

def pid_stop():
    done = False
    while not done:
        right_motor_velocity = right_drive_smart.velocity(PERCENT)
        if right_motor_velocity < -10:
            new_right_motor_velocity = right_motor_velocity + 10
        elif right_motor_velocity > 10:
            new_right_motor_velocity = right_motor_velocity - 10
        else:
            new_right_motor_velocity = 0
            done = True
        
        new_left_motor_velocity = new_right_motor_velocity * LEFT_WHEEL_SCALE_DOWN
        left_drive_smart.set_velocity(new_left_motor_velocity, PERCENT)
        right_drive_smart.set_velocity(new_right_motor_velocity, PERCENT)

        wait(20, MSEC)

def when_started():
    global conveyor_state, conveyor
    global is_intake_on, intake_motor
    global is_catapult_on, catapult_motor, is_catapult_loaded
    global start_auton, stop_auton

    conveyor_state = CONVEYOR_LOADED
    conveyor.set_max_torque(CONVEYOR_TORQUE, PERCENT)
    conveyor.set_velocity(CONVEYOR_VELOCITY, PERCENT)
    is_intake_on = False
    intake_motor.set_max_torque(INTAKE_TORQUE, PERCENT)
    intake_motor.set_velocity(INTAKE_VELOCITY, PERCENT)
    is_catapult_on = False
    is_catapult_loaded = False
    catapult_motor.set_max_torque(CATAPULT_TORQUE, PERCENT)
    catapult_motor.set_velocity(CATAPULT_VELOCITY, PERCENT)
    catapult_motor.set_stopping(HOLD)
    left_drive_smart.set_stopping(BRAKE)
    right_drive_smart.set_stopping(BRAKE)
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)
    drivetrain.set_drive_velocity(DRIVETRAIN_VELOCITY, PERCENT)
    start_auton = False
    stop_auton = False
    if not is_catapult_loaded:
        catapult_button_on_off()
    wait(2000, MSEC)
    intake_motor.spin(FORWARD)
    wait(1000, MSEC)
    intake_motor.stop()

def conveyor_load():
    global conveyor, conveyor_state
    if conveyor_state == CONVEYOR_INIT or conveyor_state == CONVEYOR_UNLOADING:
        conveyor.spin(FORWARD)
        conveyor_state = CONVEYOR_LOADING

def conveyor_unload():
    global conveyor, conveyor_state
    if  conveyor_state == CONVEYOR_LOADED:
        conveyor.spin(FORWARD)
        conveyor_state = CONVEYOR_UNLOADING

def conveyor_hold():
    global conveyor, conveyor_state
    if conveyor_state == CONVEYOR_LOADING:
        conveyor.stop()
        conveyor_state = CONVEYOR_LOADED       

def catapult_button_on_off():
    global is_catapult_on, catapult_motor
    if is_catapult_on:
        catapult_motor.stop()
        is_catapult_on = False
    else:
        catapult_motor.spin(FORWARD)
        is_catapult_on = True

def catapult_lowered():
    global is_catapult_loaded, catapult_motor, is_catapult_on
    catapult_motor.stop()
    is_catapult_on = False
    is_catapult_loaded = True

def catapult_released():
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

def go_back_and_load():
    drive_staight(direction=FORWARD, 
                  distance=BALL_PICKUP_ZONE_DISTANCE, 
                  velocity=BALL_PICKUP_ZONE_VELOCITY, 
                  use_smart_drive = True,
                  do_wait=True)
    conveyor_load()
    drive_staight(direction=FORWARD, 
                  distance=BALL_PICKUP_LOAD_DISTACE, 
                  velocity=BALL_PICKUP_LOAD_VELOCITY, 
                  use_smart_drive = True,
                  do_wait=True)

    
def go_to_i_goal():
    drive_staight(direction=REVERSE, 
                  distance=RETURN_TO_I_GOAL_DISTANCE, 
                  velocity=RETURN_TO_I_GOAL_VELOCITY, 
                  use_smart_drive = False,
                  do_wait=True)
    adjust_to_goal_f()

def go_to_x_goal():
    drivetrain.turn_for(direction=LEFT,
                        angle=X_GOAL_ANGLE,
                        units=DEGREES)
    wait(250, MSEC)
    drive_staight(direction=REVERSE, 
                  distance=RETURN_TO_X_GOAL_DISTANCE, 
                  velocity=RETURN_TO_X_GOAL_VELOCITY, 
                  use_smart_drive = False,
                  do_wait=True)
    drivetrain.turn_for(direction=RIGHT,
                        angle=X_GOAL_ANGLE,
                        units=DEGREES)
    wait(250, MSEC)
    drive_staight(direction=REVERSE, 
                  distance=18, 
                  velocity=RETURN_TO_X_GOAL_VELOCITY, 
                  use_smart_drive = False,
                  do_wait=True)
    adjust_to_goal_f()

def unload_bot_with_catapult():
    wait(CATAPULT_WAIT_TIME, MSEC)
    catapult_button_on_off()
    wait(1500, MSEC)
    conveyor_unload()
    wait(CONVEYOR_TOP_UNLOAD_TIME, MSEC)

def unload_bot_with_conveyor():
    conveyor_unload()
    wait(CONVEYOR_BOTTOM_UNLOAD_TIME, MSEC)

def fetch_and_unload(x_goal=False, use_catapult=False):
    go_back_and_load()
    wait(250, MSEC)
    
    if x_goal:
        go_to_x_goal()
    else:
        go_to_i_goal()

    if use_catapult:
        unload_bot_with_catapult()
    else:
        unload_bot_with_conveyor()

def set_start_auton():
    global start_auton
    start_auton = True

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

# Calibrate the Drivetrain
calibrate_drivetrain()

## End of the drivetrain code

def auton_routine():
    global drivetrain

    intake_motor.spin(FORWARD, INTAKE_VELOCITY, PERCENT)
    drivetrain.drive_for(FORWARD, 4, INCHES)
    drivetrain.turn_for(direction=LEFT,
                        angle=START_TURN_ANGLE,
                        units=DEGREES,
                        velocity=28,
                        units_v=PERCENT,
                        wait=True)
    drive_staight(direction=FORWARD, 
                  distance=START_FORWARD_DIST, 
                  velocity=DRIVE_MAX_VELOCITY, 
                  use_smart_drive = False,
                  do_wait=True)
    drivetrain.turn_for(direction=RIGHT,
                        angle=START_TO_I_GOAL_ANGLE,
                        units=DEGREES,
                        velocity=30,
                        units_v=PERCENT,
                        wait=True)
    wait(200, MSEC)
    drive_staight(direction=REVERSE, 
                  distance=START_TO_I_GOAL_DIST, 
                  velocity=DRIVE_MAX_VELOCITY, 
                  use_smart_drive = False,
                  do_wait=True)
    wait(CATAPULT_WAIT_TIME, MSEC)
    unload_bot_with_catapult()
    wait(500, MSEC)
    adjust_to_goal_r()
    fetch_and_unload(x_goal=False, use_catapult=True)
    adjust_to_goal_r()
    fetch_and_unload(x_goal=True, use_catapult=True)
    fetch_and_unload(x_goal=False, use_catapult=True)
    while not stop_auton:
        fetch_and_unload(x_goal=False, use_catapult=False)
        adjust_to_goal_r()

calib_velocity = 100
def caliberate_distance():
    global calib_velocity
    if calib_velocity >= 10:
        calib_velocity = calib_velocity - 10
    else:
        calib_velocity = 100
    

def calib_go_forward(run_time):
    left_drive_smart.spin(FORWARD, calib_velocity)
    right_drive_smart.spin(FORWARD, calib_velocity)
    wait(run_time, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()
   
def calib_go_forward_quarter():
    calib_go_forward(250)

def calib_go_forward_half():
    calib_go_forward(500)

def calib_go_forward_one():
    calib_go_forward(1000)

def calib_go_forward_one_half():
    calib_go_forward(500)

# system event handlers
brain.buttonLeft.pressed(set_start_auton)
optical_sensor.object_detected(conveyor_hold)
catapult_sensor.object_detected(catapult_lowered)
catapult_sensor.object_lost(catapult_released)
# add 15ms delay to make sure events are registered correctly.
wait(750, MSEC)
when_started()

while not start_auton:
    wait(10, MSEC)

auton_routine()
#auton_thread = Thread(auton_routine)

#wait(600000, MSEC)
#stop_auto = True

drivetrain.stop()
conveyor.stop()
catapult_motor.stop()
intake_motor.stop()

