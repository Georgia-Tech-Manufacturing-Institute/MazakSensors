import numpy as np
import board
import analogio
import adafruit_tca9548a
import time

# pip install -r requirements.txt
# https://github.com/adafruit/circup/issues/143 - Resolve with pip install setuptools
#

def temp_monitoring(sample_rate=0.1):
    '''
    Setup: RPi 4, adafruit AD8495 thermocouple amplifiers, type K thermocouples
    Amplifier outputs are connected to a multiplexor -> Mux to
    AD8495 https://learn.adafruit.com/ad8495-thermocouple-amplifier/python-circuitpython
    Multiplexor https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/circuitpython-python
    :return:
    '''
    def convert_temp(pin): # Conversion from voltage to
        voltage = (pin.value * 3.3) / 65536
        return (voltage - 1.25) / 0.005


    i2c = board.I2C()  # uses board.SCL and board.SDA
    tca = adafruit_tca9548a.TCA9548A(i2c) # Create TCA9548A object and give it the I2C bus
    temp_array = convert_temp(np.array(tca)) # should do it to the whole array but we'll see

    return temp_array

if __name__ == '__main__':
    temp_monitoring(1)