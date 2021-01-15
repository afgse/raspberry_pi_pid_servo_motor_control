import gpiozero as gp
import time
import RPi.GPIO as GPIO
from encoder import Encoder
from stepper import Motor
from data import *

def main():
 
    encoder = Encoder(20,21)
    motor = Motor(bcm[0],bcm[1],bcm[2],bcm[3],0.1)
 
    while True:
        print('Encoder : {}\t\t'.format(encoder.getValue()),end='\r')
        if encoder.getValue() > 50:
            motor.foreward()

if __name__ == '__main__':
    exit(main())
    
