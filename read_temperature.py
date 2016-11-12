#!/usr/bin/env python3

import smbus
import time
from bitstring import BitArray

I2C_BUS = 1 # /dev/i2c-1

# Device address
DS1621_ADDRESS      = 0x48

# DS1621 commands
ACCESS_CONFIG       = 0xAC
START_CONVERT       = 0xEE
READ_TEMPERATURE    = 0xAA

# DS1621 status register flags
ONE_SHOT            = 0x01
DONE                = 0x80


bus = smbus.SMBus(I2C_BUS)

# Reading status register.
status_reg = bus.read_byte_data(DS1621_ADDRESS, ACCESS_CONFIG)

# Setting one shot flag.
status_reg |= ONE_SHOT
bus.write_byte_data(DS1621_ADDRESS, ACCESS_CONFIG, status_reg)

print("Start conversion.")
bus.write_byte(DS1621_ADDRESS, START_CONVERT)

while True:
    status_reg = bus.read_byte_data(DS1621_ADDRESS, ACCESS_CONFIG)
    print(".", end="", flush=True)
    if status_reg & DONE == DONE:
        print("")
        break
    time.sleep(0.1)
        
print("Conversion done.")
print("Reading temperature.")
temperature = bus.read_word_data(DS1621_ADDRESS, READ_TEMPERATURE)

print("Temperature value read from device:", format(temperature, "#06X"))

lsb = temperature & 0xFF00
lsb >>= 8
msb = temperature & 0x00FF

bit_array = BitArray(int=msb, length=8)

decimal = 0
if lsb == 0x80:
    decimal = 0.5

temperature_celsius = bit_array.int + decimal
temperature_fahrenheit = (temperature_celsius * 9) / 5 + 32

print(
    "Temperature: {0:.1f} °C = {1:.1f} °F"
    .format(temperature_celsius, temperature_fahrenheit)
)

