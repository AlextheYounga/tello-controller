import cv2
import numpy as np
import sys

width, height = 1080, 720
fb_range = [27900, 30600]
pid = [0.4, 0.4, 0]  # Proportional, Integral, Derivative
p_error = 0

cap = cv2.VideoCapture(0)


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

    error = x - width // 2

    # Speed is equal to pid proportional * error * integral * (error - p_error)
    speed = pid[0] * error + pid[1] * (error - p_error)
    speed = int(np.clip(speed, -100, 100))

    if area > fb_range[0] and area < fb_range[1]:
        forward_backward = 0
    elif area > fb_range[1]:
        forward_backward = -20
    elif area < fb_range[0] and area != 0:
        forward_backward = 20

    if x == 0:
        speed = 0
        error = 0

    print("Drone Status:", drone, "Speed", speed, "Forward Backward", forward_backward)

    return error


drone = 'setup'

while True:
    try:
        _, img_capture = cap.read()

        img_capture = cv2.resize(img_capture, (width, height))

        img_face_capture, face_stats = find_face(img_capture)

        p_error = track_face(face_stats, p_error)

        # print("Center", face_stats[0], "Area", face_stats[1])
        cv2.imshow("Output", img_face_capture)
        cv2.waitKey(1)
    except:
        print('Shutting down...')
        print('Landing...')
        break
sys.exit()
