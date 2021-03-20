import time, os, sys, threading
import RPi.GPIO as gp

# GPIO Library Setup
gp.setwarnings(False)
gp.setmode(gp.BCM)

# Encoder (Feedback) Setup
from encoder import Encoder
ENC_A, ENC_B = 19, 26
encoder = Encoder(ENC_A, ENC_B)

#########################################################################
# FUNCTIONS
#########################################################################

# Clear the Screen
def clear():
    os.system('clear')
    return None

# Start and Stop the Motor
def start(x):
    pwm.start(x)
    return None
def stop():
    pwm.stop()
    return None

# Change PWM Attributes
def change_frequency(x):
    pwm.ChangeFrequency(x)
    return None
def change_duty(x):
    pwm.ChangeDutyCycle(x)
    return None
def change_direction(x):
    if x == 'ccw':
        gp.output(P1, gp.HIGH)
        gp.output(P2, gp.LOW)
    if x == 'cw':
        gp.output(P1, gp.LOW)
        gp.output(P2, gp.HIGH)
    return None

#########################################################################
# SETUP
#########################################################################

# Control Setup
P1, P2 = 16, 20
gp.setup(P1, gp.OUT)
gp.setup(P2, gp.OUT)
gp.output(P1, gp.HIGH)
gp.output(P2, gp.LOW)

# PWM Setup
PW = 21
frequency, duty_cycle = 10000, 0
gp.setup(PW, gp.OUT)
pwm = gp.PWM(PW, frequency)
pwm.start(duty_cycle)

# PID Setup
SAMPLETIME, TARGET = 0.005, 0
KP, KD, KI = 1, 0.1, 0.01
e1_prev_error = 0
e1_sum_error = 0
PV = 0

# Open Log File and Start Timer
TESTNAME = 'mar_19_log'
f = open(TESTNAME + '.391', 'w')
START = time.time()

#########################################################################
# PID
#########################################################################

# Forever
os.system('clear')
while True:
    
    # Wait and Reset Screen
    time.sleep(0.1)
    os.system('clear')

    # Calculate Error
    e1_error = TARGET - encoder.value / 600

    # Adjust Direction
    if e1_error > 0.01:
        change_direction('cw')
    else:
        change_direction('ccw')

    # Update Process Variable
    PV = (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)

    if abs(PV) < 99:
        K = 2
        change_duty(K * abs(PV))

    # Wait
    time.sleep(SAMPLETIME)
    
    # Update Error
    e1_prev_error = e1_error
    e1_sum_error += e1_error

    # Print and Save Information
    INFO = '{} | t {:>10.3f} | erf {:>10.3f} | pv {:>10.3f} | dt {:>10.3f} | int {:>20.3f}'.format(time.ctime()[:10],
                          time.time() - START,
                            e1_error * KP,
                            PV,
                            e1_prev_error * KD,
                            e1_sum_error * KI)
    print(INFO)
    f.write(INFO)

# Close File
f.close()