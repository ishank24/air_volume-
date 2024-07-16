import cv2
import mediapipe as mp
import numpy as np
from math import hypot
import tkinter as tk
from PIL import Image, ImageTk
import wmi

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize brightness variables
brightness = 50  # Default brightness level

# Setup WMI to set system brightness
c = wmi.WMI(namespace='wmi')
methods = c.WmiMonitorBrightnessMethods()[0]

def set_system_brightness(value):
    """Set the brightness of the system to a given value."""
    methods.WmiSetBrightness(Brightness=value, Timeout=0)

# Example: Set initial brightness to 50%
set_system_brightness(brightness)

def process_image(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lm_list = []

    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handlandmark, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

                if id == 4:  # Thumb tip
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                elif id == 8:  # Index finger tip
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            if len(lm_list) >= 2:
                # Calculate distance between thumb tip and index finger tip
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2]
                length = hypot(x2 - x1, y2 - y1)
                brightness = np.interp(length, [50, 300], [0, 100])
                set_system_brightness(int(brightness))

    return img

def update_video_stream():
    ret, frame = cap.read()
    if ret:
        frame = process_image(frame)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.itemconfig(video_stream, image=img_tk)
        canvas.image = img_tk
    root.after(1, update_video_stream)

# Initialize webcam and GUI
cap = cv2.VideoCapture(0)
root = tk.Tk()
root.title("Hand Gesture Brightness Control")
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()
video_stream = canvas.create_image(10, 10, anchor=tk.NW)

update_video_stream()
root.mainloop()

cap.release()
cv2.destroyAllWindows()
