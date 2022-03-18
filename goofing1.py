import cv2
print("package imported")
'''   Open Images

img = cv2.imread("Resources/img1.jpg")

cv2.imshow("Output", img)

cv2.waitKey(0)

'''


''' cap = cv2.VideoCapture("Resources/dude.mp4")  this is used to play a video '''

''' this is used to access webcam '''

cap = cv2.VideoCapture(0)
cap.set(3, 280)
cap.set(4,480)

while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
