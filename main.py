# Samuel Lajoie, Maxime Gazzé, Miguel Boka et Edgar Pereda Puig
import os, sys, inspect, time, cadrant, motor
import RPi.GPIO as GPIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from aliot.aliot import alive_iot as iot
from mainCode import iterationCode

projectId = 'e8a2df37-e54d-4175-b640-8bc2082d60c2'
iot.ObjConnecteAlive.set_url("wss://alivecode.ca/iotgateway/")
my_iot = iot.ObjConnecteAlive(key="06ba2eda-60e5-48f7-8d4e-4da9efff35ac")

stationnement = False

@my_iot.on_recv(action_id=10)
def activateLight(value):
    global stationnement
    stationnement = True


@my_iot.on_recv(action_id=20)
def activateLight(value):
    global stationnement
    stationnement = False


@my_iot.main_loop(1)
def main():
    try:
        global stationnement
        while True:
            while stationnement == True:
                visites = str(iterationCode())
                print(visites)
                compteur = 0
                try:
                    while compteur < 200:
                        compteur += 1
                    my_iot.send_route(projectId + '/entree', {'nbVisites': visites[2:]})
                    motor.tourner()
                except:
                    pass

    except KeyboardInterrupt:
        print('interrupted!')
        GPIO.cleanup()

my_iot.begin()
GPIO.cleanup()
