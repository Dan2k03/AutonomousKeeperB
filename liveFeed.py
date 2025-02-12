import cv2
from picamera2 import Picamera2
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

while True:
    # Capture a frame from the camera
    frame_array = picam2.capture_array("main")

    # Convert RGB to BGR
    frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

    # Display the frame using OpenCV
    cv2.imshow("PiCamera2 Feed", frame_array)

    # Check for user input to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the camera and close windows
picam2.stop()
cv2.destroyAllWindows()
