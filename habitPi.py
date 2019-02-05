# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Edit by Abhinuv Nitin Pitale https://abhinuvpitale.github.io
# App created to measure your habits and keep a track of them!


import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Custom Imports, the ones I added later
import datetime
import json

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 


GPIO.setmode(GPIO.BCM) 

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Get default fonts
font = ImageFont.load_default()

# String to show Time
strTime = ''

filer = open("habits.json")
json_data = filer.read()
data = json.loads(json_data)
filer.close()
keys = data.keys()
values = data.values()

print keys
print values

habit1 = keys[0]
habit2 = keys[1]

habit1Value = data[habit1][0]
habit2Value = data[habit2][0]

habit1History = str(data[habit1][1])
habit2History = str(data[habit2][1])

prevDay = (datetime.datetime.now()-datetime.timedelta(hours=5)).day

updateDay = 0;

addHabit1 = 1;
addHabit2 = 1;

u_pin_old = -1
d_pin_old = -1
l_pin_old = -1
r_pin_old = -1

try:
    while 1:
        currTime = datetime.datetime.now()-datetime.timedelta(hours=5)
        currDay = currTime.day
        strTime = str((currTime).strftime("%Y-%m-%d")) 
        daysLeft = datetime.datetime(2019, 12, 31) - datetime.datetime.now()
        daysLeft = daysLeft.days
          
        # Check for Pin Press
        u_pin = GPIO.input(U_pin)
        d_pin = GPIO.input(D_pin)
        l_pin = GPIO.input(L_pin)
        r_pin = GPIO.input(R_pin)

        if u_pin == 1 and u_pin_old == 0 and addHabit1 == 1:
                habit1Value = habit1Value + 1
                addHabit1 = 0
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                print "Up Pressed \n"
        if d_pin == 1 and d_pin_old == 0 and addHabit1 == 0:
                habit1Value = habit1Value - 1
                addHabit1 = 1
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                print "Down Pressed \n"
        if l_pin == 1 and l_pin_old == 0 and addHabit2 == 0:
                habit2Value = habit2Value - 1
                addHabit2 = 1
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                print "Left Pressed \n"
        if r_pin == 1 and r_pin_old == 0 and addHabit2 == 1:
                habit2Value = habit2Value + 1
                addHabit2 = 0
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                print "Right Pressed \n"
        
        # Check if Same Day
        if currDay != prevDay:
            updateDay = 1
        if updateDay == 1:
            if addHabit1 == 0:
                habit1History = 'X' + habit1History[0:-1]
            else:
                habit1History = '-' + habit1History[0:-1]
            if addHabit2 == 0:
                habit2History = 'X' + habit2History[0:-1]
            else:
                habit2History = '-' + habit2History[0:-1]
                
                
            data[habit1] = [habit1Value, habit1History]
            data[habit2] = [habit2Value, habit2History]
            filer = open("habits.json","w+")
            filer.write(json.dumps(data))
            updateDay = 0
            addHabit1 = 1
            addHabit2 = 1

        # Draw the Text Here
        draw.text((0,0), strTime+"   "+str(daysLeft)+"/365",font=font ,fill=255)
        draw.text((0,10), str(habit1)+" : "+str(habit1Value), font=font, fill=255)
        draw.text((0,18),str(habit1History),font=font, fill=255)
        draw.text((0,26), str(habit2)+" : "+str(habit2Value), font=font, fill=255)
        draw.text((0,34),str(habit2History), font=font, fill=255)
        disp.image(image)
        disp.display()   
        time.sleep(.1) 
        prevDay = currDay
        u_pin_old = u_pin
        d_pin_old = d_pin
        l_pin_old = l_pin
        r_pin_old = r_pin

except KeyboardInterrupt: 
    GPIO.cleanup()
