import cv2
import numpy as np
from djitellopy import tello
import time
import sys


width, height = 1080, 720
fb_range = [27900, 30600]
pid = [0.4, 0.4, 0]  # Proportional, Integral, Derivative
p_error = 0


def find_face(img_capture):
    face_cascade = cv2.CascadeClassifier("resources/haarcascades/haarcascade_frontalface_default.xml")

    img_gray = cv2.cvtColor(img_capture, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.2, 8)

    face_center_list = []
    face_area_list = []

    for (x, y, w, h) in faces:
        red = (0, 0, 255)
        green = (0, 255, 0)

        center_x = x + w // 2
        center_y = y + h // 2
        center = [center_x, center_y]
        area = w * h

        # Draw box around face and add green dot to center
        cv2.rectangle(img_capture, (x, y), (x + w, y + h), red, 2)
        cv2.circle(img_capture, (center_x, center_y), 2, green, cv2.FILLED)

        face_center_list.append(center)
        face_area_list.append(area)

    if len(face_area_list) != 0:
        i = face_area_list.index(max(face_area_list))  # index of greatest area value in list

        face_center = face_center_list[i]
        face_area = face_area_list[i]

        return img_capture, [face_center, face_area]
    else:
        return img_capture, [[0, 0], 0]


def track_face(face_stats, p_error):
    area = face_stats[1]
    x, y = face_stats[0]

    forward_backward = 0

    distanceFromCenter = x - width // 2

    # Speed is equal to pid proportional * distanceFromCenter * integral * (distanceFromCenter - p_error)
    speed = pid[0] * distanceFromCenter + pid[1] * (distanceFromCenter - p_error)
    speed = int(np.clip(speed, -100, 100))

    if area > fb_range[0] and area < fb_range[1]:
        forward_backward = 0
    elif area > fb_range[1]:
        forward_backward = -20
    elif area < fb_range[0] and area != 0:
        forward_backward = 20

    if x == 0:
        speed = 0
        distanceFromCenter = 0

        print("Speed", speed,
              "Forward Backward", forward_backward,
              "Center", face_stats[0],
              "Area", face_stats[1]
              )
    drone.send_rc_control(0, forward_backward, 0, speed)
    return distanceFromCenter

time.sleep(4)
drone = tello.Tello()
drone.connect()

print(drone.get_battery())

drone.streamon()

drone.takeoff()
drone.send_rc_control(0, 0, 25, 0)

time.sleep(2.1)

try:
    while True:
        frame_reader = drone.get_frame_read().frame

        frame_reader = cv2.resize(frame_reader, (width, height))

        img_face_capture, face_stats = find_face(frame_reader)

        p_error = track_face(face_stats, p_error)

        cv2.imshow("Tello Drone Footage", img_face_capture)
        cv2.waitKey(1)
except:
    print('Ending...')
    drone.end()
    cv2.destroyAllWindows()

    print('Shutting down...')
    sys.exit()
