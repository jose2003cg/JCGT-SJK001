import WebGUI
import HAL
import Frequency
import cv2

KP = 0.0105
KD = 0.0085
KI = 0.000001  
V_MAX = 8.8
V_MIN = 3.20
IMG_CENTER = 320

last_err = 0
integral = 0

while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30,255,255))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cX = M["m10"] / M["m00"]
            err = IMG_CENTER - cX

            derivative = err - last_err

            integral += err

            w_dyn = KP * err + KD * derivative + KI * integral

            v_dyn = V_MAX - ((abs(err) / IMG_CENTER) * (V_MAX - V_MIN))

            HAL.setV(v_dyn)
            HAL.setW(w_dyn)

            last_err = err  
            HAL.setV(0)
            HAL.setW(0)
    else:
        HAL.setV(0)
        HAL.setW(0)
        
    WebGUI.showImage(img)
