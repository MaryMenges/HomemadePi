import RPi.GPIO as GPIO
import MFRC522
import Stepper
import signal

motor = Stepper.Stepper()
authcode = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
continue_reading = True
direction = 0

def motor_func():
    print("Start Motor")
    global direction
    if direction == 0:
        motor.clockwise()
        direction = 1
    else:
        motor.counterclockwise()
        direction = 0
    print("Stop Motor")

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the garage"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card Detected"
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            # Read block 8
            data = MIFAREReader.MFRC522_Read(8)
            if data[:16] == authcode:
                motor_func()
            else:
                print("Invalid Card")
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Failure")
