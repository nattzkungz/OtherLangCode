# Importing Libraries
import RPi.GPIO as GPIO
import time
from playsound import playsound

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

# Setting up PWM
servo = GPIO.PWM(SERVO_PIN, 50)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)
servo.start(0)

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

def horn():
    playsound("horn.wav")
# Receiving input from user

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
        key = getkey()
        # Braking
        if key == " ":
            brake()
            speed = 0
        if key == "h":
            horn()
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
    temp = (value/32767)*100
    return round(temp, 2)

def servoConverter(value):
    temp = (value/32767) * 1.25
    return round(temp, 2)

def ds4controller():
    from pyPS4Controller.controller import Controller
    class MyController(Controller):
        duty = 6.5
        speed = 0
        def __init__(self, **kwargs):
            Controller.__init__(self, **kwargs)
        
        def on_L2_press(self):
            print("Brake")
            brake()
        
        def on_L2_release(self):
            middle()

        def on_R2_press(self, value):
            print("Forward")
            front_and_back(GPIO.HIGH, driverMotorConverter(value))

        def on_L3_right(self, value):
            print("Right")
            turn = servoConverter(value)
            duty += turn
            if duty <= 7.75:
                servo.ChangeDutyCycle(duty)
            else:
                print("Cannot turn right anymore")

        def on_L3_left(self, value):
            print("Left")
            turn = servoConverter(value)
            duty -= turn
            if duty >= 5.25:
                servo.ChangeDutyCycle(duty)
            else:
                print("Cannot turn left anymore")

        def on_triangle_release(self):
            dragRace()
        
        def on_square_press(self):
            horn()
    
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

# Main loop for the program
while modeSelect != "kb" and modeSelect != "ds4":
    modeSelect = input("Keyboard or Joystick? (kb/ds4): ")
    if modeSelect == "kb":
        keyboard()
    elif modeSelect == "ds4":
        ds4controller()
    else:
        print("Please delect a mode")

# Cleaning up
servo.stop()
p1.stop()
p2.stop()
GPIO.cleanup()