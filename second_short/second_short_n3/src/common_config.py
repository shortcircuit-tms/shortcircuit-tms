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