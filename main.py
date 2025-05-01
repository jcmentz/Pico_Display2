import max7219
from machine import Pin, SPI
from utime import sleep

# setup SPI and CS pin (comms)
# SPI(0) is used for the MAX7219, CS pin is connected to GPIO 5
# GPIO 2 is used for SCK, GPIO 3 is used for MOSI
spi = SPI(0, baudrate=1000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

# define the message to scroll and its length
msg = "MEETING IN PROGRESS"
length = len(msg)
length = (length*8) #calculate the numbr of columns to scroll

# setup the display
display = max7219.Matrix8x8(spi, ss, 4)
display.brightness(1)
display.fill(0)
sleep(1)

while True:
    for i in range(32, -length, -1):
        display.fill(0)
        display.text(msg, i, 0, 1)
        display.show()
        #display.scroll(-1, 0) #not sure what this does, doe snto seem to impact the execution
        sleep(0.1)
    sleep(1) # sleep 1sec
    display.fill(0)
    display.show()  
    sleep(0.5) # sleep 0.5sec   