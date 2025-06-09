import cv2 as cv
import mediapipe as mp
import os

x1 = y1 = x2 = y2 = 0
webcam = cv.VideoCapture(0)
mpHands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    success, image = webcam.read()
    if not success:
        break

    image = cv.flip(image, 1)
    frame_height, frame_width, frame_depth = image.shape
    imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = mpHands.process(imgRGB)
    hands = results.multi_hand_landmarks
    # print(results.multi_hand_landmarks)
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv.circle(img=image, center=(x,y), radius=8, color=(0,255,255), thickness=3)
                    x1, y1 = x, y
                if id == 4:
                    cv.circle(img=image, center=(x,y), radius=8, color=(0,0,255), thickness=3)
                    x2, y2 = x, y

        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5) // 4
        cv.line(image, (x1,y1), (x2,y2), (0,255,0), 5)
        if dist > 50:
            os.system("pactl set-sink-volume @DEFAULT_SINK@ +5%")
        else:
            os.system("pactl set-sink-volume @DEFAULT_SINK@ -5%")

    cv.imshow('Image', image)
    key = cv.waitKey(1)
    if key == 27:
        break

webcam.release()
cv.destroyAllWindows()