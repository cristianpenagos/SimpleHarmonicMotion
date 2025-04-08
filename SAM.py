import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


#Variables Globales
pauseVideo = False
viewPixel = False

#Mouse Collback
def mouse_callback(event, _x, _y, flags, param):
    global pauseVideo, viewPixel, x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = _x, _y
        viewPixel = True
    if event == cv2.EVENT_RBUTTONDOWN:
        pauseVideo = not pauseVideo

#Video Load

videoPath = 'MAS.MOV'
cap = cv2.VideoCapture(videoPath)

#Create Window and config callback mouse
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_callback)

while True:
    if not pauseVideo:
        ret, frame = cap.read()
        frame2 = np.copy(frame)
        if not ret:
            break
    if viewPixel:
        pixelColor = frame[y, x] #Obtain pixel color Value
        frame2 = np.copy(frame)
        cv2.putText(frame2, f'position (x, y): ({x}, {y}) color: {pixelColor}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Video', frame2)
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC key to exit
        break
cap.release()
cv2.destroyAllWindows()