#This file acts as a manager that helps usto call the gesture_detctor
#in a clean or consistent way 
from api.ai.gesture.gesture_detector import (
    detect_gesture,
    decode_base_64_image
)
from api.ai.effects.effect_processor import blur_effect

def process_gesture_input(data: dict):
    image=data.get("image_base64")
    if not image:
        return{
            "status":"error",
            "message":"Image Not Provided"
        }
    action=detect_gesture(image)
     
    if action=="pinch":
         frame = decode_base_64_image(image)
         blurred = blur_effect(frame)

    # Placeholder for actual MediaPipe or logic processing
    return {
        "status": "success" if action else "no_gesture",
        "action_detected": action,
        "message": "Gesture processed successfully" if action else "No gesture found"
    }
