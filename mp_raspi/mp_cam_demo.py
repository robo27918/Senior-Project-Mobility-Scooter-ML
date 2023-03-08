import cv2
import mediapipe as mp
from FPSmetric import FPSmetric # weird i know, but this is how we avoid TypeError: module object is not callable
import time
cap = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mp_pose.Pose()
start_time = time.time()
fpsMetric = FPSmetric(start_time)

while True:
     ret,frame = cap.read()
     
     if not ret:
         print("Error:Could not read from the camera!")
         
     
     #flipped =cv2.flip(frame,flipCode=-1)
     frame1 = cv2.resize(frame,(700,480))
     rgb_img = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
     
     result = pose.process(rgb_img)
     
     #print(result.pose_landmarks)
     
     mpDraw.draw_landmarks(frame1,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
     frame1 = fpsMetric(frame1)
     cv2.imshow("Mediapipe Demo",frame1)
     finished_time = time.time()
     print("elapsed_time:", finished_time - start_time,"\n")
     
    
    
     key = cv2.waitKey(1) & 0xFF
     if key == ord('q'):
         break
