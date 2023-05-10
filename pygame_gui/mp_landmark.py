import mediapipe as mp
mp_pose = mp.solutions.pose
#face landmarks:

nose_idx = mp_pose.PoseLandmark.NOSE.value

l_eye_inner_idx = mp_pose.PoseLandmark.LEFT_EYE_INNER.value
l_eye_idx = mp_pose.PoseLandmark.LEFT_EYE.value
l_eye_outer_idx = mp_pose.PoseLandmark.LEFT_EYE_OUTER.value

r_eye_inner_idx = mp_pose.PoseLandmark.RIGHT_EYE_INNER.value
r_eye_idx = mp_pose.PoseLandmark.RIGHT_EYE.value
r_eye_outer_idx = mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value

l_ear_idx = mp_pose.PoseLandmark.LEFT_EAR.value
r_ear_idx = mp_pose.PoseLandmark.RIGHT_EAR.value

l_mouth_idx = mp_pose.PoseLandmark.MOUTH_LEFT.value
r_mouth_idx = mp_pose.PoseLandmark.MOUTH_RIGHT.value

face_landmarks = [nose_idx,l_eye_inner_idx, l_eye_idx, l_eye_outer_idx, 
                  r_eye_inner_idx, r_eye_idx, r_eye_outer_idx,
                  l_ear_idx, r_ear_idx, l_mouth_idx, r_mouth_idx]

#---- hand landmarks
l_pinky_idx = mp_pose.PoseLandmark.LEFT_PINKY.value
r_pinky_idx = mp_pose.PoseLandmark.RIGHT_PINKY.value
l_thumb_idx = mp_pose.PoseLandmark.LEFT_THUMB.value
r_thumb_idx = mp_pose.PoseLandmark.RIGHT_THUMB.value
l_index_idx = mp_pose.PoseLandmark.RIGHT_INDEX.value
r_index_idx = mp_pose.PoseLandmark.LEFT_INDEX.value

## ---- the essential landmarks -----
l_shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
r_shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
l_elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
r_elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
l_wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
r_wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value

#make the dictionary for csv stuff

landmark_dict = {
 nose_idx:"Nose",

l_eye_inner_idx:"left-eye-inner",
l_eye_idx : "left_eye",
l_eye_outer_idx :"left_eye-outer",
r_eye_inner_idx :"right-eye-inner",
r_eye_idx :"right-eye",
r_eye_outer_idx:"right-eye-outer",
l_ear_idx :"left-ear",
r_ear_idx :"right-ear",
l_mouth_idx:"left-mouth",
r_mouth_idx :"right-mouth",

l_pinky_idx: "left-pinky" ,
r_pinky_idx:"right-pinky" ,
l_thumb_idx:"left-thumb",
r_thumb_idx:"right-thumb",
l_index_idx:"left-index",
r_index_idx:"right-index",
l_shoulder_idx:"left-shoulder" ,
r_shoulder_idx:"right-shoulder",
l_elbow_idx:"left-elbow",
r_elbow_idx:"right-elbow",
l_wrist_idx:"left-wrist",
r_wrist_idx:"right-wrist",
}