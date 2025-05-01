import max7219
from machine import Pin, SPI, I2C
from utime import sleep
from ds3231 import *

# Define the pins for I2C communication
sdaPIN = Pin(0) # SDA pin for I2C
sclPIN = Pin(1,Pin.IN) # SCL pin for I2C

# Initialize the I2C interface with the specified pins
i2c = I2C(0, scl=sclPIN, sda=sdaPIN, freq=400000) # create I2C object with pins and frequency
time.sleep(0.5) # wait for I2C to stabilize

# test I2C connection
devices = i2c.scan() # scan for devices on the I2C bus
if len(devices) == 0:
    print("No I2C devices found!")
for device in devices:
    print("I2C device found at address:", hex(device))

# Create an instance of the DS3231 class for interfacing with the DS3231 RTC
ds = DS3231(i2c)

# Set the DS3231 RTC to current system time
ds.set_time()
date = ds.get_time() # get the current date and time from the DS3231
print("Current date and time from DS3231: ", str(ds.get_time()[4]))

# Print the current date in the format: month/day/year
print( "Date={}/{}/{}" .format(ds.get_time()[1], ds.get_time()[2],ds.get_time()[0]) )

# Print the current time in the format: hours:minutes:seconds
print( "Time={}:{}:{}" .format(ds.get_time()[3], ds.get_time()[4],ds.get_time()[5]) )