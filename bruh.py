import cv2
import numpy as np
from picamera2 import Picamera2
import serial
import time
import serial.tools.list_ports

# --- Initialize Serial Communication ---
ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)  # Wait for Arduino to reset

def send_angle(angle):
    if ser.is_open:
        ser.write(f"{angle}\n".encode())
        ser.flush()
        print(f"Sent angle: {angle}")

# --- Print Available Serial Ports (debug) ---
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Available port: {port.device}")

# --- Initialize PiCamera2 ---
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# --- Track last angle sent ---
current_angle = 90  # Assume starting straight ahead

# --- Ball Detection Function ---
def detect_orange_ball(image):
    global current_angle

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Improved orange HSV range
    lower_orange = np.array([5, 150, 180])
    upper_orange = np.array([20, 255, 255])

    # Mask & noise reduction
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if M["m00"] > 0 and radius > 10:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)

            frame_width = image.shape[1]
            target_angle = int((x / frame_width) * 180)

            print(f"Ball at X: {x}, mapped angle: {target_angle}")

            if abs(target_angle - current_angle) >= 10:
                step = 10 if target_angle > current_angle else -10
                for angle in range(current_angle, target_angle + step, step):
                    send_angle(angle)
                    time.sleep(0.05)
                current_angle = target_angle

    return image

# --- Main Loop ---
try:
    while True:
        frame_array = picam2.capture_array("main")
        frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

        result_image = detect_orange_ball(frame_array)

        cv2.imshow('Live Orange Ball Detection', result_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    ser.close()
    cv2.destroyAllWindows()
