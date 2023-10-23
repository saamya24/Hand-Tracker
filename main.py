import cv2
import mediapipe as mp
import ctypes

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

def click(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

cap = cv2.VideoCapture(0)

cursor_x = 0
cursor_y = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_open = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            screen_width, screen_height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
            cursor_x = int(index_tip.x * screen_width)
            cursor_y = int(index_tip.y * screen_height)

            if hand_open:
                ctypes.windll.user32.SetCursorPos(cursor_x, cursor_y)
            else:
                click(cursor_x, cursor_y)

        annotated_frame = frame.copy()
        mp.solutions.drawing_utils.draw_landmarks(annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hand Tracking', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
