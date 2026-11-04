#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port, Stop, Button
from pybricks.tools import wait
import socket

ev3 = EV3Brick()

motor_a = Motor(Port.A)
motor_b = Motor(Port.B)
motor_c = Motor(Port.C)

ir_sensor = InfraredSensor(Port.S1)

POWER = 1050
MOTOR_A = 1000
MOTOR_B = 1200
MOTOR_C = 2200

PC_IP = "10.0.0.125"
PC_PORT = 5555

def control_motor(motor, duration, power=POWER, reverse=False):
    if reverse:
        power = -power

    motor.run_time(power, duration, then=Stop.HOLD, wait=True)
    motor.run_time(-power, duration, then=Stop.HOLD, wait=True)

def send_video_signal():
    """Send signal to PC to start video sequence"""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"START_VIDEO", (PC_IP, PC_PORT))
        print("Signal sent!")
    except OSError as error:
        print("Could not send video signal: {}".format(error))
    finally:
        if sock is not None:
            sock.close()

ev3.speaker.say("Ready")
print("Infrared Remote Control Active")
print("Button Right Up: Right Arm (A)")
print("Button Left Up: Left Arm (B)")
print("Button Left Down: Forward (C)")
print("Button Right Down: Play Videos on PC")

while True:
    buttons = ir_sensor.buttons(channel=1)

    if buttons:
        print("Button(s) pressed: {}".format(buttons))
        if buttons[0] == Button.RIGHT_UP:
            control_motor(motor_a, MOTOR_A)
            wait(500)

        elif buttons[0] == Button.LEFT_UP:
            control_motor(motor_b, MOTOR_B, reverse=True)
            wait(500)

        elif buttons[0] == Button.LEFT_DOWN:
            control_motor(motor_c, MOTOR_C)
            wait(500)

        elif buttons[0] == Button.RIGHT_DOWN:
            send_video_signal()
            wait(500)

    wait(100)
