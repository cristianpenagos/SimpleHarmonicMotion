import cv2
import numpy as np
import math

# Variables globales
pauseVideo = False
viewPixel = False
x, y = 0, 0
prev_cX, prev_cY = None, None
scale_cm_per_px = 2.5 / 178  # Escala de conversión
fps = 30  # Fotogramas por segundo

def mouse_callback(event, _x, _y, flags, param):
    global pauseVideo, viewPixel, x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = _x, _y
        viewPixel = True
    if event == cv2.EVENT_RBUTTONDOWN:
        pauseVideo = not pauseVideo

# Cargar video
videoPath = 'MAS4.MOV'
cap = cv2.VideoCapture(videoPath)

if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

# Obtener fps del video
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30  # Valor predeterminado si no se puede obtener

newWidth = 1080
newHeight = 680

def nothing(x):
    pass

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_callback)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("H Min", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Max", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Max", "Trackbars", 255, 255, nothing)

while True:
    if not pauseVideo:
        ret, frame = cap.read()
        if not ret:
            break
        frame2 = np.copy(frame)

    if viewPixel:
        pixelColor = frame[y, x]
        frame2 = np.copy(frame)
        cv2.putText(frame2, f'Posición (x, y): ({x}, {y}) Color: {pixelColor}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame3 = cv2.resize(frame2, (newWidth, newHeight))
    hsv = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("H Min", "Trackbars")
    h_max = cv2.getTrackbarPos("H Max", "Trackbars")
    s_min = cv2.getTrackbarPos("S Min", "Trackbars")
    s_max = cv2.getTrackbarPos("S Max", "Trackbars")
    v_min = cv2.getTrackbarPos("V Min", "Trackbars")
    v_max = cv2.getTrackbarPos("V Max", "Trackbars")

    bajo = np.array([h_min, s_min, v_min])
    alto = np.array([h_max, s_max, v_max])
    mascara = cv2.inRange(hsv, bajo, alto)

    contours, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Calcular velocidad si hay una posición previa
                if prev_cX is not None and prev_cY is not None:
                    dx = cX - prev_cX
                    dy = cY - prev_cY
                    distancia_px = math.hypot(dx, dy)
                    velocidad_cm_s = distancia_px * scale_cm_per_px * fps
                    cv2.putText(frame3, f"Velocidad: {velocidad_cm_s:.2f} cm/s", (cX + 10, cY + 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                # Dibujar contorno y centroide
                cv2.drawContours(frame3, [contour], -1, (0, 239, 255), 2)
                cv2.circle(frame3, (cX, cY), 5, (255, 255, 255), -1)
                cv2.putText(frame3, "Centroide", (cX - 25, cY - 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Actualizar posición previa
                prev_cX, prev_cY = cX, cY

    cv2.imshow('Video con contornos', frame3)
    cv2.imshow('Video mascara', mascara)
    cv2.imshow('Video', hsv)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()