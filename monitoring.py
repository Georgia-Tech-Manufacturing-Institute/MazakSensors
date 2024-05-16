#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 118 Functions Demonstrated:
        mcc118.a_in_scan_start
        mcc118.a_in_scan_read

    Purpose:
        Perform a finite acquisition on 1 or more channels.

    Description:
        Acquires blocks of analog input data for a user-specified group
        of channels.  The last sample of data for each channel is
        displayed for each block of data received from the device.  The
        acquisition is stopped when the specified number of samples is
        acquired for each channel.

"""
from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc118, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, \
chan_list_to_mask
import csv
import os
from datetime import datetime as dt
import numpy as np

CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'

def main():
    """
    This function is executed automatically when the module is run directly.
    """

    # Store the channels in a list and convert the list to a channel mask that
    # can be passed as a parameter to the MCC 118 functions.
    channels = [0, 1, 2, 3]
    channel_mask = chan_list_to_mask(channels)
    num_channels = len(channels)

    samples_per_channel = 10000
    scan_rate = 1000.0
    options = OptionFlags.DEFAULT

    try:
        # Select an MCC 118 HAT device to use.
        address = select_hat_device(HatIDs.MCC_118)
        hat = mcc118(address)

        print('\nSelected MCC 118 HAT device at address', address)

        actual_scan_rate = hat.a_in_scan_actual_rate(num_channels, scan_rate)

        print('\nMCC 118 continuous scan example')
        print('    Functions demonstrated:')
        print('         mcc118.a_in_scan_start')
        print('         mcc118.a_in_scan_read')
        print('    Channels: ', end='')
        print(', '.join([str(chan) for chan in channels]))
        print('    Requested scan rate: ', scan_rate)
        print('    Actual scan rate: ', actual_scan_rate)
        print('    Samples per channel', samples_per_channel)
        print('    Options: ', enum_mask_to_string(OptionFlags, options))


        # Configure and start the scan.
        hat.a_in_scan_start(channel_mask, samples_per_channel, scan_rate,
                            options)

        print('Starting scan ... Press Ctrl-C to stop\n')
    except (HatError, ValueError) as err:
        print('\n', err)
    header = ['timestamp'] + channels
    ff = init_csv(name='temperature', header= header)

    try:
        read_and_display_data(hat, samples_per_channel, num_channels, record_to=ff)

    except KeyboardInterrupt:
        # Clear the '^C' from the display.
        print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')
        hat.a_in_scan_stop()

    hat.a_in_scan_cleanup()



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



def read_and_display_data(hat, samples_per_channel, num_channels, record_to):
    """
    Reads data from the specified channels on the specified DAQ HAT devices
    and updates the data on the terminal display.  The reads are executed in a
    loop that continues until either the scan completes or an overrun error
    is detected.

    Args:
        hat (mcc118): The mcc118 HAT device object.
        samples_per_channel: The number of samples to read for each channel.
        num_channels (int): The number of channels to display.

    Returns:
        None

    """
    total_samples_read = 0
    read_request_size = 500
    timeout = 5.0 # seconds to wait for the samples to be read

    # Continuously update the display value until Ctrl-C is
    # pressed or the number of samples requested has been read.
    while total_samples_read < samples_per_channel:
        read_result = hat.a_in_scan_read_numpy(read_request_size, timeout)

        # Check for an overrun error
        if read_result.hardware_overrun:
            print('\n\nHardware overrun\n')
            break
        elif read_result.buffer_overrun:
            print('\n\nBuffer overrun\n')
            break

        samples_read_per_channel = int(len(read_result.data) / num_channels)
        total_samples_read += samples_read_per_channel

        with open(record_to, 'a', newline='') as f:
            csv.writer(f).writerow(row)

        if samples_read_per_channel > 0:
            stdout.flush()


if __name__ == '__main__':
    main()
