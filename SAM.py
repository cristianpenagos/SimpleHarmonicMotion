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
    if event == cv2.EVENT_LBUTTONDOWN:              #Left click pixel coordinates
        x, y = _x, _y
        viewPixel = True
    if event == cv2.EVENT_RBUTTONDOWN:              #Right click pause video
        pauseVideo = not pauseVideo

#Video Load

videoPath = 'MAS.MOV'                                   # Path to video file
cap = cv2.VideoCapture(videoPath)

#Validate is cap is opened
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    print("Video opened successfully.")

newWidth = 880                                       #New width of the video
newHeight = 680                                    #New height of the video

upper_limit = np.array([225,120,35])
lower_limit = np.array([221,118,31])                #Upper limit of the video

def nothing(x):
    pass


#Create Window and config callback mouse
cv2.namedWindow('Video')                                #Name of the window video
cv2.setMouseCallback('Video', mouse_callback)           #Set mouse callback function


# create window trackbar for color change
cv2.namedWindow("Trackbars")
cv2.createTrackbar("H Min", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Max", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Max", "Trackbars", 255, 255, nothing)

# Centroid calculation function

#Centroid distannce calculation function

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)** + (y2 - y1)**2)

    




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
    
    frame3 = cv2.resize(frame2, (newWidth, newHeight)) 
    # BGR to HSV Converter
    hsv = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    # read trackbar positions
    h_min = cv2.getTrackbarPos("H Min", "Trackbars")
    h_max = cv2.getTrackbarPos("H Max", "Trackbars")
    s_min = cv2.getTrackbarPos("S Min", "Trackbars")
    s_max = cv2.getTrackbarPos("S Max", "Trackbars")
    v_min = cv2.getTrackbarPos("V Min", "Trackbars")
    v_max = cv2.getTrackbarPos("V Max", "Trackbars")

    # Create color range for mask
    bajo = np.array([h_min, s_min, v_min])
    alto = np.array([h_max, s_max, v_max])
    ## binarizar imagen
    mascara = cv2.inRange(hsv, bajo, alto)

    cv2.imshow('Video mascara', mascara)
    cv2.imshow('Video', hsv)

    #cv2.imshow('Video', frame2)
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC key to exit
        break
cap.release()
cv2.destroyAllWindows()