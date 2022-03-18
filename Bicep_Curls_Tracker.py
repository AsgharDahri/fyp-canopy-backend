import cv2
import numpy as np
import time
import PoseModule as pm
from flask_cors import CORS
from flask import Flask, render_template, Response
from flask import jsonify


Error_report = []

exercise_quality = ""
exercise_comment = ""
print("Running Bice_Curls_Tracker.py")

'''
    The youtuber started off by doing stuff with an image, whereas we directly used a video instead, 
    while working with the image, he put the following line's equivalent inside the "while True" thing,
    so, see this if there is an error
'''
app = Flask(__name__)
cap = cv2.VideoCapture(0)
CORS(app)
detector = pm.PoseDetector()
count = -0.5

# 0 = going up, 1 = going down
dir = 0


simpleVariable='asghar'
def gen_frames():  
    detector = pm.PoseDetector()
    count = -0.5

    # 0 = going up, 1 = going down
    dir = 0
        
    while True:
        success, img = cap.read()
        passed_thru = 0
        # Comment this out when you use the webcam
        #img = cv2.resize( img, (480, 710)) # This is used to resize the video/webcam footage

        img = detector.findPose(img, False)

        # Section A1 starts here: The following code is being used to find the landmarks that we're going to use;
        # your landmarks are prob. diff. from the youtuber's...
        simpleVariable='dahri'
        lmList = detector.findPosition(img, False)
        print("\nPoint: ", lmList)
        if len(lmList) != 0:
            angle = detector.findAngle(img, 11, 13, 15)

            '''
            Below, we've converted the repetition's angular movement to a scale of 0% to 100%, 
            you can set whatever min/max angle you want (We've used numpy)
            '''
            per = np.interp(angle, (55, 93), (0, 100))

            bar = np.interp( angle, (55, 93), (650, 100) ) # For the bar: (MAX, MIN)
            print("\nAngle: ", angle, " -- ", per)          #|_____|______________________^    ^
                                                    #|___________________________|
            # COUNT EXERCISE REPETITIONS:
            if per == 100:
                if dir == 0 & passed_thru == 0 :
                    count += 0.5
                    dir = 1
                    passed_thru = 1
                else:
                    pass

            if per == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0
                    passed_thru = 0
            print(count)

            # to count full reps only, use str( int( count ) )
        # cv2.rectangle( img, (0, 450), (50, 100), (0, 255, 0), cv2.FILLED )

            cv2.putText( img, f'Reps: {count}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 5 )

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # cv2.imshow( "Image", img )
        cv2.waitKey(1)
        # if(count==2):
        #     # app.r
        #     # video_feedback()
        #     return count


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feedback')
def video_feedback():
    # return {'name':'Jimit'}
    # return jsonify(simpleVariable)
    return ({'name':count})


# @app.route('/video_assistment')
# def video_feedback(count):
#     # return {'name':'Jimit'}
#     # return jsonify(simpleVariable)
    # return ({'name':count})


if __name__ == "__main__":
    app.run(debug=True)