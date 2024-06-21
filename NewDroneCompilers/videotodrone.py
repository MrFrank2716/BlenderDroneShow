import cv2
import pandas as pd

# Function to identify and track drones
def identify_and_track_drones(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to reveal light regions in the blurred image
    _, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Perform a series of dilations to remove any small blobs of noise from the thresholded image
    thresholded = cv2.dilate(thresholded, None, iterations=2)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    drones = []
    for contour in contours:
        # Compute the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Get the color of the drone
        color = frame[cY, cX, :]

        # Add the drone's data to the list
        drones.append({
            'pixel_coordinates': (cX, cY),
            'color': color,
            'id': len(drones) + 1  # Assign a unique ID to each drone
        })

    return drones

# Function to convert pixel coordinates to real-world coordinates
def convert_coordinates(pixel_coordinates, image_size):
    # Unpack the pixel coordinates and image size
    x_pixel, y_pixel = pixel_coordinates
    width, height = image_size

    # Compute the center of the image
    center_x, center_y = width / 2, height / 2

    # Convert the pixel coordinates to the new coordinate system
    x = x_pixel - center_x
    y = center_y - y_pixel  # The y axis is inverted in pixel coordinates

    return x, y

# Initialize video capture
cap = cv2.VideoCapture('dreams.mp4')

drone_data = []
frame_count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        drones = identify_and_track_drones(frame)
        for i, drone in enumerate(drones):
            # Get the size of the frame
            image_size = frame.shape[1], frame.shape[0]  # Width, Height
            # Convert pixel coordinates to real-world coordinates
            real_world_coordinates = convert_coordinates(drone['pixel_coordinates'], image_size)
            drone_data.append({
                'Time [msec]': frame_count * 40,  # Assuming the video is 25 fps
                'x [m]': real_world_coordinates[0],
                'y [m]': real_world_coordinates[1],
                'z [m]': 0,
                'Red': drone['color'][0],
                'Green': drone['color'][1],
                'Blue': drone['color'][2]
            })
        frame_count += 1
    else:
        break

cap.release()

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(drone_data)

# Save each drone's data to a separate .csv file
for drone_id in df['Time [msec]'].unique():
    df[df['Time [msec]'] == drone_id].to_csv(f'Drone {drone_id // 40}.csv', index=False)
