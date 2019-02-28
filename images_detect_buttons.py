import detector_core

# SETTINGS
_settings = {
    "IMAGE_FILE_NAME": "shirt (6).jpg",
    "PIXELS_PER_INCH": 40,
    "ACCEPTED_TOLERANCE_INCHES": 0.2,
    "QUALITY_TOLERANCE_INCHES": 0.04,
    "WIDTH_PERCENTAGE_OF_SCANNING_AREA": 30
}

detector_core.detection_api_detect_from_image(_settings)
