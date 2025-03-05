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
LEFT_WHEEL_SCALE_DOWN = .95

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
brain.screen.print("SH_N3: Pid Test\n")
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

#If value is true, it's on the left, and if it's false, it's on the right

def when_started():
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_VELOCITY, PERCENT)
    left_drive_smart.set_stopping(BRAKE)
    right_drive_smart.set_stopping(BRAKE)


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

def spid_stop():
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

def spid_zero_to_v(right_target_velocity):
    
    done = False
    start_spin = True
    if  right_target_velocity >  0:
        direction = FORWARD
    else:
        direction = REVERSE

    while not done:
        if start_spin:
            right_motor_velocity = 0
        else:
            right_motor_velocity = right_drive_smart.velocity(PERCENT)

        error = right_target_velocity - right_motor_velocity
        if error < -10:
            new_right_motor_velocity = right_motor_velocity - 10
        elif error > 10:
            new_right_motor_velocity = right_motor_velocity + 10
        else:
            new_right_motor_velocity = right_target_velocity
            done = True
        
        if right_motor_velocity > 25:
            new_right_motor_velocity = right_target_velocity
            done = True
        
        new_left_motor_velocity = new_right_motor_velocity * LEFT_WHEEL_SCALE_DOWN
        
        if start_spin:
            right_drive_smart.spin(direction, new_right_motor_velocity, PERCENT)
            left_drive_smart.spin(direction, new_left_motor_velocity, PERCENT)
            start_spin = False
        else:
            right_drive_smart.set_velocity(new_right_motor_velocity, PERCENT)
            left_drive_smart.set_velocity(new_left_motor_velocity, PERCENT)
        
# Calibrate the Drivetrain
calibrate_drivetrain()

def run_base_test():
    for i in range(10):
        left_drive_smart.spin(FORWARD, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(FORWARD, 100)
        wait(1000, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
        wait(160, MSEC)
        left_drive_smart.spin(REVERSE, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(REVERSE, 100)
        wait(1000, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
        wait(160, MSEC)

def run_spid_test():
    for i in range(10):
        left_drive_smart.spin(FORWARD, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(FORWARD, 100)
        #spid_zero_to_v(100)
        wait(1000, MSEC)
        spid_stop()
        left_drive_smart.spin(REVERSE, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(REVERSE, 100)
        #spid_zero_to_v(-100)
        wait(1000, MSEC)
        spid_stop()

def run_once_forward():
        left_drive_smart.spin(FORWARD, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(FORWARD, 100)
        wait(1500, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()

def run_once_forward_pid():
        left_drive_smart.spin(FORWARD, 100*LEFT_WHEEL_SCALE_DOWN)
        right_drive_smart.spin(FORWARD, 100)
        # spid_zero_to_v(100)
        wait(1000, MSEC)
        spid_stop()
        # spid_stop()

## End of the drivetrain code

controller.buttonEUp.pressed(run_base_test)
controller.buttonFUp.pressed(run_spid_test)
controller.buttonEDown.pressed(run_once_forward)
controller.buttonFDown.pressed(run_once_forward_pid)

# system event handlers
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started()

remote_control_code_enabled = True
rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)


