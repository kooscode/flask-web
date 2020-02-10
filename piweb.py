#! /usr/bin/python3

import os
import threading
import time
import RPi.GPIO as GPIO
from flask import  Flask, request, render_template

app = Flask(__name__)

#setup pin numbers
pin_P1 = 18
pin_P2 = 23

#using Broadcom pin numbering.
GPIO.setmode(GPIO.BCM)
#ignore warnings if channels already open
GPIO.setwarnings(False)

#setup pin as output
GPIO.setup(pin_P1, GPIO.OUT)
GPIO.setup(pin_P2, GPIO.OUT)

#default is on
GPIO.output(pin_P1, GPIO.HIGH)
GPIO.output(pin_P2, GPIO.HIGH)

#get current status
status_P1 = GPIO.input(pin_P1)
status_P2 = GPIO.input(pin_P2)

#cleanup GPIO
# GPIO.cleanup()

#pin to channel convert
def pin_to_channel(pin_in=1):

    pi_channel = pin_P1
    if (pin_in == 1 ):
        pi_channel = pin_P1

    if (pin_in == 2):
        pi_channel = pin_P2
    
    return pi_channel

#async func to reboot
def rebooter():
    time.sleep(5)
    os.system("sudo reboot")

#async func to bounce..
def bouncer(pin_bounce):
    GPIO.output(pin_bounce, GPIO.LOW)
    time.sleep(5)
    GPIO.output(pin_bounce, GPIO.HIGH)

#home
@app.route("/")
def home():
    status_P1 = GPIO.input(pin_P1)
    status_P2 = GPIO.input(pin_P2)
    return render_template("home.html", status_P1=status_P1, status_P2=status_P2)

#manual bounce
@app.route("/bounce", methods=['GET', 'POST'])
def bounce():
    bounce_task1 = threading.Thread(target=bouncer, args=(pin_P1,))
    bounce_task1.start()
    bounce_task2 = threading.Thread(target=bouncer, args=(pin_P2,))
    bounce_task2.start()
    return render_template("bounce.html")

#toggle
@app.route("/toggle", methods=['GET', 'POST'])
def toggle():
    request_pin = pin_to_channel( int(request.form["p"]) )
    status_pin = GPIO.input(request_pin)
    GPIO.output(request_pin, not status_pin)
    return render_template("toggle.html")

#manual on
@app.route("/on")
def on():
    GPIO.output(pin_P1, GPIO.HIGH)
    GPIO.output(pin_P2, GPIO.HIGH)
    return ("ON...")

#manual off
@app.route("/off")
def off():
    GPIO.output(pin_P1, GPIO.LOW)
    GPIO.output(pin_P2, GPIO.LOW)
    return ("OFF...")

#system reboot
@app.route("/reboot", methods=['GET', 'POST'])
def reboot():
    reboot_task = threading.Thread(target=rebooter)
    reboot_task.start()
    return ("Rebooting in 5 seconds!")

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8000, debug=True)

