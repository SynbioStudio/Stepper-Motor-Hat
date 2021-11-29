from TMC5130 import *
import time

motor0 = Stepmotor (0,0,15,15) #bus, chip select, hold current (0-31), run current (0-31)
motor1 = Stepmotor (0,1,15,15) #bus, chip select, hold current (0-31), run current (0-31)

#turn motor 0 right for 1 second at 100000 velocity
motor0.TMC5130_right(100000)
time.sleep(1)
motor0.TMC5130_right(0)

#turn motor 1 left for 1 second at 100000 velocity
motor1.TMC5130_left(100000)
time.sleep(1)
motor1.TMC5130_left(0)
