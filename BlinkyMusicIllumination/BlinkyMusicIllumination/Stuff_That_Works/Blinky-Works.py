#!/usr/bin/env python
#
# Command Line usage:
#   xmas.py <input sequence> <audio file>

import RPi.GPIO as GPIO, time
import sys
import time
import pygame
import random

#This is the array that stores the SPI sequence
set = bytearray(25 * 3)

#blinks is used to handle the Star Blinking Effect
blinks = bytearray(25 * 3)
blink_active = int(-1)
blink_max    = int(0)
blink_R1      = int(0)
blink_G1      = int(0)
blink_B1      = int(0)
blink_R2      = int(0)
blink_G2      = int(0)
blink_B2      = int(0)

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE
logical_map = [0 for i in range(9)]

# Defines the mapping of the GPIO1-8 to the pin on the Pi
# GPIO     0,01,02,3,04,05,06,07,8          
pin_map = [0,11,12,8,15,16,18,22,7]
# print getRaspiModel(GPIO.RPI_INFO['REVISION'])
#Sequence   PIN     GPIO
#   3       8       14
#   4       16      23
#   5       11      17
#   7       14      22
#   8       12      18       

#####################################################################


# Setup the board
GPIO.setmode(GPIO.BOARD)
for i in range(1,9):
  GPIO.setup(pin_map[i], GPIO.OUT)
time.sleep(2.0);
dev    = "/dev/spidev0.0"
spidev = file(dev,"wb")


# Calculate gamma correction
gamma = bytearray(256)
for i in range(256):
  gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)



# Open the setup config file and parse it to determine 
# how GPIO1-8 are mapped to logical 1-8
with open("setup.txt",'r') as f:
  data = f.readlines()
  i=0
  for i in range(8):
    logical_map[i+1] = int(data[i])

# Open the input sequnce file and read/parse it
with open(sys.argv[1],'r') as f:
  seq_data = f.readlines()
  for i in range(len(seq_data)):
    seq_data[i] = seq_data[i].rstrip()

# Current light states
lights = [False for i in range(8)]

# Load and play the music
pygame.mixer.init()
pygame.mixer.music.load(sys.argv[2])
pygame.mixer.music.play()

# Start sequencing
start_time = int(round(time.time()*1000))
step       = 1 #ignore the header line 
while True :
  next_step = seq_data[step].split(",");
  next_step[1] = next_step[1].rstrip()
  cur_time = int(round(time.time()*1000)) - start_time

  # time to run the command
  if int(next_step[0]) <= cur_time:

    print next_step
    # if the command is Relay 1-8 
    if next_step[1] >= "1" and next_step[1] <= "8":

      # change the pin state
      if next_step[2] == "1":
        GPIO.output(pin_map[logical_map[int(next_step[1])]],True)
      else:
        GPIO.output(pin_map[logical_map[int(next_step[1])]],False)

    # Check for star commands 
    if next_step[1].rstrip() == "BLINK":
      blink_active = 0
      blink_max    = int(next_step[2])
      blink_R1     = int(next_step[3])
      blink_G1     = int(next_step[4])
      blink_B1     = int(next_step[5])
      blink_R2     = int(next_step[6])
      blink_G2     = int(next_step[7])
      blink_B2     = int(next_step[8])
      for i in range(25):
         blinks[i*3] = 0
         blinks[i*3+1] = 0
         blinks[i*3+2] = 0
      blink_next_time   = int(round(time.time()*1000)) - start_time
    if next_step[1].rstrip() == "BLINK_END":
      blink_active = -1
    if next_step[1].rstrip() == "STAR_VERT":
      star_vert(next_step[2],next_step[3],next_step[4], next_step[5], next_step[6], next_step[7], next_step[8])
    if next_step[1].rstrip() == "STAR_TIPS":
      star_tips(next_step[2],next_step[3],next_step[4], next_step[5], next_step[6], next_step[7])
    if next_step[1].rstrip() == "STAR_SOLID":
      star_solid(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_INSIDE_SOLID":
      star_inside_solid(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_POINT1":
      star_point1(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_POINT2":
      star_point2(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_POINT3":
      star_point3(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_POINT4":
      star_point4(next_step[2],next_step[3],next_step[4])
    if next_step[1].rstrip() == "STAR_POINT5":
      star_point5(next_step[2],next_step[3],next_step[4])

    # if the END command
    if next_step[1].rstrip() == "END":
      for i in range(1,9):
        GPIO.output(pin_map[logical_map[i]],False)
      break
    step += 1

  # ----------BLINKS---------------------------------
  # The following is to handle the star blink command....
  # if blinks are active and it's time
  if blink_active > -1 and cur_time > blink_next_time:
    blink_next_time = cur_time + 100
    #increment active blinks
    for i in range (25):
      if blinks[i*3]>0 or blinks[i*3+1]>0 or blinks[i*3+2]>0:
        blinks[i*3]   += blink_R1
        blinks[i*3+1] += blink_G1
        blinks[i*3+2] += blink_B1
        if blinks[i*3]==255 or blinks[i*3+1]==255 or blinks[i*3+2]==255:
          blinks[i*3]   = 0
          blinks[i*3+1] = 0
          blinks[i*3+2] = 0
          blink_active -= 1
    
    #try and get a new blink randomly
    if blink_active < blink_max and random.randrange(1,5) == 1:
      pick = random.randrange(0,24)
      if blinks[pick*3] == 0 and blinks[pick*3+1]==0 and blinks[pick*3+2]==0:
        blink_active += 1
        blinks[pick*3]   = blink_R1
        blinks[pick*3+1] = blink_G1
        blinks[pick*3+2] = blink_B1

    #push out the serial
    for i in range (25):
      if blinks[i*3]==0 and blinks[i*3+1]==0 and blinks[i*3+2]==0:
        set[i*3]   = blink_R2
        set[i*3+1] = blink_G2
        set[i*3+2] = blink_B2
      else:
        set[i*3]   = blinks[i*3]
        set[i*3+1] = blinks[i*3+1]
        set[i*3+2] = blinks[i*3+2]

    spidev.write(set)
    spidev.flush()
  # ------END-BLINKS---------------------------------

