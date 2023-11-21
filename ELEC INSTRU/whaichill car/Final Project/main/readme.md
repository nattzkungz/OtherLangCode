# Raspberry Pi RC Car using DS4 + Keyboard Project

## Setup
### Installation Step (Raspbian OS):

1. Open command line and navigate the command window to this folder
2. Input ```chmod +x <setup.sh path>```
3. Input ```chmod +x <startupSequence.sh>```
3. Run setup.sh

### Start Up step:
1. Navigate the command window to this folder
2. Run "startupSequence.sh"
3. Access the camera feed via VLC, use the address: ```tcp/h264://<raspberry pi address>:8494``` to connect to the network feed
##### NOTE: Both raspberry pi and computer must be on the same network circle


## Manual
#### NOTE: Automatic Emergency Braking System only works on Keyboard input, DS4 Input does not support this feature

### For keyboard:
w: forward (speed +10 max 100)  
s: backward (speed = 25)  
a: left (servo duty -0.25 until 5.0)  
d: right (servo duty +0.25 until 8)  
spacebar: brake  
m: middle (servo duty = 6.5)  
h,j,k,l: playsound  

### For DS4:

L3 Stick to turn (Real time steering)  
X,Triangle,O, down arrow: playsound  
R2: variable accelerator (Forward)  
L2: variable reverser (Backward)  
Square: Brake  

##### NOTE: Both R2 and L2 have a deadzone from unpressed to around the middle, so press more to accelerate forward or backward

## Useful Information
Command to start streaming camera manually:  

```libcamera-vid -t0 --width 1920 --height 1080 --framerate 30 --nopreview --codec h264 --profile high --intra 5 --listen -o tcp://0.0.0.0:8494```

NOTE: The video feed is streaming in h264 format, requiring the use of VLC to open the stream  

To access video feed:  

1. Open VLC
2. Find open network content and type in: tcp/h264://<raspberry pi address>:8494
3. Enjoy


## Known Issues:
1. Automated Emergency Braking System (AEB) requires constant user input to work
2. AEB does not work when using DS4 Controller
3. Weak Wifi signal, video stream would usually cut off and delay  
This have been identified as Raspberry Pi fault since the wifi antenna equipped on the device is low power unit  
Therefore, wifi usb stick with external antenna would have help this problem
4. After a period of extensive usage of the device, some function would not work due to heat (ex. Locked servo, Wifi is disconnected randomly, etc.)
5. Video Stream is hard to access and require manual stream restart as the receiver device is disconnected

## Simplified Program Flowchart

```+----------------------+
|   Setup and          |
|   Initialization     |
|                      |
| - Import Libraries   |
| - Setup GPIO Pins    |
| - Setup PWM          |
| - Initialize Sound   |
|   Components         |
+----------------------+
           |
           v
+----------------------+
|    Keyboard Input    |
|        Handling       |
|                      |
| - Check Keys         |
|   (w, s, a, d, etc)  |
| - Handle Movement    |
|   Keys (w, s, a, d)  |
| - Handle Sound Keys  |
|   (h, j, k, l, etc)  |
| - Handle Special Keys|
|   (p, m, q, etc)      |
+----------------------+
           |
           v
+----------------------+
| Ultrasonic Sensor     |
| Functions            |
|                      |
| - Distance Back      |
|   Calculation        |
| - Distance Front     |
|   Calculation        |
+----------------------+
           |
           v
+----------------------+
|  Movement Functions  |
|   (Front and Back,    |
|    Brake, Middle,     |
|    Drag Race)         |
|                      |
| - Front and Back      |
|   Movement Function  |
| - Brake Movement      |
|   Function            |
| - Middle Movement     |
|   Function            |
| - Drag Race Function  |
| - ds4controller       |
| - driverMotorConverter|
| - servoConverter      |
+----------------------+
           |
           v
+----------------------+
|   Receiving Input    |
|   from User Functions |
|  (Keyboard and        |
|   Joystick)           |
|                      |
| - horn                |
| - bmwSound            |
| - farting             |
| - wallsSound          |
| - emerBrakeSound      |
| - joystickSafetyCheck |
+----------------------+
```

### Created by @whaichill_group

Member:  
Thanakrit Trongmahavisate   
Sarun Khieonavavongsa  
Jirath Yongvivathanakul  
Pawarisa Tanpoonkiat  


