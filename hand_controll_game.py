import cv2
import pyautogui
import time
import mediapipe as mp

# Key mappings
LEFT_ARROW = 'left'
RIGHT_ARROW = 'right'
UP_ARROW = 'up'     # JUMP
DOWN_ARROW = 'down' # SLIDE

def PressKey(key):
    pyautogui.keyDown(key)

def ReleaseKey(key):
    pyautogui.keyUp(key)

# Mappings
left_key = LEFT_ARROW
right_key = RIGHT_ARROW
jump_key = UP_ARROW
slide_key = DOWN_ARROW

time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        if not ret:
            print("Failed to grab frame")
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        detected_text = "No hands detected"

        if results.multi_hand_landmarks:
            detected_text = "Hand detected"
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        fingers = []
        if len(lmList) != 0:
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Other fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total = fingers.count(1)

            # Decide action
            if total == 0:
                # Fist → LEFT
                cv2.putText(image, "LEFT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 0, 255), 5)
                if left_key not in current_key_pressed:
                    PressKey(left_key)
                    current_key_pressed.add(left_key)
                for key in [right_key, jump_key, slide_key]:
                    if key in current_key_pressed:
                        ReleaseKey(key)
                        current_key_pressed.discard(key)

            elif total == 5:
                # Open → RIGHT
                cv2.putText(image, "RIGHT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 5)
                if right_key not in current_key_pressed:
                    PressKey(right_key)
                    current_key_pressed.add(right_key)
                for key in [left_key, jump_key, slide_key]:
                    if key in current_key_pressed:
                        ReleaseKey(key)
                        current_key_pressed.discard(key)

            elif total == 1 and fingers[1] == 1:
                # 1 finger → JUMP
                cv2.putText(image, "JUMP", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 255, 0), 5)
                if jump_key not in current_key_pressed:
                    PressKey(jump_key)
                    current_key_pressed.add(jump_key)
                for key in [left_key, right_key, slide_key]:
                    if key in current_key_pressed:
                        ReleaseKey(key)
                        current_key_pressed.discard(key)

            elif total == 2 and fingers[1] == 1 and fingers[2] == 1:
                # 2 fingers → SLIDE
                cv2.putText(image, "SLIDE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 255), 5)
                if slide_key not in current_key_pressed:
                    PressKey(slide_key)
                    current_key_pressed.add(slide_key)
                for key in [left_key, right_key, jump_key]:
                    if key in current_key_pressed:
                        ReleaseKey(key)
                        current_key_pressed.discard(key)

            else:
                # Other = release all
                for key in list(current_key_pressed):
                    ReleaseKey(key)
                current_key_pressed.clear()

        else:
            # No hand = release all
            for key in list(current_key_pressed):
                ReleaseKey(key)
            current_key_pressed.clear()

        cv2.putText(image, detected_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)

        cv2.imshow("Hand Gesture Control", image)
        k = cv2.waitKey(1)
        if k == 27:  # ESC to exit
            for key in list(current_key_pressed):
                ReleaseKey(key)
            break

video.release()
cv2.destroyAllWindows()
