import cv2
import mediapipe as mp
import numpy as np

import client

#检测脸部
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#通信传输
myRaspConnection = client.connect_Raspberry('192.168.43.66', 8888)

if __name__ == "__main__":

    capture = cv2.VideoCapture("http://192.168.43.66:8080/?action=stream")

    ref, frame = capture.read()
    fps = 0.0

    while(True):

        ref, frame = capture.read()
        h,w,_ = np.shape(frame)
        if not ref:
            break
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #脸部检测
        with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.8) as face_detection:
            results = face_detection.process(image)

            if results.detections:
                for detection in results.detections:
                    box=detection.location_data.relative_bounding_box
                    #cx,cy,cw,ch=box
                    cx=box.xmin
                    cy=box.ymin
                    cw=box.width
                    ch=box.height
                    
                    cv2.rectangle(image, (int(cx*w) , int(cy*h)), (int((cx+cw)*w) , int((cy+ch)*h)),(0, 255, 0), 2)
                
                #控制云台
                msg = str(int(cx*w)) + " " + str(int(cy*h)) + " " + str(int((cx+cw)*w)) + " " + str(int((cy+ch)*h)) + " "
                
                myRaspConnection.send(msg)



        frame = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        # cv2.rectangle(frame, (int(cx*w) , int(cy*h)), (int((cx+cw)*w) , int((cy+ch)*h)),(0, 255, 0), 2)  
        
        cv2.imshow("face_track",frame)
        c= cv2.waitKey(1) & 0xff 

        if c==27:
            capture.release()
            break
    print("Video Detection Done!")
    capture.release()
    cv2.destroyAllWindows()

