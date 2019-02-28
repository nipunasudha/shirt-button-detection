import detector_core

# SETTINGS
_settings = {
    "PIXELS_PER_INCH": 40,
    "ACCEPTED_TOLERANCE_INCHES": 0.2,
    "QUALITY_TOLERANCE_INCHES": 0.0047,
    "WIDTH_PERCENTAGE_OF_SCANNING_AREA": 70
}

detector_core.detection_api_detect_from_webcam(_settings)
