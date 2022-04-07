# Samuel Lajoie et Maxime Gazzé
import os, sys, inspect, time, motor
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
import I2C_LCD_driver as LCD

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0, currentdir)

from Aliot.aliot import alive_iot as iot
from mainCode import iterationCode

#projectId = 'e8a2df37-e54d-4175-b640-8bc2082d60c2'
iot.ObjConnecteAlive.set_url("ws://192.168.0.102:8881/")
my_iot = iot.ObjConnecteAlive(object_id = "3e273ab3-38d8-4d0a-984e-589fd39e3a84")

stationnement = False

led_red_pin = 23
led_green_pin = 24

led_red = LED(led_red_pin)
led_green = LED(led_green_pin)

def stationnement_lights_open(isOpen):
    if isOpen:
        led_red.off()
        led_green.on()
    else:
        led_red.on()
        led_green.off()

# set light to red on start
stationnement_lights_open(False)

@my_iot.on_recv(action_id=10)
def activateLight(value):
    global stationnement
    stationnement = True
    my_iot.update_doc({'/documents/ouvert': True})

@my_iot.on_recv(action_id=20)
def activateLight(value):
    global stationnement
    stationnement = False
    my_iot.update_doc({'/documents/ouvert': False})


@my_iot.main_loop()
def main():
    try:
        global stationnement
        stationnement = my_iot.get_field('/document/ouvert')
        while True:
            while stationnement == True:

                lcd = LCD.lcd()
                visites = iterationCode(my_iot, lcd)

                if visites == None:
                    break

                my_iot.update_doc({'/documents/visites/nombre': int(visites[2:])})
                stationnement_lights_open(True)
                motor.tourner()
                stationnement_lights_open(False)
                sleep(6.1)

    except KeyboardInterrupt:
        print('interrupted!')
        GPIO.cleanup()

my_iot.begin()
GPIO.cleanup()
