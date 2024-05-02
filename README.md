Documentation for the Mazak Thermocouple monitoring tool. intended integration with gas flow monitoring and powder flow ? 

# Physical Assembly
 - Raspberry Pi 4
 - x4 Adafruit Type-K Thermocouple amplifiers
 - x4 Type K Thermocouples
 - x1 [MCC DAQ HAT](https://digilent.com/shop/mcc-118-128-voltage-measurement-daq-hat-for-raspberry-pi/)
 -
# Reference Libraries
 - [DAQHAT](https://mccdaq.github.io/daqhats/install.html) 
 - [Adafruit amplifiers](https://learn.adafruit.com/ad8495-thermocouple-amplifier/python-circuitpython) 

# Device setup 
1. Reimage Pi with Raspian
2. Download/install python/pip
3. Create env
4. Clone repo
5. Prepare environment with packages from requirements.

```
pip install --upgrade pip
pip install -r requirements.txt
sudo pip install daqhats
sudo rpi-update

```

6. 
7. 
