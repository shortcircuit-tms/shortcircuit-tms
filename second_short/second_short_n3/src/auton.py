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
brain.screen.print("SH_N3: Auton\n")
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

#endregion VEXcode Generated Robot Configuration

myVariable = 0
launcher_speed = 0
conveyer_state = CONVEYOR_INIT 
is_intake_on = False
is_catapult_loaded = False
is_catapult_on = False
start_auton = False
stop_auton = False

def when_started():
    global conveyor_state, conveyor
    global is_intake_on, intake_motor
    global is_catapult_on, catapult_motor, is_catapult_loaded
    global start_auton, stop_auton

    conveyor_state = CONVEYOR_INIT
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
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)
    drivetrain.set_drive_velocity(DRIVETRAIN_VELOCITY, PERCENT)
    start_auton = False
    stop_auton = False
    if not is_catapult_loaded:
        catapult_button_on_off()
    wait(2000, MSEC)
    intake_motor.spin(FORWARD)
    wait(5000, MSEC)
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

    drivetrain.drive_for(direction=REVERSE,
                         distance=12,
                         units=INCHES,
                         velocity=100,
                         units_v=PERCENT,
                         wait=True)
    wait(500, MSEC)
    drivetrain.turn_for(direction=LEFT,
                        angle=85,
                        units=DEGREES,
                        velocity=30,
                        units_v=PERCENT,
                        wait=True)
    wait(200, MSEC)
    drivetrain.drive_for(direction=REVERSE,
                         distance=26,
                         units=INCHES,
                         velocity=100,
                         units_v=PERCENT,
                         wait=True)
    wait(1000, MSEC)
    #catapult_button_on_off()
    #left_drive_smart.spin(FORWARD)
    #right_drive_smart.spin(FORWARD)
    #wait(1750, MSEC)
    #left_drive_smart.stop()
    #right_drive_smart.stop()
    #intake_on_off()
    #conveyor_load()
    #wait(1000, MSEC)
    #intake_on_off()
    #left_drive_smart.spin(REVERSE)
    #right_drive_smart.spin(REVERSE)
    #wait(2750, MSEC)
    #left_drive_smart.stop()
    #right_drive_smart.stop()
    #conveyor_unload()
    


# system event handlers
brain.buttonLeft.pressed(set_start_auton)
optical_sensor.object_detected(conveyor_hold)
catapult_sensor.pressed(catapult_bumper_pressed)
catapult_sensor.released(catapult_bumper_released)
# add 15ms delay to make sure events are registered correctly.
wait(750, MSEC)
when_started()

while not start_auton:
    wait(10, MSEC)

auton_routine()


