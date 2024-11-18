# Importing Libraries
import RPi.GPIO as GPIO
import time

# Setting GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Setting up GPIO pins
# Servo
SERVO_PIN = 17
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Motor
AN2 = 13
AN1 = 12
DIG2 = 24
DIG1 = 26
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)

# Ultrasonic Sensor
# BACK
TRIGGER = 18
ECHO = 23
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# FRONT
TRIGGER_2 = 20
ECHO_2 = 21
GPIO.setup(TRIGGER_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)

# Setting up PWM
servo = GPIO.PWM(SERVO_PIN, 50)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)
servo.start(0)

# UltraSonic Sensor
def distance_back():
    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34900 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34900) / 2
    return distance

def distance_front():
    # set Trigger to HIGH
    GPIO.output(TRIGGER_2, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER_2, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(ECHO_2) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(ECHO_2) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34900 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34900) / 2
    return distance

# Setup function for movement
def front_and_back(movement, speed): # movement = GPIO.HIGH or GPIO.LOW (high for forward, low for backward)
    if speed <= 100:
        GPIO.output(DIG1, movement)
        GPIO.output(DIG2, movement)
        p1.start(speed)
        p2.start(speed)
    else:
        print("Max Speed, cannot go faster")

def brake():
    print("Brake")
    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(0)
    p2.start(0)

def middle():
    print("Middle")
    servo.ChangeDutyCycle(6.5)

def dragRace():
    middle()
    front_and_back(GPIO.HIGH, 100)
    time.sleep(3)
    brake()

########### Receiving input from user ############
# KEYBOARD
def keyboard():

    def turning(direction, pastDuty):
        if direction == "left":
            print("Turning left")
            pastDuty -= 0.25
        elif direction == "right":
            print("Turning right")
            pastDuty += 0.25
        servo.ChangeDutyCycle(pastDuty)
        return pastDuty
    
    from getkey import getkey, keys
    duty = 6.5
    speed = 0
    pastKey = ""


    while True:
        key = input("Input the key, w - forward | s - break\n a - turn left, d - turn right: ")
        distFRONT = round(distance_front(),1)
        distBACK = round(distance_back(),1)
        print(f"Front Space: {distFRONT}")
        print(f"Back Space: {distBACK}")
        count = 0
        print(distFRONT)
        if distFRONT <= 7:
            count = 1
            if count == 1:
                brake()
                print("Distance Too Close\nAutomated Braking Activated")
                time.sleep(2)
            if key == "w":
                count = 1
            else:
                count = 0
        print(distBACK)
        if distBACK <= 5:
            count = 1
            if count == 1:
                brake()
                print("Distance Too Close\nAutomated Braking Activated")
                time.sleep(2)
            if key == "s":
                count = 1
            else:
                count = 0

        # Braking
        if key == " ":
            brake()
            speed = 0

        # DRAG RACE MODE
        if key == "p":
            dragRace()
        # Middle
        if key == "m":
            middle()
            duty = 6.5
        # Forward Backward
        if key == "w":
            if pastKey == "w" and speed < 100:
                speed += 10
                print("forward")
            elif pastKey == "s":
                speed = 0
            else:
                print("Max speed already") 
            front_and_back(GPIO.HIGH, speed)
        elif key == "s":
            speed = 25
            front_and_back(GPIO.LOW, speed)
        # Left Right
        if key == "a":
            if duty >= 5.25:
                duty = turning("left", duty)
            else:
                print("Cannot turn left anymore")
            
        elif key == "d":
            if duty <= 7.75:
                duty = turning("right", duty)
            else:
                print("Cannot turn right anymore")
        print("-----Status-----")
        print("Speed: " + str(speed) + " Duty: " + str(duty))
        print("----------------")
        # Storing past key data
        pastKey = key
        # Exit
        if key == "q":
            break

# JOYSTICK

def driverMotorConverter(value):
    if value < 0:
        return 0
    else:
        temp = (value/32767)*85.0 # Limit to 85% of max speed
        return abs(round(temp, 1))

def servoConverter(value):
    temp = (value/32767) * 1.25
    return round(temp, 2)

def ds4controller():
    from pyPS4Controller.controller import Controller
    class MyController(Controller):
        duty = 6.5
        def __init__(self, **kwargs):
            Controller.__init__(self, **kwargs)
        
        def on_L2_press(self, value):
            print("Backward")
            front_and_back(GPIO.LOW, driverMotorConverter(value))

        def on_L2_release(self):
            front_and_back(GPIO.LOW, 0)

        def on_R2_press(self, value):
            print("Forward")
            front_and_back(GPIO.HIGH, driverMotorConverter(value))

        def on_R2_release(self):
            front_and_back(GPIO.HIGH, 0)

        def on_L3_right(self, value):
            print("Right")
            turn = 6.5 + servoConverter(value)
            servo.ChangeDutyCycle(turn)

        def on_L3_x_at_rest(self):
            middle()
        
        def on_L3_y_at_rest(self):
            middle()
        
        def on_L3_left(self, value):
            print("Left")
            turn = 6.5 + servoConverter(value)
            servo.ChangeDutyCycle(turn)

        def on_square_press(self):
            print("BRAKE")
            brake()

        def on_options_press(self):
            servo.stop()
            p1.stop()
            p2.stop()
            GPIO.cleanup()

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

modeSelect = ""
# Main loop for the program


while modeSelect != "kb" and modeSelect != "ds4":
    modeSelect = input("Keyboard or Joystick? (kb/ds4): ")
    if modeSelect == "kb":
        print("Keyboard Activated")
        keyboard()
    elif modeSelect == "ds4":
        print("DS4 Activated")
        ds4controller()
    else:
        print("Please select a mode")

# Cleaning up
servo.stop()
p1.stop()
p2.stop()
GPIO.cleanup()