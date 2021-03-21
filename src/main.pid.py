# Import Libraries
import time, os, sys, threading
import RPi.GPIO as gp
from encoder import Encoder

#########################################################################
# FUNCTIONS
#########################################################################

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
    return x
def change_duty(x):
    pwm.ChangeDutyCycle(x)
    return x
def change_direction(x):
    if x == 'ccw':
        gp.output(P1, gp.HIGH)
        gp.output(P2, gp.LOW)
    if x == 'cw':
        gp.output(P1, gp.LOW)
        gp.output(P2, gp.HIGH)
    return x

#########################################################################
# REGISTERS
#########################################################################

# PIN VARS           

P1            = 16      # HBRIDGE CONTROL X
P2            = 20      # HBRIDGE CONTROL Y 
PW            = 21      # HBRIDGE PWM

ENC_A         = 19      # ENCODER PHASE A
ENC_B         = 26      # ENCODER PHASE B

# PWM VARS

FREQUENCY     = 10000    # PWM INITIAL FREQUENCY
DUTY_CYCLE    =   10    # PWM INITIAL DUTY CYCLE

KDC           = 3
KF            = 1

# PID VARS

PULSE_REV     = 600     
START         = 0
SAMPLETIME    = 0.0005
TARGET        = 0

KP            = 20.0
KD            = 4.0
KI            = 0.04

ERROR_PREV    = 0
ERROR_SUM     = 0
PV            = 0

# DATA LOG VARS

TESTNAME = 'mar_19_log'


#########################################################################
# SETUP
#########################################################################

# GPIO LIBRARY SETUP

gp.setwarnings(False)
gp.setmode(gp.BCM)

# GPIO PIN MODE SETUP

gp.setup(P1, gp.OUT) # HBRIDGE CONTROL X
gp.setup(P2, gp.OUT) # HBRIDGE CONTROL Y
gp.setup(PW, gp.OUT) # HBRIDGE PWM

# ENCODER SETUP 

encoder = Encoder(ENC_A, ENC_B)

# PWM SETUP 

pwm = gp.PWM(PW, FREQUENCY)

gp.output(P1, gp.HIGH) # Initial direction CW
gp.output(P2, gp.LOW)

#########################################################################
# PID
#########################################################################

pwm.start(DUTY_CYCLE)               # PWM START

f = open(TESTNAME + '.391', 'w')    # OPEN LOG FILE FOR WRITING

START = time.time()                 # SET PROGRAM START TIME

while True:                             # FOREVER
    

    time.sleep(0.1)                             # WAIT 0.1 SECONDS
    os.system('clear')                          # CLEAR SCREEN

    ERROR = (TARGET - encoder.value) / 600.0    # CALCULATE ERROR


    # ###########################  TEST ################################## #

    if ERROR > 0:                    
        change_direction('ccw')          # ADJUST DIRECTION CW
    else:
        change_direction('cw')         # ADUST DIRECTION CCW

    if abs(ERROR) < 1e2:
        PV = (ERROR * KP) + (ERROR_PREV * KD) + (ERROR_SUM * KI) 

    DUTY_CYCLE =  change_duty(KDC * abs(PV))
    #FREQUENCY = change_frequency(abs(PV))

    # #################################################################### #

    time.sleep(SAMPLETIME)              # WAIT FOR SAMPLETIME SECONDS
    
    ERROR_PREV = ERROR                  # SAVE DERIVATIVE ERROR
    ERROR_SUM += ERROR                  # ADD INTEGRAL ERROR

    # PRINT DATA AND WRITE TO FILE

    INFO = ''' 
    ------------------------------------------------------------------------  
    KP = {kp:<04.2f}                                         t  =  {dt: >14.3f}  
    KD = {kd:< 04.2f} 
    KI = {ki:< 4.2f}  
                                                    ___________________________
    ERROR         \t   e   = {e_: > 10.3f} \t   |  e   *  KP  =  {x: > 10.3f} 
    dERROR        \t   de  = {ep: > 10.3f} \t   |  de  *  KD  =  {y: > 10.3f} 
    sum(ERROR)    \t   se  = {es: > 10.3f} \t   |  se  *  KI  =  {z: > 10.3f}
    _______________________________________________

    PROCESS VARIABLE  \t         e * KP + de * KD + se * KI = PV  =   {pv: > 10.3f} 
    
    ________________________________________________________________________ 

    K_DC = {kdc:3.0f}
    k_F  = {kf:3.0f}

    DUTY CYCLE \t\t V   =  PV  *  K_DC  = {dc: > 16.3f}  
    FREQUENCY  \t\t f   =  PV  *  K_F   = {f: > 16.3f}    
    
    --------------------------------------------------------------------------'''.format(e_=ERROR, ep=ERROR_PREV, es=ERROR_SUM,
                                                                                        dt=time.time() - START, s=' ',
                                                                                        kp=KP, kd=KD, ki=KI,
                                                                                        kdc=KDC, kf=KF,
                                                                                        dc=DUTY_CYCLE, f=FREQUENCY, 
                                                                                        pv=PV,
                                                                                        x=KP*ERROR, y=KD*ERROR_PREV, z=KI*ERROR_SUM)
    
    print(INFO)                         # PRINT DATA
    f.write(INFO)                       # WRITE DATA TO FILE

f.close()       # CLOSE FILE