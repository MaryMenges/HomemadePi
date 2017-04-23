# http://www.raspberrypi-spy.co.uk/

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

class Stepper:

  def rotation(self, steps):
    # use physical pin numbers to match MFRC522
    GPIO.setmode(GPIO.BOARD)

    # Define GPIO signals to use
    # Physical pins 11,15,16,18
    # GPIO17,GPIO22,GPIO23,GPIO24
    #StepPins = [17,22,23,24]
    StepPins = [11,15,16,18]

    # Set all pins as output
    for pin in StepPins:
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)

    # Define advanced sequence
    Seq = [[1,0,0,0],
           [0,1,0,0],
           [0,0,1,0],
           [0,0,0,1]]

    StepCount = len(Seq)

    # Read wait time from command line
    if len(sys.argv)>1:
      WaitTime = int(sys.argv[1])/float(1000)
    else:
      WaitTime = 10/float(1000)

    # Initialise variables
    StepCounter = 0
    count = 0

    # Start main loop
    while (count < steps):
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
      StepCounter += StepDir
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount+StepDir
      # Wait before moving on
      time.sleep(WaitTime)
      count = count + 1

  def clockwise(self):
    global StepDir
    StepDir = 1
    self.rotation(2048)

  def counterclockwise(self):
    global StepDir
    StepDir = -1
    self.rotation(2048)
