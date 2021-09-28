# Receiving messages
HOST = 'localhost'
PORT = 5000

# Sending messages
PD_HOST = 'localhost'
PD_PORT = 8000
SEND_INTERVAL = 100 # (ms)
numSensor = 4

import threading
import time
import random

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

# from adafruit_servokit import ServoKit
# robot = ServoKit(channels=16)

def receive_servo_data(address, *args):
  servoID = int(args[0])
  servoAngle = args[1]
  # robot.servo[servoID].angle = servoAngle

  print("servoID:", servoID, "angle:", servoAngle)


def send_sensor_data(client):
  while True:
    accel_data = [random.random() for n in range(numSensor)]
    client.send_message("/accel", accel_data)

    time.sleep(SEND_INTERVAL/1000.0)

    # accel_data = []
    # for i in range(len(numMPU)):
    #   for j in range(3):
    #     accel_data.append(numMPU[i].acceleration[j])


def start_server():
  message_handler = dispatcher.Dispatcher()
  message_handler.map("/servo", receive_servo_data)

  server = osc_server.ThreadingOSCUDPServer((HOST, PORT), message_handler)
  print("Serving on {}".format(server.server_address),'\n')

  thread = threading.Thread(target=server.serve_forever)
  thread.start()


def start_client():
  client = udp_client.SimpleUDPClient(PD_HOST, PD_PORT)

  thread = threading.Thread(target=send_sensor_data(client))
  thread.start()


if __name__ == "__main__":
  start_server()
  start_client()
