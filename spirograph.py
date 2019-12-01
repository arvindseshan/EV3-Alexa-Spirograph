#!/usr/bin/python3

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent, LargeMotor
from ev3dev2.sensor.lego import InfraredSensor
import time

print("loaded spirograph")

def spirograph(pattern):
    D = 0 #table
    C = 0 #left
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_C)
    turnTable = LargeMotor(OUTPUT_D)
    if pattern == 1 :
        D=30
        A=30
        C=30
    if pattern == 2 :
        D=7
        A=50
        C=0
    if pattern == 3 :
        D=30
        A=-30
        C=30
    if pattern == 4 :
        D=30
        A=-30
        C=30
    if pattern == 5 :
        D=10
        A=-20
        C=20
    turnTable.on(SpeedPercent(D))
    tank_drive.on(C, A)
    time.sleep(25)
    turnTable.on(SpeedPercent(0))
    tank_drive.on(0, 0)