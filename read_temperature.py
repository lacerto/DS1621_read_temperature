#!/usr/bin/env python3

import smbus
import time
from bitstring import BitArray

def start_conversion(bus, address):
    # DS1621 commands
    ACCESS_CONFIG       = 0xAC
    START_CONVERT       = 0xEE
    
    # DS1621 status register flags
    ONE_SHOT            = 0x01
    DONE                = 0x80
    
    # Reading status register.
    status_reg = bus.read_byte_data(address, ACCESS_CONFIG)
    
    # Setting one shot flag.
    status_reg |= ONE_SHOT
    bus.write_byte_data(address, ACCESS_CONFIG, status_reg)
    
    print("Start conversion.")
    bus.write_byte(address, START_CONVERT)
    
    while True:
        status_reg = bus.read_byte_data(address, ACCESS_CONFIG)
        print(".", end="", flush=True)
        if status_reg & DONE == DONE:
            print("")
            break
        time.sleep(0.1)
            
    print("Conversion done.")
    return True
    
def read_temp_hex(bus, address):
    # DS1621 commands
    READ_TEMPERATURE    = 0xAA
    
    print("Reading hex temperature.")
    temperature = bus.read_word_data(address, READ_TEMPERATURE)    
    print("Temperature value read from device:", format(temperature, "#06X"))
    return temperature    

def convert_hex_to_celsius(temperature):
    lsb = temperature & 0xFF00
    lsb >>= 8
    msb = temperature & 0x00FF
    
    bit_array = BitArray(uint=msb, length=8)
    
    decimal = 0
    if lsb == 0x80:
        decimal = 0.5
    
    return bit_array.int + decimal    

def convert_celsius_to_fahrenheit(temp_c):
    return (temp_c * 9) / 5 + 32

def read_temperature(bus, address):

    # DS1621 commands
    READ_TEMPERATURE    = 0xAA
    
    temperature_celsius = -1000
    
    if start_conversion(bus, address):    
        temperature = read_temp_hex(bus, address)        
        temperature_celsius = convert_hex_to_celsius(temperature)
        
    return temperature_celsius
    

if __name__ == "__main__":
    I2C_BUS = 1 # /dev/i2c-1

    # Device address
    DS1621_ADDRESS = 0x48    

    bus = smbus.SMBus(I2C_BUS)
    
    temp_c = read_temperature(bus, DS1621_ADDRESS)
    temp_f = convert_celsius_to_fahrenheit(temp_c)
    
    print("Temperature: {0:.1f} °C = {1:.1f} °F".format(temp_c, temp_f))
    
