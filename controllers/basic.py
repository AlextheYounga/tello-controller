from djitellopy import Tello
import time


drone = Tello()

drone.connect()

battery = drone.get_battery()
print(drone.get_battery())

drone.takeoff()
time.sleep(1)

drone.move_forward(200)

drone.move_back(200)

drone.land()
