# -*- coding: utf-8 -*-
# @author: leesoar

"""Raspberry Pi"""

import argparse
import json

from . import util, __version__


def show_devices(args):
    devices = util.get_raspberry_pi()

    try:
        for i, d in enumerate(devices, start=1):
            print(f"=> Device {i}:\n{json.dumps(d, ensure_ascii=False, indent=4)}\n")
    except TypeError:
        print("No devices online.")


def run():
    parser = argparse.ArgumentParser(
        description=f"A Raspberry Pi Toolkit.",
        prog="raspberrypi", add_help=False)

    subparsers = parser.add_subparsers(dest='cmd', title='Available commands')
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of raspberrypi')
    parser.add_argument('-h', '--help', action='help', help='Show help message')

    p_device = subparsers.add_parser('device')
    p_device.set_defaults(func=show_devices)

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception:
        print("A Raspberry Pi Toolkit.")
