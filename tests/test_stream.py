from djitellopy import Tello
import cv2

width, height = 360, 240

drone = Tello()
drone.connect()

battery = drone.get_battery()
print(battery)

drone.streamon()

img_capture = drone.get_frame_read().frame

img_capture = cv2.resize(img_capture, (width, height))

cv2.imshow("Output", img_capture)