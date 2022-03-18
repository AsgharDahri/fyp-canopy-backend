import cv2
import time
import PoseModule as pm



cap = cv2.VideoCapture("Resources/man_performing_bicep_curls_small.mp4")

prev_time = 0

detector = pm.PoseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)

    lmList = detector.findPosition(img)
    print(lmList)

    current_time = time.time()
    fps = 1/( current_time - prev_time )
    prev_time = current_time

    cv2.putText( img, str(int( fps )) , (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)