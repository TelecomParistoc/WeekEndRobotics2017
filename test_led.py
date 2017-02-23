import RPi.GPIO as GPIO

state=GPIO.gpio_function(12)
print(state)
