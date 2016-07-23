import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Button:
    def __init__(self,pin,callback):
        self.pin = pin
        self.callback = callback
        self.oldButton = 1
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        button = GPIO.input(self.pin)
        if button == False and self.oldButton:
            self.callback()
        self.oldButton = button

class RotaryEnc:
    def __init__(self,PinA,PinB,button,rotaryCallback,buttonCallback):
        self.PinA = PinA
        self.PinB = PinB
        self.button = Button(button, buttonCallback)
        self.rotaryCallback = rotaryCallback
        self.buttonCallback = buttonCallback
        self.oldPinA = 0
        self.oldButton = 1

        GPIO.setup(self.PinA, GPIO.IN)
        GPIO.setup(self.PinB, GPIO.IN)

    def read(self):
        # function to read the rotary encoder
        pinA = GPIO.input(self.PinA)
        pinB = GPIO.input(self.PinB)

        if pinA and not self.oldPinA:
            if not pinB:
                self.rotaryCallback(True)
            else:
                self.rotaryCallback(False)

        self.oldPinA = pinA

    def read_button(self):
        self.button.read()

