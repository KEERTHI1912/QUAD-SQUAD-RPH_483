import cv2
import numpy as np

def calculate_displacement(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()

    # Match descriptors
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test and RANSAC
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Use RANSAC to filter matches
    if len(good_matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        mask = mask.ravel()

        # Calculate displacement based on matched keypoints after RANSAC
        displacement = np.mean(dst_pts[mask == 1] - src_pts[mask == 1], axis=0).reshape(-1)
    else:
        displacement = (0, 0)

    return displacement

def interpret_displacement(displacement):
    x, y = displacement
    movement = ""

    if x > 0:
        movement += "Right "
    elif x < 0:
        movement += "Left "

    if y > 0:
        movement += "Down"
    elif y < 0:
        movement += "Up"

    return movement.strip()

if __name__ == "__main__":
    # Open the camera (change the parameter to 0 if using the default camera)
    cap = cv2.VideoCapture(0)

    # Read the first frame
    ret, frame1 = cap.read()

    while True:
        # Read the next frame
        ret, frame2 = cap.read()

        if not ret:
            print("Error capturing frames.")
            break

        # Calculate displacement
        displacement = calculate_displacement(frame1, frame2)

        # Interpret displacement
        movement_description = interpret_displacement(displacement)

        # Display the result on the video feed
        cv2.putText(frame2, f"Movement: {movement_description}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Live Displacement Detection', frame2)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Update the previous frame
        frame1 = frame2

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()