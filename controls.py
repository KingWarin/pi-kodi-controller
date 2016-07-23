import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Button:
    ''' Simple Button

    Button needs to know which GPIO-pin it should listen to,
    what to do if it's pressed and can optionally be setup
    so it only triggers once it's pressed or as long as it's
    pressed.
    '''
    def __init__(self,pin,callback,single=True):
        self.pin = pin
        self.callback = callback
        self.oldButton = 1
        self.lastPressed = self.current_millis()
        self.single = single
        GPIO.setup(self.pin, GPIO.IN)

    def current_millis(self):
        return int(round(time.time() * 1000))

    def read(self):
        button = GPIO.input(self.pin)
        now = self.current_millis()
        if self.single:
            if button == False and self.oldButton:
                self.callback()
            self.oldButton = button
        else:
            if button == False and (now - self.lastPressed > 150):
                self.callback()
                self.lastPressed = now

class RotaryEnc:
    ''' RotaryEncoder with integrated switch

    Utilizies the Button-Class for the integrated switch
    Needs to know both GPIO-pins for the rotaryEncoder,
    the GPIO-pin for the swich and callbacks for both the
    encoder and the switch.

    Note: The integrated switch is set to trigger just once it's
    pressed. This is due to the rotaryEncoders I use (KY-040)
    will multi-trigger even with debouncing.
    '''
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

