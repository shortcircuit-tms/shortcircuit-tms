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

CONVEYOR_INIT = 0
CONVEYOR_UNLOADING = 1
CONVEYOR_LOADING = 2
CONVEYOR_LOADED = 3

BALL_PICKUP_ZONE_DISTANCE = 25
BALL_PICKUP_LOAD_DISTACE = 18
BALL_PICKUP_ZONE_VELOCITY = 100
BALL_PICKUP_LOAD_VELOCITY = 30
RETURN_TO_I_GOAL_DISTANCE = 41
RETURN_TO_I_GOAL_VELOCITY = 100
ADJUST_TO_GOAL_TIME_1 = 500
ADJUST_TO_GOAL_TIME_2 = 250
ADJUST_TO_GOAL_VELOCITY_1 = 50
X_GOAL_ANGLE = 30
RETURN_TO_X_GOAL_VELOCITY = 100
RETURN_TO_X_GOAL_DISTANCE = 43

CONVEYOR_TOP_UNLOAD = 1500
CONVEYOR_BOTTOM_UNLOAD = 2500
CATAPULT_WAIT_TIME = 1000

# Port configurations
# All L(left) R(right) directions are defined from viewpoint
# looking from behind the bot towards the flyweel
 
CONVEYER_L_PORT = Ports.PORT1
CATAPULT_PORT = Ports.PORT2
INTAKE_PORT = Ports.PORT4
CONVEYER_R_PORT = Ports.PORT5
OPTICAL_SENSOR_PORT = Ports.PORT6
CATAPULT_SENSOR_PORT = Ports.PORT8
DRIVETRAIN_L_PORT = Ports.PORT9
DRIVETRAIN_R_PORT = Ports.PORT10
DISTANCE_SENSOR_PORT = Ports.PORT11

# Brain should be defined by default
brain=Brain()
brain.screen.print("SH_N3: Calib\n")
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

def when_started():
    global conveyor, intake_motor, catapult_motor, drivetrain

    conveyor.set_max_torque(CONVEYOR_TORQUE, PERCENT)
    conveyor.set_velocity(CONVEYOR_VELOCITY, PERCENT)
    intake_motor.set_max_torque(INTAKE_TORQUE, PERCENT)
    intake_motor.set_velocity(INTAKE_VELOCITY, PERCENT)
    catapult_motor.set_max_torque(CATAPULT_TORQUE, PERCENT)
    catapult_motor.set_velocity(CATAPULT_VELOCITY, PERCENT)
    catapult_motor.set_stopping(HOLD)
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)
    drivetrain.set_drive_velocity(DRIVETRAIN_VELOCITY, PERCENT)
 
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

def print_row(text, row_number, delete_row_before_print=True):
    if delete_row_before_print:
        brain.screen.clear_row(row_number)
    brain.screen.set_cursor(row_number, 1)
    brain.screen.print(text)

# Calibrate the Drivetrain
calibrate_drivetrain()

## End of the drivetrain code

calib_velocity = 100
def set_caliberate_velocity():
    global calib_velocity
    if calib_velocity > 10:
        calib_velocity = calib_velocity - 10
    else:
        calib_velocity = 100
    message = "v=" + str(calib_velocity) + ",t=" + str(calib_time)
    print_row(text=message, row_number=1)
    
calib_time = 250
def set_caliberate_time():
    global calib_time
    if calib_time > 3000:
        calib_time = 250
    else:
        calib_time = calib_time + 125
    message = "v=" + str(calib_velocity) + ",t=" + str(calib_time)
    print_row(text=message, row_number=1)

calib_dis = 2
def set_caliberate_dist():
    global calib_dis, calib_time
    if calib_dis > 36:
        calib_dis = 2
    else:
        calib_dis = calib_dis + 2
    calib_time = get_drive_time_for_distance(calib_dis)
    message = "v=" + str(calib_velocity) + ",t=" + str(calib_time)
    print_row(text=message, row_number=1)
    message = "d=" + str(calib_dis)
    print_row(text=message, row_number=2)

def calib_go_forward():
    global calib_velocity, calib_time
    left_drive_smart.spin(FORWARD, calib_velocity)
    right_drive_smart.spin(FORWARD, calib_velocity)
    wait(calib_time, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()

def calib_go_backward():
    global calib_velocity, calib_time
    left_drive_smart.spin(REVERSE, calib_velocity)
    right_drive_smart.spin(REVERSE, calib_velocity)
    wait(calib_time, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()
    

# system event handlers
controller.buttonEUp.pressed(set_caliberate_time)
controller.buttonEDown.pressed(set_caliberate_dist)
controller.buttonFUp.pressed(set_caliberate_velocity)
controller.buttonRUp.pressed(calib_go_forward)
controller.buttonLUp.pressed(calib_go_backward)

# add 15ms delay to make sure events are registered correctly.
wait(750, MSEC)
when_started()

