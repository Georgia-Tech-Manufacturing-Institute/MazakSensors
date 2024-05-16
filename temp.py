import numpy as np
from datetime import datetime as dt
import time
import daqhats

import os
import csv


# pip install -r requirements.txt
# https://github.com/adafruit/circup/issues/143 - Resolve with pip install setuptools

def init_csv(name='record', header=[]):
    init_date = dt.now().strftime('%Y-%m-%d')
    init_time = dt.now().strftime('%H-%M-%S')
    # Create directory if it doesn't exist
    directory = os.path.join('data', init_date)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f'{name}_{init_time}.csv')

    with open(filename, 'a', newline='') as f:
        csv_writer = csv.writer(f)

        if len(header)>0:
            csv_writer.writerow(header)
    return filename


def monitoring(sample_rate=0.1, timeout=10, channel_ranges=[]):
    '''
    :param sample_rate: time spacing between observations.
    :param timeout: Length of time to wait. Defaults to 10 seconds. Set as -1 to read indefinitely.
    :param channels: list of tuples; for each hat, specify the range of channels to read
    :return:
    '''
    def convert_temp(pin): # Conversion from voltage to
        voltage = (pin * 3.3) / 65536 # SCale voltage - update if change to 5V
        return (voltage - 1.25) / 0.005

    # Initialization
    start_time = time.time()
    hat_list = daqhats.hat_list()
    if len(hat_list) > 0:
        print('Identified Boards: ', len(hat_list))
        header = ['timestamp']
        devices = []
        for i, hat in enumerate(hat_list): # Allows for multiple boards
            address = hat.address # int
            try:
                lc, hc = channel_ranges[i]
            except IndexError: # Default to read all addresses
                lc, hc = 0, 7
            header += [f'{address}_{i}' for i in range(lc, hc)]

            devices.append(daqhats.mcc118(address=address))

            print('Blinking HAT: ', address)
            devices[-1].blink_led(count=3) # Blink to show that you exist !
    else:
        print('No Boards found')
        return None

    options = daqhats.OptionFlags.DEFAULT
    condition = True

    # Initialize CSV
    filename = init_csv(name='temperature', header=header)
    while condition:
        it_start = time.time()
        #row = np.zeros((len(header)))  # Single row
        row = list(range(len(header)))
        row[0] = dt.now().strftime('%m-%d %H:%M:%S')
        i = 1
        for head in header[1:]:
            row[i] = devices[int(head[0])].a_in_read(int(head[-1]), options)
            row[i] = convert_temp(row[i])
            print(row[i], type(row[i]))
            i += 1
            
        #row[1:] = convert_temp(row[1:]) # Convert temperature values
        # apapnendnd  the row
        with open(filename, 'a', newline='') as f:
            csv.writer(f).writerow(row)

        if timeout == -1: # Do not terminate until forced.
            condition = True
        else: # Check if timeout exceeded
            condition = (time.time() - start_time) > timeout

        elapsed = time.time() - it_start
        if elapsed > sample_rate:
            time.sleep(sample_rate-elapsed) # wait for length of sample rate.

if __name__ == '__main__':
    #print(daqhats.__version__)
    monitoring(1, channel_ranges=[(1,2)])


