#!/usr/bin/env python

import time
import Adafruit_ADS1x15
import smbus

def sht31(var,bus_num):
    
    # Get I2C bus
    bus = smbus.SMBus(bus_num)
     
    # SHT31 address, 0x44(68)
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
     
    time.sleep(0.5)
     
    # SHT31 address, 0x44(68)
    # Read data back from 0x00(00), 6 bytes
    # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
     
    # Convert the data
    tmp = data[0] * 256 + data[1]
    temperature = -45 + (175 * tmp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    if var=="temp":
        return temperature
    elif var=="hum":
        return humidity
    else:
        return [humidity, temperature]

def ads1115_4ch(address_num,bus_num):

    adc = Adafruit_ADS1x15.ADS1115(address=address_num, busnum=bus_num)

    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 2/3

    while True:
        values = [0]*4
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)
        return values

def main():

    values=ads1115_4ch(0x48,1)
    print(values)
    temp=sht31("both",1)
    print(temp)


if __name__ == "__main__":
    main()
