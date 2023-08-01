from djitellopy import Tello
import time


tello = Tello()

tello.connect()

battery = tello.get_battery()
print(tello.get_battery())

tello.takeoff()

tello.move_forward(200)

tello.move_back(200)

tello.land()
