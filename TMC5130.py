# Copyright 2021, Liberum Biotech Inc., All rights reserved.

import time
import spidev

TMC5130_dict = {
    "TMC5130_GCONF": 0x00,
    "TMC5130_GSTAT": 0x01,
    "TMC5130_IFCNT": 0x02,
    "TMC5130_SLAVECONF": 0x03,
    "TMC5130_INP_OUT": 0x04,
    "TMC5130_X_COMPARE": 0x05,
    "TMC5130_IHOLD_IRUN": 0x10,
    "TMC5130_TZEROWAIT": 0x11,
    "TMC5130_TSTEP": 0x12,
    "TMC5130_TPWMTHRS": 0x13,
    "TMC5130_TCOOLTHRS": 0x14,
    "TMC5130_THIGH": 0x15,

    "TMC5130_RAMPMODE": 0x20,
    "TMC5130_XACTUAL": 0x21,
    "TMC5130_VACTUAL": 0x22,
    "TMC5130_VSTART": 0x23,
    "TMC5130_A1": 0x24,
    "TMC5130_V1": 0x25,
    "TMC5130_AMAX": 0x26,
    "TMC5130_VMAX": 0x27,
    "TMC5130_DMAX": 0x28,
    "TMC5130_D1": 0x2A,
    "TMC5130_VSTOP": 0x2B,
    "TMC5130_TZEROCROSS": 0x2C,
    "TMC5130_XTARGET": 0x2D,

    "TMC5130_VDCMIN": 0x33,
    "TMC5130_SWMODE": 0x34,
    "TMC5130_RAMPSTAT": 0x35,
    "TMC5130_XLATCH": 0x36,
    "TMC5130_ENCMODE": 0x38,
    "TMC5130_XENC": 0x39,
    "TMC5130_ENC_CONST": 0x3A,
    "TMC5130_ENC_STATUS": 0x3B,
    "TMC5130_ENC_LATCH": 0x3C,

    "TMC5130_MSLUT0": 0x60,
    "TMC5130_MSLUT1": 0x61,
    "TMC5130_MSLUT2": 0x62,
    "TMC5130_MSLUT3": 0x63,
    "TMC5130_MSLUT4": 0x64,
    "TMC5130_MSLUT5": 0x65,
    "TMC5130_MSLUT6": 0x66,
    "TMC5130_MSLUT7": 0x67,
    "TMC5130_MSLUTSEL": 0x68,
    "TMC5130_MSLUTSTART": 0x69,
    "TMC5130_MSCNT": 0x6A,
    "TMC5130_MSCURACT": 0x6B,
    "TMC5130_CHOPCONF": 0x6C,
    "TMC5130_COOLCONF": 0x6D,
    "TMC5130_DCCTRL": 0x6E,
    "TMC5130_DRVSTATUS": 0x6F,
    "TMC5130_PWMCONF": 0x70,
    "TMC5130_PWMSTATUS": 0x71,
    "TMC5130_EN_CTRL": 0x72,
    "TMC5130_LOST_STEPS": 0x73,

    # ramp modes (Register TMC5130_RAMPMODE)
    "TMC5130_MODE_POSITION": 0,
    "TMC5130_MODE_VELPOS": 1,
    "TMC5130_MODE_VELNEG": 2,
    "TMC5130_MODE_HOLD": 3,

    # limit switch mode bits (Register TMC5130_SWMODE)
    "TMC5130_SW_STOPL_ENABLE":0x0001,
    "TMC5130_SW_STOPR_ENABLE":0x0002,
    "TMC5130_SW STOPL_POLARITY": 0x0004,
    "TMC5130_SW_STOPR_POLARITY": 0x0008,
    "TMC5130_SW_SWAP_LR": 0x0010,
    "TMC5130_SW_LATCH_L_ACT": 0x0020,
    "TMC5130_SW_LATCH_L_INACT": 0x0040,
    "TMC5130_SW_LATCH_R_ACT": 0x0080,
    "TMC5130_SW_LATCH_R_INACT": 0x0100,
    "TMC5130_SW_LATCH_ENC": 0x0200,
    "TMC5130_SW_SG_STOP": 0x0400,
    "TMC5130_SW_SOFTSTOP": 0x0800,

    # Status bits (Register TMC5130_RAMPSTAT)
    "TMC5130_RS_STOPL": 0x0001,
    "TMC5130_RS_STOPR": 0x0002,
    "TMC5130_RS_LATCHL": 0x0004,
    "TMC5130_RS_LATCHR": 0x0008,
    "TMC5130_RS_EV_STOPL": 0x0010,
    "TMC5130_RS_EV_STOPR": 0x0020,
    "TMC5130_RS_EV_STOP_SG": 0x0040,
    "TMC5130_RS_EV_POSREACHED": 0x0080,
    "TMC5130_RS_VELREACHED": 0x0100,
    "TMC5130_RS_POSREACHED": 0x0200,
    "TMC5130_RS_VZERO": 0x0400,
    "TMC5130_RS_ZEROWAIT": 0x0800,
    "TMC5130_RS_SECONDMOVE": 0x1000,
    "TMC5130_RS_SG": 0x2000,

    #Encoderbits (Register TMC5130_ENCMODE)
    "TMC5130_EM_DECIMAL": 0x0400,
    "TMC5130_EM_LATCH_XACT": 0x0200,
    "TMC5130_EM_CLR_XENC": 0x0100,
    "TMC5130_EM_NEG_EDGE": 0x0080,
    "TMC5130_EM_POS_EDGE": 0x0040,
    "TMC5130_EM_CLR_ONCE": 0x0020,
    "TMC5130_EM_CLR_CONT": 0x0010,
    "TMC5130_EM_IGNORE_AB": 0x0008,
    "TMC5130_EM_POL_N": 0x0004,
    "TMC5130_EM_POL_B": 0x0002,
    "TMC5130_EM_POL_A": 0x0001
}

class Stepmotor:
    #INITIALIZE
    def __init__(self, bus, device, holdcurrent, runcurrent):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 976000
        self.spi.mode = 3
        
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_GCONF"],4)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_TPWMTHRS"],500)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_PWMCONF"],0x000401C8)
    
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_CHOPCONF"],0x000100C3)

        #self.tmc5130_writeDatagram(TMC5130_IHOLD_IRUN, 0, 7, 5, 2);# 0.35Apeak/ 0.25ARMS
        self.tmc5130_writeDatagram(TMC5130_dict["TMC5130_IHOLD_IRUN"], 0, holdcurrent, runcurrent, 2);# 0.00Apeak/ 0.71ARMS
 
        #Reset position
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_RAMPMODE"], TMC5130_dict["TMC5130_MODE_POSITION"])
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_XTARGET"], 0)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_XACTUAL"], 0)

        #Standard values for speed and acceleration
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_VSTART"], 1)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_A1"], 30000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_V1"], 50000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_AMAX"], 10000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_VMAX"], 150000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_DMAX"], 10000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_D1"], 30000)
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_VSTOP"], 10)

    #WRITE REGISTERS
    def tmc5130_writeDatagram(self, address, x1, x2, x3, x4):
        #write TMC5130 register, where x1 is the highest and x4 the lowest byte
        buf = bytes([address | 0x80, x1,x2,x3,x4])
        self.spi.writebytes(buf)

    def tmc5130_writeInt(self, address, value):
        #write TMC5130 register
        self.tmc5130_writeDatagram(address, 0xFF & (value>>24), 0xFF & (value>>16), 0xFF & (value>>8), 0xFF & (value>>0))

    def tmc5130_readInt(self, address):
        #read TMC5130 register
        buf = bytes([address & 0x7F, 0,0,0,0]) ###
        self.spi. writebytes(buf)
        buf = self.spi.readbytes(5)

        value = buf[1]
        value <<= 8
        value |= buf[2]
        value <<= 8
        value |= buf[3]
        value <<= 8
        value |= buf[4]

        return value

    #VELOCITY MODE
    def TMC5130_rotate(self,velocity):
        #rotates the motor with a defined velocity, sign defines direction

        #set absolute velocity, independant from direction
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_VMAX"], abs(velocity))

        if velocity>=0:
            self.tmc5130_writeInt(TMC5130_dict["TMC5130_RAMPMODE"], 1)
        else:
            self.tmc5130_writeInt(TMC5130_dict["TMC5130_RAMPMODE"], 2)

    
    def TMC5130_right(self, velocity):
        #rotate motor with positive step count
        self.TMC5130_rotate(velocity) 


    def TMC5130_left(self, velocity):
        #rotate motor with negative step count
        self.TMC5130_rotate(-1 * velocity) 

    #POSITION MODE        
    def TMC5130_moveTo (self, position):
        #moves the motor to a certain position, make sure to set acceleration and velocity values upfront
        #set position
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_XTARGET"], position)
        #change to positioning mode
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_RAMPMODE"], 0)


    def TMC5130_moveBy(self, steps):
        #determine actual position and add numbers of ticks to move
        position = self.tmc5130_readInt(TMC5130_dict["TMC5130_XACTUAL"])
        self.TMC5130_moveTo(position+steps)
        
    def TMC5130_setVelocity(self, velocity):
        self.tmc5130_writeInt(TMC5130_dict["TMC5130_VMAX"], abs(velocity))
        
    def TMC5130_Close(self):
        self.spi.close()
