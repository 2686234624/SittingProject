import cv2
import mediapipe as mp
import numpy as np
import math as m
import time
import os

import socket
import client

def findDistance(x1, y1, x2, y2): # 计算两点之间的距离
    dist = m.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist

def findAngle_hor(x1, y1, x2, y2): # 计算水平角度
    if (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1) == 0:
        return 0
    theta = m.acos((y2 -y1)*(-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180/m.pi)*theta
    return abs(degree - 90)

def findAngle_ver(x1, y1, x2, y2): # 计算垂直角度
    if (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1) == 0:
        return 0
    theta = m.acos((y2 -y1)*(-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180/m.pi)*theta
    return degree

<<<<<<< HEAD
def sendWarning(): # 发送警告
=======
def sendWarning(x): # 发送警告
>>>>>>> 4732386cdee22c786b3e2789fd83ffcf44fcc849
    # os.system("start " + file)
    pass

#检测脸部
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#检测坐姿
# mp_pose = mp.solutions.pose  # 初始化mediapipe pose模型
# mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose # 初始化mediapipe pose模型
pose = mp_pose.Pose()

good_frames = 0  # 关于坐姿的帧数
bad_frames = 0

font = cv2.FONT_HERSHEY_SIMPLEX # 设置字体

blue = (255, 127, 0) # 设置颜色
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

#通信传输
myRaspConnection = client.connect_Raspberry('192.168.43.66', 8888)

#报警音乐
file = r".\Warning\drumver.mp3"

if __name__ == "__main__":

<<<<<<< HEAD
    capture = cv2.VideoCapture("http://192.168.43.66:8080/?action=stream") # 从树莓派摄像头通过网络获取实时视频
    # capture = cv2.VideoCapture(0) # 从本地摄像头获取实时视频
=======
    # capture = cv2.VideoCapture("http://192.168.43.66:8080/?action=stream") # 从树莓派摄像头通过网络获取实时视频
    capture = cv2.VideoCapture(0) # 从本地摄像头获取实时视频
>>>>>>> 4732386cdee22c786b3e2789fd83ffcf44fcc849

    ref, frame = capture.read()
    fps = 0.0

    while(True):

        ref, frame = capture.read()
        h,w,_ = np.shape(frame)
        if not ref:
            break
        fps = capture.get(cv2.CAP_PROP_FPS)
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        start_time = time.time()

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
                    
                    cv2.rectangle(image, (int(cx*w) , int(cy*h)), (int((cx+cw)*w) , int((cy+ch)*h)), blue, 2)
                
                #控制云台
                msg = str(int(cx*w)) + " " + str(int(cy*h)) + " " + str(int((cx+cw)*w)) + " " + str(int((cy+ch)*h)) + " "
<<<<<<< HEAD
                myRaspConnection.send(msg)

                # 当树莓派连接成功时，发送消息
                # error = myRaspConnection.mySocket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                # if error != 0:
                #     myRaspConnection.send(msg)
=======
                # myRaspConnection.send(msg)

                # 当树莓派连接成功时，发送消息
                error = myRaspConnection.mySocket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if error != 0:
                    myRaspConnection.send(msg)
>>>>>>> 4732386cdee22c786b3e2789fd83ffcf44fcc849
        
        keypoints = pose.process(image)
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        if hasattr(lm, 'landmark'):
            # 获得关键点的坐标      
            # 左肩
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            # 右肩
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

            # 计算左右肩膀之间的距离，判断是否是侧面
            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

            # Assist to align the camera to point at the side view of the person.
            # Offset threshold 30 is based on results obtained from analysis over 100 samples.
            if offset > 100:
                # 左耳
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                # 右耳
                r_ear_x = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
                r_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].y * h)
                # 左眼 
                l_eye_x = int(lm.landmark[lmPose.LEFT_EYE].x * w)
                l_eye_y = int(lm.landmark[lmPose.LEFT_EYE].y * h)
                # 右眼
                r_eye_x = int(lm.landmark[lmPose.RIGHT_EYE].x * w)
                r_eye_y = int(lm.landmark[lmPose.RIGHT_EYE].y * h)
                cv2.putText(image, str(int(offset)) + " front", (w - 150, 30), font, 0.9, blue, 2)
                # 计算角度
                ear_inclination = findAngle_hor(l_ear_x, l_ear_y, r_ear_x, r_ear_y)
                eye_inclination = findAngle_hor(l_eye_x, l_eye_y, r_eye_x, r_eye_y)

                # 绘制关键点
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
                cv2.circle(image, (l_eye_x, l_eye_y), 7, yellow, -1)

                # Let's take y - coordinate of P3 100px above x1,  for display elegance.
                # Although we are taking y = 0 while calculating angle between P1,P2,P3.
                cv2.circle(image, (r_eye_x, r_eye_y), 7, pink, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
                cv2.circle(image, (r_ear_x, r_ear_y), 7, pink, -1)

                angle_text_string = 'ear : ' + str(int(ear_inclination)) + '  eye : ' + str(int(eye_inclination))

                # Determine whether good posture or bad posture.
                # The threshold angles have been set based on intuition.
                if ear_inclination < 15 and eye_inclination < 15:
                    bad_frames = 0
                    good_frames += 1

                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(ear_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(eye_inclination)), (l_eye_x + 10, l_eye_y), font, 0.9, light_green, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                    cv2.line(image, (l_ear_x, l_ear_y), (l_eye_x, l_eye_y), green, 4)
                    cv2.line(image, (l_eye_x, l_eye_y), (r_eye_x, r_eye_y), green, 4)
                    cv2.line(image, (r_eye_x, r_eye_y), (r_ear_x, r_ear_y), green, 4)
                    cv2.line(image, (r_ear_x, r_ear_y), (r_shldr_x, r_shldr_y), green, 4)

                else:
                    good_frames = 0
                    bad_frames += 1

                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                    cv2.putText(image, str(int(ear_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                    cv2.putText(image, str(int(eye_inclination)), (l_eye_x + 10, l_eye_y), font, 0.9, red, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                    cv2.line(image, (l_ear_x, l_ear_y), (l_eye_x, l_eye_y), red, 4)
                    cv2.line(image, (l_eye_x, l_eye_y), (r_eye_x, r_eye_y), red, 4)
                    cv2.line(image, (r_eye_x, r_eye_y), (r_ear_x, r_ear_y), red, 4)
                    cv2.line(image, (r_ear_x, r_ear_y), (r_shldr_x, r_shldr_y), red, 4)

            else:
                # 左耳
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                # 左臀
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)
                cv2.putText(image, str(int(offset)) + " side", (w - 150, 30), font, 0.9, dark_blue, 2)
                # Calculate angles.
                neck_inclination = findAngle_ver(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle_ver(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                # Draw landmarks.
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

                # Let's take y - coordinate of P3 100px above x1,  for display elegance.
                # Although we are taking y = 0 while calculating angle between P1,P2,P3.
                cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

                # Similarly, here we are taking y - coordinate 100px above x1. Note that
                # you can take any value for y, not necessarily 100 or 200 pixels.
                cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

                # Text string for display.
                angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

                # Determine whether good posture or bad posture.
                # The threshold angles have been set based on intuition.
                if neck_inclination < 40 and torso_inclination < 10:
                    bad_frames = 0
                    good_frames += 1

                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

                else:
                    good_frames = 0
                    bad_frames += 1

                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                    cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                    cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)
            
            # Calculate the time of remaining in a particular posture.
            good_time = (1 / fps) * good_frames
            bad_time =  (1 / fps) * bad_frames

            # 打印帧率和姿势时间
            now  = time.time()
            fps_time = now - start_time
            start_time = now
            fps_txt = 1 / fps_time
            cv2.putText(image, 'FPS : ' + str(int(fps_txt)), (w - 150, 60), font, 0.9, blue, 2)

            # Pose time.
            if good_time > 0:
                time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
                cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
            else:
                time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
                cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

            # 如果保持错误的时间超过3分钟，发送警告
            if bad_time > 5:
                sendWarning()

        # cv2.rectangle(frame, (int(cx*w) , int(cy*h)), (int((cx+cw)*w) , int((cy+ch)*h)),(0, 255, 0), 2)  
        
        frame = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        cv2.imshow("video",image)
        c= cv2.waitKey(1) & 0xff 

        if c==27:
            capture.release()
            break
    print("Video Detection Done!")
    capture.release()
    cv2.destroyAllWindows()

