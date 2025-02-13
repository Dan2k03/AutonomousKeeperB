# import cv2
# import numpy as np
#
# def detect_orange_ball(image):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     lower_orange = np.array([5, 150, 50])
#     upper_orange = np.array([7, 255, 200])
#     mask = cv2.inRange(hsv, lower_orange, upper_orange)
#
#     mask = cv2.erode(mask, None, iterations=2)
#     mask = cv2.dilate(mask, None, iterations=2)
#
#     contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     center = None
#
#     if len(contours) > 0:
#         c = max(contours, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#
#         if radius > 10:
#             cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#             cv2.circle(image, center, 5, (0, 0, 255), -1)
#     return image
#
# # Example usage (assuming you have an image named 'ball_image.jpg')
# image = cv2.imread('balllll.png')
# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     _, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#
#     if frame is not None:
#         result_image = detect_orange_ball(frame)
#         cv2.imshow('Orange Ball Detection', result_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("Error: Could not open or read the image file.")


import cv2
import numpy as np


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

    return image


# Start live video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't capture video")
        break

    frame = cv2.flip(frame, 1)  # Mirror effect for better tracking
    result_image = detect_orange_ball(frame)

    cv2.imshow('Live Orange Ball Detection', result_image)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
