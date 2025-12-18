import cv2
import numpy as np
import math
import time
import WebGUI as GUI
import HAL

# Coordenadas del objetivo central
TARGET_X = 33.0
TARGET_Y = -35.0

# Altura objetivo
FLIGHT_HEIGHT = 4.0

SPIRAL_SPEED = 2.05       # m/s
MAX_FOUND_VICTIMS = 6.0
SPIRAL_INCREMENT = 0.22

angle_accumulated = 0.0
radius_current = 0.0

# Carga del clasificador de caras
face_cascade_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_detector = cv2.CascadeClassifier(face_cascade_file)

drone_state = "TAKEOFF"
victims_locations = []
prev_time = time.time()

def rotate_gray(img, deg):
    center_point = tuple(np.array(img.shape[1::-1]) / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_point, deg, 1.0)
    rotated = cv2.warpAffine(img, rotation_matrix, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated

print(f"Misión iniciada: espiral centrada en [{TARGET_X}, {TARGET_Y}]")

while True:
    now = time.time()
    dt = now - prev_time
    if dt <= 0: dt = 0.01
    prev_time = now

    frame = HAL.get_ventral_image()
    drone_pos = HAL.get_position()
    x_pos, y_pos, z_pos = drone_pos

    if frame is None:
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_face = False

    # Revisamos rotaciones cada 15
    for rotation in range(0, 360, 15):
        check_frame = gray_frame if rotation == 0 else rotate_gray(gray_frame, rotation)
        faces_found = face_detector.detectMultiScale(check_frame, scaleFactor=1.2, minNeighbors=3)

        if len(faces_found) > 0:
            detected_face = True
            break

    if detected_face:
        h, w = frame.shape[:2]
        cv2.circle(frame, (w//2, h//2), 30, (0, 255, 0), 3)

        if drone_state == "SEARCH":
            is_new_victim = all(math.hypot(x_pos - vx, y_pos - vy) >= 3.0 for vx, vy in victims_locations)
            if is_new_victim:
                print(f"VÍCTIMA DETECTADA en ({x_pos:.2f}, {y_pos:.2f})")
                victims_locations.append([x_pos, y_pos])

    GUI.showImage(frame)

    # Control de estados
    if drone_state == "TAKEOFF":
        HAL.takeoff()
        if z_pos < (FLIGHT_HEIGHT - 0.2):
            HAL.set_cmd_vel(0, 0, 1.5, 0)
        else:
            drone_state = "MOVE_TO_CENTER"

    elif drone_state == "MOVE_TO_CENTER":
        dx = TARGET_X - x_pos
        dy = TARGET_Y - y_pos
        distance = math.hypot(dx, dy)
        vz = (FLIGHT_HEIGHT - z_pos) * 0.5

        if distance < 1.0:
            print("Centro alcanzado, iniciando patrón espiral.")
            drone_state = "SEARCH"
            HAL.set_cmd_vel(0, 0, 0, 0)
        else:
            vx = max(min(dx * 0.5, 3.0), -3.0)
            vy = max(min(dy * 0.5, 3.0), -3.0)
            HAL.set_cmd_vel(vx, vy, vz, 0)

    elif drone_state == "SEARCH":
        radius_current = SPIRAL_INCREMENT * angle_accumulated
        if len(victims_locations) >= MAX_FOUND_VICTIMS:
            print("Todas las víctimas detectadas. Volviendo al punto de inicio...")
            drone_state = "RETURN_HOME"
        else:
            if radius_current < 0.1:
                radius_current = 0.1

            angular_speed = SPIRAL_SPEED / radius_current
            angle_accumulated += angular_speed * dt

            target_x = TARGET_X + radius_current * math.cos(angle_accumulated)
            target_y = TARGET_Y + radius_current * math.sin(angle_accumulated)

            vx_cmd = max(min((target_x - x_pos), 2.5), -2.5)
            vy_cmd = max(min((target_y - y_pos), 2.5), -2.5)
            vz_cmd = (FLIGHT_HEIGHT - z_pos) * 0.5

            HAL.set_cmd_vel(vx_cmd, vy_cmd, vz_cmd, 0)

    elif drone_state == "RETURN_HOME":
        home_x, home_y = 0.0, 0.0
        dx = home_x - x_pos
        dy = home_y - y_pos
        distance = math.hypot(dx, dy)
        vz = (FLIGHT_HEIGHT - z_pos) * 0.5

        if distance < 0.5:
            print("Punto de inicio alcanzado. Aterrizando...")
            drone_state = "LAND"
            HAL.set_cmd_vel(0, 0, 0, 0)
        else:
            vx = max(min(dx * 0.5, 3.0), -3.0)
            vy = max(min(dy * 0.5, 3.0), -3.0)
            HAL.set_cmd_vel(vx, vy, vz, 0)

    elif drone_state == "LAND":
        HAL.land()
        for i, loc in enumerate(victims_locations, start=1):
            print(f" [{i}] X={loc[0]:.2f}, Y={loc[1]:.2f}")
        break
