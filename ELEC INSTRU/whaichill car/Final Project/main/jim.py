# Importing Libraries
import RPi.GPIO as GPIO
import time
import os
from getkey import getkey, keys

# Setting GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# GPIO Pin Configuration
# Servo
SERVO_PIN = 17
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Motor
MOTOR_PWM_PIN = 12
GPIO.setup(MOTOR_PWM_PIN, GPIO.OUT)

# Ultrasonic Sensors
# Front
FRONT_TRIGGER = 20
FRONT_ECHO = 21
GPIO.setup(FRONT_TRIGGER, GPIO.OUT)
GPIO.setup(FRONT_ECHO, GPIO.IN)

# Back
BACK_TRIGGER = 18
BACK_ECHO = 23
GPIO.setup(BACK_TRIGGER, GPIO.OUT)
GPIO.setup(BACK_ECHO, GPIO.IN)

# Setting up PWM
servo = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for servo
motor_pwm = GPIO.PWM(MOTOR_PWM_PIN, 100)  # 100 Hz for motor

# Initializing PWM
servo.start(7.5)  # Neutral position (90 degrees)
motor_pwm.start(0)  # Motor off

# Variables to track current state
servo_angle = 90  # Initial angle
motor_speed = 0   # Initial speed (0%)
front_distance = 100  # Initial front distance
back_distance = 100   # Initial back distance
OBSTACLE_THRESHOLD = 20  # Stop the car if obstacle is closer than 20 cm

# Function to display the current status
def display_status():
    os.system('clear')  # Clear the console for a clean display
    print(f"Current Speed: {motor_speed}%")
    print(f"Servo Angle: {servo_angle}°")
    print(f"Front Distance: {front_distance:.1f} cm")
    print(f"Back Distance: {back_distance:.1f} cm")

# Function to set the servo angle
def set_servo_angle(angle):
    global servo_angle
    servo_angle = max(0, min(180, angle))  # Constrain angle between 0° and 180°
    duty_cycle = (servo_angle / 18) + 2.5  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty_cycle)

# Function to set the motor speed
def set_motor_speed(speed):
    global motor_speed
    motor_speed = max(0, min(100, speed))  # Constrain speed between 0% and 100%
    motor_pwm.ChangeDutyCycle(motor_speed)

# Function to measure distance using ultrasonic sensors
def measure_distance(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    # Record the time of the signal's travel
    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    # Calculate the distance (speed of sound = 34300 cm/s)
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

# Function to check for obstacles
def check_obstacles():
    global front_distance, back_distance
    front_distance = measure_distance(FRONT_TRIGGER, FRONT_ECHO)
    back_distance = measure_distance(BACK_TRIGGER, BACK_ECHO)

    # Stop the motor if an obstacle is detected within the threshold
    if front_distance < OBSTACLE_THRESHOLD or back_distance < OBSTACLE_THRESHOLD:
        print("Obstacle detected! Stopping the car...")
        set_motor_speed(0)

# Cleanup GPIO and PWM
def cleanup():
    servo.stop()
    motor_pwm.stop()
    GPIO.cleanup()

# Main keyboard control function
def keyboard_control():
    print("Use the following keys to control:")
    print("'w' - Increase Speed | 's' - Decrease Speed")
    print("'a' - Turn Servo Left | 'd' - Turn Servo Right")
    print("'q' - Quit the Program")
    display_status()

    try:
        while True:
            # Continuously check for obstacles
            check_obstacles()
            display_status()

            # Get key input without Enter
            key = getkey()

            if key == 'w':  # Increase speed
                set_motor_speed(motor_speed + 10)
            elif key == 's':  # Decrease speed
                set_motor_speed(motor_speed - 10)
            elif key == 'a':  # Turn servo left
                set_servo_angle(servo_angle - 10)
            elif key == 'd':  # Turn servo right
                set_servo_angle(servo_angle + 10)
            elif key == 'q':  # Quit the program
                print("Exiting program...")
                break
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting program...")
    finally:
        cleanup()

# Entry point of the program
if __name__ == "__main__":
    print("System initializing...")
    display_status()
    keyboard_control()
