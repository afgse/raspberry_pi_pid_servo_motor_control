import gpiozero as gp
import time

class Motor:
    
    def __init__(self, pinOneHigh, pinOneLow, pinTwoHigh, pinTwoLow,speed):
        self.vccOneHigh = gp.DigitalOutputDevice(pinOneHigh)
        self.vccOneLow  = gp.DigitalOutputDevice(pinOneLow)
        self.vccTwoHigh = gp.DigitalOutputDevice(pinTwoHigh)
        self.vccTwoLow  = gp.DigitalOutputDevice(pinTwoLow)
        self.speed      = speed
        self.statesClockwise = [[1,0,1,0],
                                [0,1,1,0],
                                [0,1,0,1],
                                [1,0,0,1]]
        self.statesCounterClockwise = [[1,0,1,0],
                                       [1,0,0,1],
                                       [0,1,0,1],
                                       [0,1,1,0]]
   
    def state_update(self,state):
    
        if state[0] == 1:
            self.vccOneHigh.on()
        else:
            self.vccOneHigh.off()

        if state[1] == 1:
             self.vccOneLow.on()
        else:
             self.vccOneLow.off()
           
        if state[2] == 1:
             self.vccTwoHigh.on()
        else:
             self.vccTwoHigh.off()
            
        if state[3] == 1:
             self.vccTwoLow.on()
        else:
             self.vccTwoLow.off()
   
    def printer(self):
        print('\n{} {} {} {}\n'.format(self.vccOneHigh.value,
                                     self.vccOneLow.value,
                                     self.vccTwoHigh.value,
                                     self.vccTwoLow.value))
    
    def foreward(self):
        for state in self.statesClockwise:
            self.state_update(state)
            #self.printer() 
            time.sleep(self.speed)

    def backward(self):
        for state in self.statesCounterClockwise:
            self.state_update(state)
            #self.printer() 
            time.sleep(self.speed)
