import cv2
import mediapipe as mp
import time
import math

print("PoseModule.py is running now")

''' 
  Right now, on Line # 54, we've called a specific video into VideoCapture,
  So, if you run a code file that relies on or calls PoseModule.py,
  It might show that specific video instead of whatever you reall wanna use (video/webcam)
  
  '''

class PoseDetector():

    def __init__(self, mode=False, complexity=1, smooth=True, enab_seg = False, smooth_seg = False, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.enab_seg = enab_seg
        self.smooth_seg = smooth_seg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.enab_seg, self.smooth_seg,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks( img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS )
        return img


    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark ):
                height, width, channel = img.shape
               # print( id, lm )
                cx, cy = int( lm.x * width ), int( lm.y * height)
                self.lmList.append( [id, cx, cy] )
                if draw:
                    cv2.circle( img, (cx, cy), 5, ( 255, 0, 0 ), cv2.FILLED ) #This is used to style the landmarks
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw = True):

        # We're going to use these landmarks:
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        ''' Right now, we haven't used the original formula because it gave a wierd angle,
            Instead, we tweaked it a bit and used our own, it is mathematically correct and
            gives the correct angle, if it f's around with the other exercises' angles, 
            just use the original one. '''

        #Original:
        #angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

     #   if angle < 0:
      #      angle += 360

        #Ours:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1) - math.atan2(y2 - y3, x2 - x3))
        if angle < 0:
            angle += 360
        print(angle)

        # This is used to style the landmarks & connections
        if draw:
            # CONNECTIONS:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

            # LANDMARKS:
            # FOR ( x1, y1 ):
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)

            # FOR ( x2, y2 ):
            cv2.circle(img, (x2, y2), 10, (0, 0, 255, cv2.FILLED))
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)

            # FOR ( x3, y3 ):
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)

            #ANGLE SHOWN AT PIVOT
            cv2.putText(img, str( int(angle)), (x2 - 20, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return angle

def main():
    cap = cv2.VideoCapture("Resources/man_performing_bicep_curls_small.mp4")

    prev_time = 0

    detector = PoseDetector()

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


if __name__ == "__main__":
    main()