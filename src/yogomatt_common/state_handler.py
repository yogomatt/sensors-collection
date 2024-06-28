#import RPi.GPIO as GPIO
#import time

#BUTTON_PIN = 16
#LED_PIN = 18


#def button_callback(channel):
#  print('button pushed')
#  time.sleep(0.1)
#  button_state = GPIO.input(BUTTON_PIN)

#  if button_state == GPIO.LOW:
#    GPIO.output(LED_PIN, GPIO.HIGH)
#  else:
#    GPIO.output(LED_PIN, GPIO.LOW)

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(LED_PIN, GPIO.OUT)
#GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # off

#GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback)

#message = input("Press enter to quit\n")

#GPIO.cleanup()

from gpiozero import LED

led = LED(14)
#button = Button(4)

def turn_on_state():
  led.on()

def turn_off_state():
  led.off()

#button.when_pressed = turn_on_led
#button.when_released = turn_off_led

