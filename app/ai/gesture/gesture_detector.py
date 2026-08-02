#Part 1 the main part of this file is to you got text in the form of image now you have to convert this text into bytes->numpy->opencv helps you to convert into its orignal image
import math
import mediapipe as mp
import base64
import numpy as np
import cv2
my_hands=mp.solutions.hands
def decode_base_64_image(image_base64:str):
    #Convert text into bytes
    img_bytes=base64.b64decode(image_base64)
    #Convert bytes into numpy
    np_arr=np.frombuffer(img_bytes,np.uint8)
    #Convert numpy into original image
    frame=cv2.imdecode(np_arr,cv2.IMREAD_COLOR)
    return frame
def detect_gesture(image_base64:str)-> str| None:
    frame=decode_base_64_image(image_base64)
    with my_hands.Hands(static_image_mode=True,max_num_hands=1)  as hands:
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(rgb)
        if not results.multi_hand_landmarks:
         return None
        hand= results.multi_hand_landmarks[0]
        thumb_tip=hand.landmark[4]
        middle_tip=hand.landmark[12]
       
    distance=math.sqrt(
       (thumb_tip.x-middle_tip.x)**2 +
       (thumb_tip.y-middle_tip.y)**2
    )
    if distance<0.05:
       return "pinch"
    return None