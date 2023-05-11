
<p align ="center" width="100%">
<img
  src=https://d1tlzifd8jdoy4.cloudfront.net/wp-content/uploads/2020/05/795316b92fc766b0181f6fef074f03fa-1.png
     width = 600
     height= 300
     style="align:center">
</p>

## Pose Estimation model: https://google.github.io/mediapipe/solutions/pose.html

# Usage

<p align ="center" width ="50%">
<img
  src= "./gui&etc_pics/gui_screenshot.png"
  alt="Alt text"
  title="Optional title"
  width=700
  height=500
  style="align:center">
</p>

# Landmark and video selection menu screen
This screen allows the user to select the landmarks they are interested in tracking and this is indicated by the button turning green. The browse button lets the user chose a video from their file system. If the video is the correct format, then the "play video" button turns green as well. Clicking play shows the video with the selected landmarks and then outputs a csv file and a video copy with the selected landmarks

<p align ="center" width ="30%">
<img
  src= "./gui&etc_pics/original_and_out_example.png"
  alt="Alt text"
  title="Optional title"
  width=700
  height=500
  style="align:center">
</p>

<p align ="center" width ="30%">
<img
  src= "./gui&etc_pics/out_ex.png"
  alt="Alt text"
  title="Optional title"
  width=700
  height=500
  style="align:center">
</p>




# Setup
- MacOS (intel chip)
  - use pip to install the following:
    - pygame
    - opencv-python
    - mediapipe
    - tkinter
    - numpy

- to install mediapipe for raspberryPi see this quick start guide: https://github.com/robo27918/Senior-Project-Mobility-Scooter-ML/blob/main/MediepipeSetup.md
