#!/usr/bin/python
#
# Analog Input with ADC0832 chip
#
# Part of SunFounder LCD StarterKit
#
# Code Credit:
# http://heinrichhartmann.com/blog/2014/12/14/Sensor-Monitoring-with-RaspberryPi-and-Circonus.html
#
# Changes made by Justin Limbach for better output voltage readings and LCD display
#
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
VoltsPerBit = 3.3 / 255             # Assuming using a 3.3 V reference
# Pins connected from the SPI port on ADC to the Cobbler
PIN_CLK = 18
PIN_D0 = 27
PIN_DI = 22
PIN_CS = 17

# Setting up the SPI interface pins
GPIO.setup(PIN_DI, GPIO.OUT)
GPIO.setup(PIN_D0, GPIO.IN)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_CS, GPIO.OUT)

# Reading SPI data form ADC 8032
def getADC(channel):

    # 1. CS LOW.
    GPIO.output(PIN_CS, True)           # Clearing last transmission
    GPIO.output(PIN_CS, False)          # Brining CS low

    # 2. Clock Initialization
    GPIO.output(PIN_CLK, False)         # Starts the clock low

    # 3. Input MUX address
    for i in [1, 1, channel]:           # start bit + mux assignment
        if i == 1:
            GPIO.output(PIN_DI, True)
        else:
            GPIO.output(PIN_DI, False)
        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)

    # 4. read 8 ADC bits
    ad = 0
    for i in range(8):
        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)
        ad <<= 1                    # bit shift
        if GPIO.output(PIN_D0):
            ad |= 0x1               # set first bit

    # 5. reset
    GPIO.output(PIN_CS, True)

    return ad

if __name__ == "__main__":
    while True:
        print "ADC[0]: %d \t  ADC[1]: %d".format(getADC(0), getADC(1))
        time.sleep(1)
