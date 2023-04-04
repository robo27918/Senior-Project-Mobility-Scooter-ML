import pygame
import sys
import mediapipe as mp
from Engine import MediaPipeEngine
"""
We want to select a few of the limbs as options for buttons --> but eventually we may want to incorporate all 33 limbs
"""
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

l_shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
r_shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
l_elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
r_elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
l_wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
r_wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value
l_pinky_idx = mp_pose.PoseLandmark.LEFT_PINKY.value
r_pinky_idx = mp_pose.PoseLandmark.RIGHT_PINKY.value

#list to append user gui choices and send over to Engine

pygame.init()
'''
    Basic function to encapsulate the drawing routine
'''
def draw_button(screen,color,clicked_color,x,y,width,height,text,clicked):
    if clicked:
        pygame.draw.rect(screen,clicked_color,(x,y,width,height))
    else:
        pygame.draw.rect(screen,color,(x,y,width,height))
    font=pygame.font.Font(None,30)
    text_surface= font.render(text,True,BLACK)
    text_rect=text_surface.get_rect(center=(x+width/2, y + height/2))
    screen.blit(text_surface,text_rect)

def is_button_clicked(button_x,button_y,button_width,button_height):
    return button_x <= mouse_pos[0]<= button_x +button_width and button_y<= mouse_pos[1] <= button_y + button_height

def reset_button(button):
    if button:
        return not button
       
        

#colors to be used for buttons
WHITE = (255, 255, 255)
GREY = (128,128,128)
GREEN = (127,255,0)
BLACK = (0, 0, 0)
RED = (255,0,0)




WINDOW_SIZE = (920,920)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("MediaPipe Demo selection screen")

#setting up parameters for each button
button_width = 150
button_height = 50
button_color = GREY
button_clicked_color=GREEN

button1_x = 200
button1_y =200
button1_text = "left shoulder"
button1_clicked = False

button2_x = 400
button2_y = 200
button2_text = "right shoulder"
button2_clicked = False

button3_x = 200
button3_y = 300
button3_text = "left elbow"
button3_clicked = False

button4_x = 400
button4_y = 300
button4_text = "right elbow"
button4_clicked = False

button5_x = 200
button5_y = 400
button5_text = "left wrist"
button5_clicked = False

button6_x = 400
button6_y = 400
button6_text = "right wrist"
button6_clicked = False

button7_x = 200
button7_y = 500
button7_text = "left pinky"
button7_clicked = False

button8_x = 400
button8_y = 500
button8_text = "right pinky"
button8_clicked = False



on_engine_button_x  = 600
on_engine_button_y = 200
on_engine_button_text = "Start webcam"
on_engine_button_clicked = False
on_button_clicked_color = RED;

user_landmark_choices = []
while True:
   
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_button_clicked(button1_x,button1_y,button_width,button_height):
                button1_clicked = not button1_clicked
                user_landmark_choices.append(l_shoulder_idx);
            if is_button_clicked(button2_x,button2_y,button_width,button_height):
                button2_clicked = not button2_clicked
                user_landmark_choices.append(r_shoulder_idx)
            if is_button_clicked(button3_x,button3_y,button_width,button_height):
                button3_clicked = not button3_clicked
                user_landmark_choices.append(l_elbow_idx)
            if is_button_clicked(button4_x,button4_y,button_width,button_height):
                button4_clicked = not button4_clicked
                user_landmark_choices.append(r_elbow_idx)
            if is_button_clicked(button5_x,button5_y,button_width,button_height):
                button5_clicked = not button5_clicked
                user_landmark_choices.append(l_wrist_idx)
            if is_button_clicked(button6_x,button6_y,button_width,button_height):
                button6_clicked = not button6_clicked
                user_landmark_choices.append(r_wrist_idx)
            if is_button_clicked(button7_x,button7_y,button_width,button_height):
                button7_clicked = not button7_clicked
                user_landmark_choices.append(l_pinky_idx)
            if is_button_clicked(button8_x,button8_y,button_width,button_height):
                button8_clicked = not button8_clicked
                user_landmark_choices.append(r_pinky_idx)
           
            #the last check is to see if we can create the new screen for the webcam stuff
            if is_button_clicked(on_engine_button_x, on_engine_button_y,button_width,button_height):
                on_engine_button_clicked = not on_engine_button_clicked
                myEngine = MediaPipeEngine(webcam_id = 0, show=True, custom_objects=None, user_landmark_list=user_landmark_choices);
                myEngine.run()
                button_on_list = [button1_clicked,button2_clicked, button3_clicked,
                                  button4_clicked,button5_clicked,button6_clicked, button7_clicked,
                                  button8_clicked, on_engine_button_clicked ]
                button1_clicked = reset_button(button1_clicked)
                button2_clicked = reset_button(button2_clicked)
                button3_clicked = reset_button(button3_clicked)
                button4_clicked = reset_button(button4_clicked)
                button5_clicked = reset_button(button5_clicked)
                button6_clicked = reset_button(button6_clicked)
                button7_clicked = reset_button(button7_clicked)
                button8_clicked = reset_button(button8_clicked)
                on_engine_button_clicked = reset_button (on_engine_button_clicked)
                user_landmark_choices = []
                print("ok the webcam is off now ")

        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(WHITE)
    draw_button(screen,button_color,button_clicked_color,button1_x,button1_y, button_width, button_height, button1_text, button1_clicked)
    draw_button(screen,button_color,button_clicked_color,button2_x,button2_y, button_width, button_height, button2_text, button2_clicked)
    draw_button(screen,button_color,button_clicked_color,button3_x,button3_y, button_width, button_height, button3_text, button3_clicked)
    draw_button(screen,button_color,button_clicked_color,button4_x,button4_y, button_width, button_height, button4_text, button4_clicked)
    draw_button(screen,button_color,button_clicked_color,button5_x,button5_y, button_width, button_height, button5_text, button5_clicked)
    draw_button(screen,button_color,button_clicked_color,button6_x,button6_y, button_width, button_height, button6_text, button6_clicked)
    draw_button(screen,button_color,button_clicked_color,button7_x,button7_y, button_width, button_height, button7_text, button7_clicked)
    draw_button(screen,button_color,button_clicked_color,button8_x,button8_y, button_width, button_height, button8_text, button8_clicked)
    draw_button(screen, button_color, button_clicked_color, on_engine_button_x, on_engine_button_y, button_width,button_height, on_engine_button_text, on_engine_button_clicked)
    pygame.display.update()