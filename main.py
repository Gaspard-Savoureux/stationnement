# Samuel Lajoie et Maxime Gazzé
import os, sys, inspect, time, motor
import RPi.GPIO as GPIO
from time import sleep

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0, currentdir)

from Aliot.aliot import alive_iot as iot
from mainCode import iterationCode

projectId = 'e8a2df37-e54d-4175-b640-8bc2082d60c2'
iot.ObjConnecteAlive.set_url("wss://alivecode.ca/iotgateway/")
my_iot = iot.ObjConnecteAlive(object_id = "06ba2eda-60e5-48f7-8d4e-4da9efff35ac")

stationnement = False

@my_iot.on_recv(action_id=10)
def activateLight(value):
    global stationnement
    stationnement = True


@my_iot.on_recv(action_id=20)
def activateLight(value):
    global stationnement
    stationnement = False


@my_iot.main_loop()
def main():
    try:
        global stationnement
        # Tester le get field
        #stationnement = my_iot.get_field(projectId, '/documents/ouvert')
        #print(stationnement)
        while True:
            while stationnement == True:
                visites = iterationCode()

                if visites == None:
                    break
                visites = str(visites)
                compteur = 0
                while compteur < 200:
                    compteur += 1

                my_iot.update(projectId, {'/documents/visites/nombre': int(visites[2:])})
                motor.tourner()

    except KeyboardInterrupt:
        print('interrupted!')
        GPIO.cleanup()

my_iot.begin()
GPIO.cleanup()
