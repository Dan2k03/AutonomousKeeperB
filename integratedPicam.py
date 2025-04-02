import cv2
import numpy as np
from picamera2 import Picamera2
import serial
import time

ser = serial.Serial(
    port='/dev/ttyS0',  # Use '/dev/ttyS0' or '/dev/serial0' for Raspberry Pi 3
    baudrate=9600,
    timeout=30
)

def send_string(data):
    ser.write(data.encode())  # Convert string to bytes and send
    print(f"Sent: {data}")

#from time import sleep
# Identify the camera index (optional, modify if needed)
camera_index = 0  # Assuming the camera is at index 0

# Initialize the PiCamera2 object
picam2 = Picamera2()
# Configure the camera for preview
preview_config = picam2.create_preview_configuration()
# INSIDE LAST LINE FUNCTION: main={"format": "RGB888", "size": (640, 480)}
#picam2.start_preview(Preview.QTGL)
picam2.configure(preview_config)
picam2.start()

#picam2.configure(config)
#picam2.start()



def detect_orange_ball(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Refined dark orange HSV range
    lower_orange = np.array([5, 150, 50])
    upper_orange = np.array([7, 255, 200])

    # Create mask
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Reduce noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(contours) > 0:
        # Find largest contour
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only detect if radius is large enough
        if radius > 10:
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)
            print(f"X: {x}, Y: {y}")
            if (x < 250):
                leftpos = ("Left")
            elif (x > 350):
                leftpos = ("Right")
            else:
                leftpos = ("Center")

            if (y < 150):
                rightpos = ("Top")
            elif (y > 250):
                rightpos = ("Bottom")
            else:
                rightpos = ("Center")
            print(f"{leftpos}, {rightpos}")
            try:
                send_string(f"{leftpos}, {rightpos}")
                time.sleep(1)  # Give time for transmission
            except Exception as e:
                print(f"Error: {e}")
            
    return image



while True:
    # Capture a frame from the camera
    frame_array = picam2.capture_array("main")

    # Convert RGB to BGR
    frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

    result_image = detect_orange_ball(frame_array)

    cv2.imshow('Live Orange Ball Detection', result_image)

    # Check for user input to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the camera and close windows
picam2.stop()
cv2.destroyAllWindows()

