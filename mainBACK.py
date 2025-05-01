import max7219
from machine import Pin, SPI, I2C
from utime import sleep
from ds3231 import * # RTC library

#=================================================================================
# Setting up the RTC
#=================================================================================
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

#=================================================================================
# Setting up the display
#=================================================================================
# initialise SPI bus and pins
spi = SPI(0, baudrate=1000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

# define the message to scroll and its length
msg = "Starting.."
length = len(msg)
length = (length*8) #calculate the numbr of columns to scroll

# Create matrix display instance, which has four MAX7219 devices.
display = max7219.Matrix8x8(spi, ss, 4)

# Set the display brightness. Value is 1 to 15.
display.brightness(1)

# clear the display
display.fill(0)
sleep(1)

#==================================================================================
# Scroll the message
#==================================================================================
while True:
    for i in range(32, -length, -1):
        # clear the display
        display.fill(0)
        # write the message to the FRAME BUFFER
        display.text(msg, i, 0, 1)
        display.show()
        #display.scroll(-1, 0) #this seems to be doing nothing
        sleep(0.1) #scroll speed 50ms
    
    # Print the current date in the format: day/month/year
    MM = ds.get_time()[1] # month
    DD = ds.get_time()[2] # day
    YY = ds.get_time()[0] # year
    date = str(DD) + "/" + str(MM) + "/" + str(YY) # format the date string
    print("Current date and time from DS3231: ", date)

    # Print the current time in the format: hours:minutes:seconds
    hh = ds.get_time()[3] # hour
    mm = ds.get_time()[4] # minute
    ss = ds.get_time()[5] # second
    tt = str(hh) + ":" + str(mm) + ":" + str(ss) # format the time string
    print("Current date and time from DS3231: ", tt)
    msg = "Date -> " + date + " Time -> " + tt
    length = len(msg)
    length = (length*8) #calculate the number of columns to scroll
    sleep(0.05) # sleep 0.5sec   