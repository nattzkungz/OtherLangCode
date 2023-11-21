# Raspberry Pi RC Car using DS4 + Keyboard Project

## Setup
###Installation Step (Raspbian OS):

1. Open command line and navigate the command window to this folder
2. Input ```chmod +x <setup.sh path>```
3. Input ```chmod +x <startupSequence.sh>```
3. Run setup.sh

###Start Up step:
1. Navigate the command window to this folder
2. Run "startupSequence.sh"
3. Access the camera feed via VLC, use the address: ```tcp/h264://<raspberry pi address>:8494``` to connect to the network feed
##### NOTE: Both raspberry pi and computer must be on the same network circle


## Manual
#### NOTE: Automatic Emergency Braking System only works on Keyboard input, DS4 Input does not support this feature

### For keyboard:
w: forward (speed +10 max 100)__
s: backward (speed = 25)__
a: left (servo duty -0.25 until 5.0)__
d: right (servo duty +0.25 until 8)__
spacebar: brake__
m: middle (servo duty = 6.5)__
h,j,k,l: playsound__

### For DS4:

L3 Stick to turn (Real time steering)__
X,Triangle,O, down arrow: playsound__
R2: variable accelerator (Forward)__
L2: variable reverser (Backward)__
Square: Brake__

##### NOTE: Both R2 and L2 have a deadzone from unpressed to around the middle, so press more to accelerate forward or backward

### Created by @whaichill


