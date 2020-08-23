# opencv-project1

- capture video from default webcam

- face detection

- crop image to area of interest

- render face in a 'port hole'

# Requirements

Requirements

- MacOSX 10.15.6 Catalina

- WebCam

- Python 3.8.5 64-bit

- Python OpenCV
  $ pip3 install opencv-python

# Instructions

## Execute Python Script

- $ python3 main.py

## Execute Unit Tests

- $ python3 test.py

## Controls

- q - quit
- opencv window controls
  - mouse-wheel / trackpad-two-fingers - zoom in/out
  - left mouse drag - pan
  - right mouse - view menu of options for pan/zoom

# MacOS Catalina - Crash at startup

If python crashes when starting script:
- It appears MacOS-Catalina wants to make sure your application (/terminal) has permission to access the camera
- Commonly seeing this crash when running from terminal with Visual Studio Code
- Python is successfully able to access Video Camera when running from iterm

# Further Ideas

- Apply filter to face
    - grayscale
    - cartoon
    - tint colour of eyes
- adjust zoom/tightness around face
    - zoom in/out keys
- State machine 
  - capture/choose
  - review
  - save
- Stabiliser
  - basic low pass filter on each of x,y,w,h to reduce jittering of window
  - track multiple face areas, and precent rapid switching between faces
- resize
  - experiment with different resize algorithms - nearest, linear, bicubic, lancosz
- apply mask to final 'porthole' image, to cut away the extra material around the porthole

