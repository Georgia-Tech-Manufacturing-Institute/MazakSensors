# -*- coding: utf-8 -*-
# @author: leesoar

"""Raspberry Pi"""

import os
import platform
import re
import socket
import subprocess
import time

MAC_ADDR_PREFIX = [
    "B8:27:EB",
    "DC:A6:32",
    "E4:5F:01",
    "B8-27-EB",
    "DC-A6-32",
    "E4-5F-01",
]


def get_cur_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()


def ping(ip):
    if not ip:
        return

    prefix = ip.rsplit(".", maxsplit=1)[0]

    with open(os.devnull, mode="w") as devnull:
        processes = [subprocess.Popen(f"ping {prefix}.{x}", shell=True, stdout=devnull, stderr=devnull)
                     for x in range(0x1, 0xff)]

    time.sleep(1)
    for process in processes:
        process.terminate()


def get_raspberry_pi():
    cur_system = platform.system()
    command = f"""arp -na | grep -i -E '{"|".join(MAC_ADDR_PREFIX)}'"""

    if "window" in cur_system.lower():
        command = f'''arp -a | findstr -i "{' '.join(MAC_ADDR_PREFIX)}"'''

    ping(get_cur_ip())

    res = os.popen(command).read()
    if not res:
        return

    devices = []
    for r in res.rstrip("\n").split("\n"):
        ip = re.search(r"(\d{1,3}\.){3}\d{1,3}", r).group()
        try:
            mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", r).group()
        except AttributeError:
            mac = "incomplete"
        try:
            net = re.search(r"on (.*?) ", r).group(1)
        except AttributeError:
            net = "unknown"
        device = {
            "ip": ip,
            "mac": mac,
            "net": net
        }
        devices.append(device)
    return devices
