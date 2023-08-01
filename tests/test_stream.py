from djitellopy import Tello
import cv2

drone = Tello()

drone.connect()
print(drone.get_battery())

drone.streamon()

try:
    frame_reader = drone.get_frame_read()
    while True:
        cv2.imshow("Tello Stream", frame_reader.frame)
        c = cv2.waitKey(1)
except KeyboardInterrupt:
    drone.end()
    cv2.destroyAllWindows()
