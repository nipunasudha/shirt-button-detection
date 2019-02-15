# Standard imports
import cv2
import numpy as np

# settings
PIXELS_PER_CENTIMETER = 18
IMAGE_TO_SCAN = "img/shirt1.jpg"

def get_button_keypoints(grayscale_img):
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(grayscale_img)
    # Sort to get the top button at first
    keypoints.sort(key=lambda coord: coord.pt[1])
    return keypoints


def draw_buttons_on_image(_keypoints, source_img):
    # Draw detected blobs as red circles.
    return cv2.drawKeypoints(source_img, _keypoints, np.array([]), (0, 255, 0),
                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


def calculate_button_distance(keypoints):
    topbutton_point = keypoints[0].pt
    secondbutton_point = keypoints[1].pt
    pixel_distance = secondbutton_point[1] - topbutton_point[1]
    real_distance = pixel_distance / PIXELS_PER_CENTIMETER
    print "Distance between first two buttons: " + "{0:.2f}".format(real_distance) + "cm"
    print "Distance between first two buttons: " + "{0:.2f}".format(real_distance / 2.54) + "inches"


# Read image
img = cv2.imread(IMAGE_TO_SCAN, cv2.IMREAD_GRAYSCALE)

keypoint_list = get_button_keypoints(img)
im_with_keypoints = draw_buttons_on_image(keypoint_list, img)
calculate_button_distance(keypoint_list)
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

