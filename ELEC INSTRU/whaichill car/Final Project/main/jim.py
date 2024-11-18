# Importing Libraries
import RPi.GPIO as GPIO
import time
import os

# Setting GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# GPIO Pin Configuration
# Servo
SERVO_PIN = 17
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Motor
MOTOR_PWM_PIN = 12
GPIO.setup(MOTOR_PWM_PIN, GPIO.OUT)

# Setting up PWM
servo = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for servo
motor_pwm = GPIO.PWM(MOTOR_PWM_PIN, 100)  # 100 Hz for motor

# Initializing PWM
servo.start(7.5)  # Neutral position (90 degrees)
motor_pwm.start(0)  # Motor off

# Variables to track current state
servo_angle = 90  # Initial angle
motor_speed = 0   # Initial speed (0%)

# Function to display the current status
def display_status():
    os.system('clear')  # Clear the console for a clean display
    print(f"Current Speed: {motor_speed}%")
    print(f"Servo Angle: {servo_angle}°")

# Function to set the servo angle
def set_servo_angle(angle):
    global servo_angle
    servo_angle = max(0, min(180, angle))  # Constrain angle between 0° and 180°
    duty_cycle = (servo_angle / 18) + 2.5  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty_cycle)
    display_status()

# Function to set the motor speed
def set_motor_speed(speed):
    global motor_speed
    motor_speed = max(0, min(100, speed))  # Constrain speed between 0% and 100%
    motor_pwm.ChangeDutyCycle(motor_speed)
    display_status()

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
            # Get user input
            key = input("Enter command: ").strip().lower()
            
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
            else:
                print("Invalid command! Use 'w', 's', 'a', 'd', or 'q'.")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting program...")
    finally:
        cleanup()

# Entry point of the program
if __name__ == "__main__":
    print("System initializing...")
    display_status()
    keyboard_control()
