import pygame
import sys
import mediapipe as mp
from Engine import MediaPipeEngine
import utils
import tkinter as tk
from tkinter import filedialog
import os
"""
We want to select a few of the limbs as options for buttons --> but eventually we may want to incorporate all 33 limbs
"""
#inits for dialog to get file dialog box
root = tk.Tk()
root.withdraw()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
## --- the not so essential landmarks ---

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



pygame.init()
'''
    Basic function to encapsulate the drawing routine
'''
def draw_button(screen,color,clicked_color,x,y,width,height,text,clicked):
    font=pygame.font.Font(None,30)
    if clicked:
        pygame.draw.rect(screen,clicked_color,(x,y,width,height))
        text_surface= font.render(text,True,BLACK)
    else:
        pygame.draw.rect(screen,color,(x,y,width,height))
        text_surface= font.render(text,True,WHITE)
 
   
    text_rect=text_surface.get_rect(center=(x+width/2, y + height/2))
    screen.blit(text_surface,text_rect)

def is_button_clicked(button_x,button_y,button_width,button_height):
    return button_x <= mouse_pos[0]<= button_x +button_width and button_y<= mouse_pos[1] <= button_y + button_height

def reset_button(button):
    if button:
        return not button
       
def get_video_from_filedir():
    # Use the filedialog module to open the window and get the selected file
    
    return filedialog.askopenfilename()
   
def is_video_file(filepath):
    video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.mkv']
    file_extension = os.path.splitext(filepath)[1]
    if file_extension in video_extensions:
        return True
    return False

#colors to be used for buttons
WHITE = (255, 255, 255)
GREY = (128,128,128)
GREEN = (127,255,0)
BLACK = (0, 0, 0)
RED = (255,0,0)
CYAN = (0, 255, 255)



WINDOW_SIZE = (920,920)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("MediaPipe Demo selection screen")

#setting up parameters for each button
button_width = 150
button_height = 50
button_color = GREY
button_clicked_color=GREEN

button0_x = 300
button0_y = 100
button0_text = "face"
button0_on = False


button1_x = 200
button1_y =200
button1_text = "left shoulder"
button1_on = False

button2_x = 400
button2_y = 200
button2_text = "right shoulder"
button2_on = False

button3_x = 200
button3_y = 300
button3_text = "left elbow"
button3_on = False

button4_x = 400
button4_y = 300
button4_text = "right elbow"
button4_on = False

button5_x = 200
button5_y = 400
button5_text = "left wrist"
button5_on = False

button6_x = 400
button6_y = 400
button6_text = "right wrist"
button6_on = False
runme = None

#---code for the hand buttons---
button7_x = 200
button7_y = 500
button7_text = "left hand"
button7_on = False

button8_x = 400
button8_y = 500
button8_text = "right hand"
button8_on = False

on_engine_button_x  = 600
on_engine_button_y = 200
on_engine_button_text = "Start webcam"
engine_button_on = False
on_button_clicked_color = RED;

on_engine_button_x  = 600
on_engine_button_y = 300
on_engine_button_text = "Start webcam"
engine_button_on = False
on_button_clicked_color = RED;

#making lable to indicate browsing option
myfont = pygame.font.SysFont("monospace",15)
label = myfont.render("Choose a file:",1,BLACK)

#making button to open file select window:
browse_button_x = 600
browse_button_y = 420
browse_button_text = "Browse"

#make a play selected video play button 
play_vid_button_x = 600
play_vid_button_y = 500
play_vid_button_text = "play video"
valid_file = False

#list to append user gui choices and send over to Engine
user_landmark_choices = []
while True:
   
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if is_button_clicked(button0_x,button0_y,button_width,button_height):
                if button0_on: #then turn off (ie remove the limb)
                    for landmark in face_landmarks:
                        user_landmark_choices.remove(landmark)
                    button0_on = not button0_on
                else:
                    button0_on = not button0_on
                    for landmark in face_landmarks:
                        user_landmark_choices.append(landmark);
    
            if is_button_clicked(button1_x,button1_y,button_width,button_height):
                if button1_on: #then turn off (ie remove the limb)
                    user_landmark_choices.remove(l_shoulder_idx)
                    button1_on = not button1_on
                else:
                    button1_on = not button1_on
                    user_landmark_choices.append(l_shoulder_idx);
    
            if is_button_clicked(button2_x,button2_y,button_width,button_height):
                if button2_on:
                    user_landmark_choices.remove(r_shoulder_idx)
                    button2_on = not button2_on
                else:
                    button2_on = not button2_on
                    user_landmark_choices.append(r_shoulder_idx)
            if is_button_clicked(button3_x,button3_y,button_width,button_height):
                if button3_on:
                    button3_on = not button3_on
                    user_landmark_choices.remove(l_elbow_idx)
                else:
                    button3_on = not button3_on
                    user_landmark_choices.append(l_elbow_idx)
            if is_button_clicked(button4_x,button4_y,button_width,button_height):
                 if button4_on:
                    button4_on= not button4_on
                    user_landmark_choices.remove(r_elbow_idx)
                 else:
                    button4_on = not button4_on
                    user_landmark_choices.append(r_elbow_idx)
            if is_button_clicked(button5_x,button5_y,button_width,button_height):
                if button5_on:
                    button5_on = not button5_on
                    user_landmark_choices.remove(l_wrist_idx)
                else:
                    button5_on = not button5_on
                    user_landmark_choices.append(l_wrist_idx)
            if is_button_clicked(button6_x,button6_y,button_width,button_height):
                if button6_on:
                    button6_on = not button6_on
                    user_landmark_choices.remove(r_wrist_idx)
                else:
                    button6_on = not button6_on
                    user_landmark_choices.append(r_wrist_idx)
            if is_button_clicked(button7_x,button7_y,button_width,button_height):
                if button7_on:
                    button7_on = not button7_on
                    user_landmark_choices.remove(l_pinky_idx)
                    user_landmark_choices.remove(l_thumb_idx)
                    user_landmark_choices.remove(l_index_idx)
                else:
                    button7_on = not button7_on
                    user_landmark_choices.append(l_pinky_idx)
                    user_landmark_choices.append(l_thumb_idx)
                    user_landmark_choices.append(l_index_idx)
            if is_button_clicked(button8_x,button8_y,button_width,button_height):
                if button8_on:
                    button8_on = not button8_on
                    user_landmark_choices.remove(r_pinky_idx)
                    user_landmark_choices.remove(r_thumb_idx)
                    user_landmark_choices.remove(r_index_idx)
                else:
                    button8_on = not button8_on
                    user_landmark_choices.append(r_pinky_idx)
                    user_landmark_choices.append(r_thumb_idx)
                    user_landmark_choices.append(r_index_idx)
           
            #the last check is to see if we can create the new screen for the webcam stuff
            if is_button_clicked(on_engine_button_x, on_engine_button_y,button_width,button_height):
                engine_button_on = not engine_button_on
                myEngine = MediaPipeEngine(webcam_id = 0, show=True, custom_objects=None, user_landmark_list=user_landmark_choices);
                myEngine.run()
                
                button0_on = reset_button(button0_on)
                button1_on = reset_button(button1_on)
                button2_on = reset_button(button2_on)
                button3_on = reset_button(button3_on)
                button4_on = reset_button(button4_on)
                button5_on = reset_button(button5_on)
                button6_on = reset_button(button6_on)
                button7_on = reset_button(button7_on)
                button8_on = reset_button(button8_on)
                engine_button_on = reset_button (engine_button_on)
                user_landmark_choices = []
                print("ok the webcam is off now ")
            #handle the browse button selection 
            if is_button_clicked(browse_button_x,browse_button_y,button_width,button_height):
                vid_file = get_video_from_filedir()
                print(vid_file)
                print (is_video_file(vid_file))
                if is_video_file(vid_file):
                    valid_file = not valid_file

            #handle the play vid button assuming it passes the filetype check 

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(CYAN)
    draw_button(screen,button_color,button_clicked_color,button0_x,button0_y, button_width, button_height, button0_text, button0_on)
    draw_button(screen,button_color,button_clicked_color,button1_x,button1_y, button_width, button_height, button1_text, button1_on)
    draw_button(screen,button_color,button_clicked_color,button2_x,button2_y, button_width, button_height, button2_text, button2_on)
    draw_button(screen,button_color,button_clicked_color,button3_x,button3_y, button_width, button_height, button3_text, button3_on)
    draw_button(screen,button_color,button_clicked_color,button4_x,button4_y, button_width, button_height, button4_text, button4_on)
    draw_button(screen,button_color,button_clicked_color,button5_x,button5_y, button_width, button_height, button5_text, button5_on)
    draw_button(screen,button_color,button_clicked_color,button6_x,button6_y, button_width, button_height, button6_text, button6_on)
    draw_button(screen,button_color,button_clicked_color,button7_x,button7_y, button_width, button_height, button7_text, button7_on)
    draw_button(screen,button_color,button_clicked_color,button8_x,button8_y, button_width, button_height, button8_text, button8_on)
    draw_button(screen, button_color, button_clicked_color, on_engine_button_x, on_engine_button_y, button_width,button_height, on_engine_button_text, engine_button_on)
    screen.blit(label,(600,400))
    draw_button(screen,button_color, button_clicked_color,browse_button_x,browse_button_y,button_width,button_height,browse_button_text,False)
    draw_button(screen, button_color, button_clicked_color, play_vid_button_x, play_vid_button_y, button_width,button_height, play_vid_button_text,valid_file)

    pygame.display.update()