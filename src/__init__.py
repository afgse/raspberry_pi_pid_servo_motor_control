import gpiozero as gp
import os
import time

f1 = gp.DigitalInputDevice(19)
f2 = gp.DigitalInputDevice(26)

c1 = gp.DigitalOutputDevice(20)
c2 = gp.DigitalOutputDevice(21)

count1 = 0
count2 = 0
def activated1():
    global count1
    count1 += 1
    pass

def activated2():   
    global count2
    count2 += 1
    pass

def deactivated1():
    pass

def deactivated2():
    pass

start = time.time()

D1 = []
D2 = []


f1.when_activated = activated1
f2.when_activated = activated2

f1.when_deactivated = deactivated1
f2.when_deactivated = deactivated2

