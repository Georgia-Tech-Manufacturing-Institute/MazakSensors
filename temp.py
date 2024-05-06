import numpy as np
import board
import time
import daqhats
from daqhats import mcc118, OptionFlags
from sys import stdout

# pip install -r requirements.txt
# https://github.com/adafruit/circup/issues/143 - Resolve with pip install setuptools
#

def monitoring(sample_rate=0.1, timeout=10, channel_ranges=[(0,7)]):
    '''

    :param sample_rate:
    :param timeout:
    :param channels: list of tuples; for each hat, specify the range of channels to cread
    :return:
    '''
    def convert_temp(pin): # Conversion from voltage to
        voltage = (pin * 3.3) / 65536
        return (voltage - 1.25) / 0.005

    # Initialization
    start_time = time.time()
    print(start_time)
    hat_list = daqhats.hat_list()
    measurements = 0
    print(hat_list)
    if len(hat_list) > 0:
        print('Identified Boards: ', len(hat_list))
        devices = []
        for i, hat in enumerate(hat_list): # Allows for multiple boards
            address = hat.address # int
            try:
                lc, hc = channel_ranges[i]
            except IndexError:
                lc, hc = 0, 7
            measurements += hc - lc + 1
            devices.append((mcc118(address=address), lc, hc))
            devices[-1][0].blink_led(count=10) # Blink to show that you exist !
    else:
        print('No Boards found')
        return None

    options = OptionFlags.DEFAULT
    condition = True
    data_array = np.zeros((int(timeout//sample_rate), measurements))
    i = 0
    while condition:
        row = np.zeros(measurements)
        j = 0
        for hat, lc, hc in devices: # Board 
            for chan in range(lc, hc + 1): # Channel
                row[j] = hat.a_in_read(chan, options)
                j += 1
        data_array[i, :] = convert_temp(row)
        print(row)
        if timeout == False: # Keep going until manual stop
            condition = True
        else: # Check if timeout exceeded
            condition = (time.time() - start_time) < timeout
        j+=1
        time.sleep(sample_rate)
    return None#temp_array

if __name__ == '__main__':
    monitoring(timeout=1, channel_ranges=[(1,1)])