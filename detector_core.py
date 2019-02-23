# Standard imports
from cv2 import *
import cv2
import ctypes
import math

# SETTINGS
settings = {}

# DEFINITIONS
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
font = cv2.FONT_HERSHEY_SIMPLEX


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def crop_and_get_buttons_only(input_image):
    image_clone = input_image.copy()
    im_height, im_width = image_clone.shape[:2]
    mid_point = im_width / 2
    half_scan_width = settings["WIDTH_PERCENTAGE_OF_SCANNING_AREA"] * im_width / 200
    return image_clone[:, mid_point - half_scan_width: mid_point + half_scan_width]


def stich_cropped_buttons_back(original, cropped):
    image_clone = original.copy()
    im_height, im_width = image_clone.shape[:2]
    mid_point = im_width / 2
    half_scan_width = settings["WIDTH_PERCENTAGE_OF_SCANNING_AREA"] * im_width / 200
    image_clone[:, mid_point - half_scan_width: mid_point + half_scan_width] = cropped
    return image_clone


def get_button_keypoints(cropped_img):
    cropped_img = apply_brightness_contrast(cropped_img, 0, 40)
    # show_image_fit_screen(cropped_img, "Intermediate")
    # cv2.waitKey(0)
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(cropped_img)
    # Sort to get the top button at first
    keypoints.sort(key=lambda coord: coord.pt[1])
    return keypoints


def draw_buttons_on_image(_keypoints, source_img):
    print "{0} BUTTONS DETECTED".format(len(_keypoints))
    if len(_keypoints) < 2:
        return None
    # Draw detected blobs as red circles.
    ax, ay = _keypoints[0].pt
    bx, by = _keypoints[1].pt
    img_out = cv2.line(source_img, (int(ax), int(ay)), (int(bx), int(by)), (255, 0, 0), 4)
    cv2.drawKeypoints(img_out, _keypoints, img_out, (0, 255, 0),
                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img_out


def calculate_button_distance_inches(keypoints):
    pt_a = keypoints[0].pt
    pt_b = keypoints[1].pt
    pixel_distance = math.sqrt((pt_b[0] - pt_a[0]) ** 2 + (pt_b[1] - pt_a[1]) ** 2)
    # pixel_distance = secondbutton_point[1] - topbutton_point[1]
    real_distance = pixel_distance / settings["PIXELS_PER_INCH"]
    print "Distance between first two buttons: " + "{0:.2f}".format(real_distance) + "inches"
    return real_distance


def show_image_fit_screen(image, window_name):
    im_height, im_width = image.shape[:2]
    print str(im_height) + " x " + str(im_width)
    window_height = screensize[1] * 0.8
    window_width = window_height * (im_width / float(im_height))
    print (im_height / float(im_width))
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, int(window_width), int(window_height))
    cv2.imshow(window_name, image)


def render_instructions(image_):
    global font
    im_width, im_height = image_.shape[:2]
    cv2.rectangle(image_, (0, im_width - 40), (im_height, im_width), (0, 0, 0), cv2.FILLED,
                  lineType=8)
    cv2.putText(image_, 'PRESS \'Q\' TO EXIT', (0, im_width - 10), font, 1,
                (255, 255, 255),
                3, cv2.LINE_AA)


def render_result(image_, inches):
    global font
    is_acceptable = abs(inches - 2) < settings["TOLERANCE_INCHES"]
    result_text = "Button Distance: {0:.2f}\" ACCEPTED: {1}".format(inches, "YES" if is_acceptable else "NO")

    im_height, im_width = image_.shape[:2]
    cv2.rectangle(image_, (0, im_height - 80), (im_width, im_height - 40),
                  (0, 255, 0) if is_acceptable else (0, 0, 255), cv2.FILLED,
                  lineType=8)
    cv2.putText(image_, result_text, (0, im_height - 50), font, 1,
                (0, 0, 0),
                3, cv2.LINE_AA)


def detection_entry_point(input_image):
    cropped_color = crop_and_get_buttons_only(input_image)

    keypoint_list = get_button_keypoints(cropped_color)
    im_with_keypoints = draw_buttons_on_image(keypoint_list, cropped_color)
    if im_with_keypoints is not None:
        stiched_final_image = stich_cropped_buttons_back(input_image, im_with_keypoints)
        inches = calculate_button_distance_inches(keypoint_list)
        # Show keypoints
        render_instructions(stiched_final_image)
        render_result(stiched_final_image, inches)
        show_image_fit_screen(stiched_final_image, "Result")

    else:
        render_instructions(input_image)
        show_image_fit_screen(input_image, "Result")


def detection_api_detect_from_image(_settings):
    global settings
    settings = _settings
    frame = cv2.imread("img/" + settings["IMAGE_FILE_NAME"], cv2.IMREAD_COLOR)
    detection_entry_point(frame)
    cv2.waitKey(0)


def detection_api_detect_from_webcam(_settings):
    global settings
    settings = _settings
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        detection_entry_point(frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()  # destroy all the opened windows
