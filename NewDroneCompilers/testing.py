import cv2

# Function to identify and track drones
# Function to identify and track drones
def identify_and_track_drones(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to reveal light regions in the blurred image
    _, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow("Thresh", thresholded)

    # Perform a series of dilations to remove any small blobs of noise from the thresholded image
    dialted = cv2.dilate(thresholded, None, iterations=2)
    cv2.imshow("Dialted", dialted)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(dialted.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # drones = []
    # for contour in contours:
    #     # Compute the center of the contour
    #     M = cv2.moments(contour)
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    #
    #     # Get the color of the drone
    #     color = frame[cY, cX, :]
    #
    #     # Add the drone's data to the list
    #     drones.append({
    #         'pixel_coordinates': (cX, cY),
    #         'color': color,
    #         'id': len(drones) + 1  # Assign a unique ID to each drone
    #     })
    #
    # return

frame = cv2.imread("test.png")
cv2.imshow("Orignial",frame)

identify_and_track_drones(frame)
while True:
    cv2.imshow("Orignial",frame)