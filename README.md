## **Hand Gesture Control**

This project leverages **OpenCV** and **MediaPipe** to recognize hand gestures and trigger keyboard inputs for controlling actions like braking and accelerating in a game or simulation.

---

## **Requirements**

* Python 3.x
* OpenCV
* MediaPipe
* PyAutoGUI

---

## **Installation**

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/narasmiha224/hand-gesture-control/blob/main/hand_controlled_game.py
   ```

2. Make sure all required packages are installed:

   ```bash
   pip install opencv-python mediapipe pyautogui
   ```

---

## **How it Works**

The script captures live video from your webcam, detects hand landmarks in real time using MediaPipe, interprets specific hand gestures, and simulates keyboard actions accordingly—enabling gesture-based control for driving actions like speed control and stopping.
