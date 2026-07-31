import cv2
def blur_effect(image):
    return cv2.GaussianBlur(image,(25,25),0)