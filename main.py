import cv2
import mediapipe as mp
import pyautogui
import math

from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


mp_hands = mp.solutions.hands
hands=  mp_hands.Hands()

camera=cv2.VideoCapture(0)

screenshot_taken = False

devices=AudioUtilities.GetSpeakers()
volume_control = devices.EndpointVolume

while True:
    success, img=camera.read()
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
     for hand_landmarks in results.multi_hand_landmarks:
        index_tip = hand_landmarks.landmark[8]
        thumb_tip = hand_landmarks.landmark[4]
        distance = math.sqrt(
           (thumb_tip.x - index_tip.x) ** 2 +
           (thumb_tip.y - index_tip.y) ** 2
        )
        volume =int((distance-0.03)/(0.84-0.03)*100)
        volume=max(0, min(volume, 100))
        volume_control.SetMasterVolumeLevelScalar(volume/100, None)
        cv2.putText(
                  img,
                  f"Distance:{distance:.2f}",
                 (20,50),
                 cv2.FONT_HERSHEY_SIMPLEX,
                 1,
                 (0,255,0),
                 2
                )
        cv2.putText(
                  img,
                  f"Volume:{volume}%",
                  (20,90),
                  cv2.FONT_HERSHEY_SIMPLEX,
                  1,
                  (0,255,0),
                  2
        )
       

         
        index_joint = hand_landmarks.landmark[6]

        if index_tip.y < index_joint.y:
         pyautogui.screenshot("gesture.png")
         screenshot_taken = True

        if index_tip.y >= index_joint.y:
         screenshot_taken = False
        mp.solutions.drawing_utils.draw_landmarks(
            img,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS )

    if not success:
        print("Failed to capture image")
        break
    cv2.imshow("Camera", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
     for hand_landmarks in results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            img,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

camera.release()
cv2.destroyAllWindows()

