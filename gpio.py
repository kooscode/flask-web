import RPi.GPIO as GPIO
import time

#using Broadcom pin numbering.
GPIO.setmode(GPIO.BCM)

#setup pin as output
GPIO.setup(18, GPIO.OUT)

#ON
GPIO.output(18, GPIO.HIGH)

#OFF
GPIO.output(18, GPIO.LOW)

# #cleanup GPIO
# GPIO.cleanup()