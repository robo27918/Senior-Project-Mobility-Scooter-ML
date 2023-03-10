<p align ="center" width="100%">
<img
  src=https://d1tlzifd8jdoy4.cloudfront.net/wp-content/uploads/2020/05/795316b92fc766b0181f6fef074f03fa-1.png
     width = 600
     height= 300
     style="align:center">
</p>

<p align ="center" width ="100%">
<img
  src= "https://www.raspberrypi.com/app/uploads/2017/06/Powered-by-Raspberry-Pi-Logo_Outline-Colour-Screen-500x153.png"
  alt="Alt text"
  title="Optional title"
  style="align:center">
</p>

# Requirements
  The first thing you will need to do is get the correct OS installed on your microSD card. Due to issues with the camera module software in the new 64-bit OS and OpenCV, we are forced to use the Legacy OS known as Buster. 
Go to https://www.raspberrypi.com/software/, and install the Raspberry Pi Imager software for your operating system. Once Pi Imager is installed, install Buster OS onto your microSD card. Use the image below as a reference, if any confusion should arise.

<p align ="center" width ="50%">
<img
  src= "./Mediapipe_setup_pics/RaspiImager.png"
  alt="Alt text"
  title="Optional title"
  width=700
  height=500
  style="align:center">
</p>

# Step 1: Camera setup and Test
  Once you've installed the Buster operating system and hooked up your camera module, you want to enable the camera. To do this click on the applications menu at the top left corner, then click on Preferences, and then Raspberry Pi Configuration. The image below shows the tab you want to navigate to and how to enable the camera. After enabling, you will have to reboot your Raspberry Pi
 
 <p align ="center" width ="50%">
<img
  src= "./Mediapipe_setup_pics/cam_setup.png"
  alt="Alt text"
  title="Optional title"
  width=700
  height=400
  style="align:center">
</p>
  
Now is the time to test that the camera module works. To do this, enter the following command in the terminal

```
raspistill -o Desktop/test_img.jpg
```
This command will enable the camera for 5 seconds, and thereafter send the image to your desktop.

# Step 2 [optional]: Installing virtualenv 


I think its good practice to use virtual environments. This can prevent a lot of headaches later on. But if you want to skip this step, then proceed to the next step, but you've warned.

So if you kept reading, the first thing you need to do is run the following command in the terminal 

```
pip3 install virtualenv virtualenvwrapper
```

Next open .bashrc script file with the following command:

```
nano ~/.bashrc
```

Then, add the follwing to the bottom of the .bashrc file

```
#Virtualenvwrapper settings:
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh
export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin
```

Thereafter, reload the file with the following command:

```
source ~/.bashrc
```
Now that you have virtualenv installed, you want to make a virtual environment. To do so, enter the following command (Note: the name can be whaever you like, but I chose mediapipe-raspi)

```
mkvirtualenv mediapipe-rapsi
```

To work inside this environment, enter the following:

```
workon mediapipe-raspi

```
To exit the environment enter:

```
deactivate
```

To list all the Python packages in the virtual environment enter:

```
pip freeze
```
# Step 3: Installing OpenCV:
OpenCV is a 'requirment' to be able to work with mediapipe, so lets get that installed first. 

First, lets make sure that our system is up-to-date so that we can avoid any issues. Thus, paste the following into your terminal:

```
sudo apt update
```

```
sudo apt upgrade
```

Now lets install numpy. The version we want is one that is compatiable with Python 3.7, otherwise we might get some errors when trying to install OpenCV later on. Thus, run the following command:

```
python3 -m pip install numpy==1.16.2
```

Now we need to install OpenCV (version: 4.3.0.38) with the following command:

```
python3 -m pip install opencv-python==4.3.0.38
```
Also install opencv-contrib-python (Version:4.1.0.25)
```
python3 -m pip install opencv-contrib-python==4.1.0.25
```

Just to be sure that we can make use of the opencv library, install the following dependencies:
```
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev

```

Now to make sure that OpenCV can be imported as a module do:

```
python3
import cv2
```

Hopefully, no errors should come up.

# Step 4: Installing Mediapipe:

Let's now get mediapipe onto the environment. We will be using Version 0.8.4.0

```
python3 -m pip install mediapipe-rpi4==0.8.4.0
```
If you get an HTTP timeout error. Simply reboot your system through either the application menu or by entering:

```
sudo reboot
```

After the installation is successfully completed, open the Python interpreter and trying importing mediapipe by pasting:

```
import mediapipe
```
You will most likely get an error that reads as follows:
>TypeError: Descriptors cannot be created directly

To fix this we simply need to downgrade the verision of protobuf package as follows:

```
python3 -m pip install protobuf==3.20.*
```

Now try importing mediapipe again. Hopefully, the import should be successful and no errors should come up!
