import getUploads as gu
import RPi.GPIO as GPIO
from time import sleep
import sys

# setup
filename = "vids.txt"
channelname = str(sys.argv[1])

#servo
servopin = 12
#duty cycles
servodown = 5   # %
servoup = 10    # %

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT)

servo = GPIO.PWM(servopin, 50)

vidsnumber = gu.getUploadsNumber(channelname)

def rewrite(name):
    f = open(name, 'w')
    f.write(str(vidsnumber))
    f.close()

# code
try:

    myfile = open('vids.txt', 'r')

except FileNotFoundError:

    rewrite(filename)
    servo.start(servodown)
    servo.stop()
    GPIO.cleanup()
    exit()

else:

    try:

        storednumber = int(myfile.read()) 

    # if file has bogus content
    except ValueError:

        myfile.close()
        rewrite(filename)
        exit()

    # nothiog changed
    if storednumber == vidsnumber:

        myfile.close()
        servo.start(servodown)

    # erronious number in file or some videos have been deleted
    elif vidsnumber < storednumber:

        myfile.close()
        rewrite(filename)

    # new videos!
    else:

        myfile.close()
        # rewrite the file
        rewrite(filename)
        # raise the servo
        servo.start(servoup)
    
    sleep(.5)
    servo.stop()
    GPIO.cleanup()
    # lower the servo
