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
        voltage = (pin.value * 3.3) / 65536
        return (voltage - 1.25) / 0.005

    # Initialization
    start_time = time.time()
    hat_list = daqhats.hat_list()

    if len(hat_list) > 1:
        print('Identified Boards: ', len(hat_list))

        devices = []
        for i, hat in enumerate(hat_list): # Allows for multiple boards
            address = hat.address # int
            try:
                print(channel_ranges[i])
            except IndexError:
                lc, hc = 0, 7
            devices.append(mcc118(address=address))
            print('Blinking HAT: ', address)
            devices[-1].blink_led(count=10) # Blink to show that you exist !
    else:
        print('No Boards found')
        return None

    options = OptionFlags.DEFAULT
    condition = True
    data_array = np.zeros(len())
    while condition:
        temp_array = convert_temp(np.array(tca)) # should do it to the whole array but we'll see

        for hat in devices:
            for chan in range(low_chan, high_chan + 1):
                value = hat.a_in_read(chan, options)

        if timeout == False:
            condition = True
        else: # Check if timeout exceeded
            condition = (time.time() - start_time) > timeout

        time.sleep(sample_rate)

    return temp_array

if __name__ == '__main__':
    monitoring(1)