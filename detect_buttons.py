# Standard imports
from cv2 import *
import cv2
import numpy as np
import ctypes

PIXELS_PER_CENTIMETER = 18

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
font = cv2.FONT_HERSHEY_SIMPLEX


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


def show_image_fit_screen(image):
    im_height, im_width = image.shape[:2]
    print str(im_height) + " x " + str(im_width)
    window_height = screensize[1] * 0.8
    window_width = window_height * (im_width / float(im_height))
    print (im_height / float(im_width))
    cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Output', int(window_width), int(window_height))
    cv2.imshow("Output", im_with_keypoints)


def render_instructions(image_):
    global font
    im_width, im_height = image_.shape[:2]
    cv2.rectangle(image_, (0, im_width - 40), (im_height, im_width), (0, 0, 0), cv2.FILLED,
                  lineType=8)
    cv2.putText(image_, 'ESC TO EXIT', (0, im_width - 10), font, 1,
                (255, 255, 255),
                3, cv2.LINE_AA)


def render_result(image_, result_string):
    global font
    im_height, im_width = image_.shape[:2]
    cv2.rectangle(image_, (0, im_height - 80), (im_width, im_height - 40), (0, 255, 0), cv2.FILLED,
                  lineType=8)
    cv2.putText(image_, result_string, (0, im_height - 50), font, 1,
                (0, 0, 0),
                3, cv2.LINE_AA)


# Read image
img = cv2.imread("img/shirt1.jpg", cv2.IMREAD_GRAYSCALE)

keypoint_list = get_button_keypoints(img)
im_with_keypoints = draw_buttons_on_image(keypoint_list, img)
calculate_button_distance(keypoint_list)
# Show keypoints
render_instructions(im_with_keypoints)
render_result(im_with_keypoints, "LOL")
show_image_fit_screen(im_with_keypoints)
cv2.waitKey(0)
