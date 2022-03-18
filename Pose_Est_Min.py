import cv2
import mediapipe as mp


''' this is used to play a video '''

''' this is used to access webcam '''

''' cap = cv2.VideoCapture(0) '''
print("It's working")


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4,480)

while True:
    success, img = cap.read()

    cv2.putText(img, str("Hello"), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
