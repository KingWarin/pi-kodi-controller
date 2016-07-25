from xbmcclient import *
from socket import *
from controls import RotaryEnc, Button
import RPi.GPIO as GPIO
import time


class CFunctions:
    def __init__(self, direction, sock, addr):
        self.direction = direction
        self.sock = sock
        self.addr = addr
        self.key_map = "KB"

    def _sender(self, button):
        packet = PacketBUTTON(map_name="KB", button_name=button, repeat=0)
        packet.send(self.sock, self.addr)

    def volumeControl(self, direction):
        if direction == self.direction:
            # clockwise -> volume Up
            print "Volume Up"
            self._sender("plus")
        else:
            # counterclockwise -> volume Down
            print "Volume Down"
            self._sender("minus")

    def menuControl(self, direction):
        if direction == self.direction:
            # clockwise -> down
            print "Down"
            self._sender("down")
        else:
            # counterclockwise -> up
            self._sender("up")

    def buttonControl(self):
        print "Switch Volume Direction"
        self.direction = False if self.direction else True

    def menuSelect(self):
        print "Select"
        self._sender("enter")

    def openMusic(self):
        print "Open Music"
        self._sender("yellow")


def main():
    host = "localhost"
    port = 9777
    addr = (host, port)
    sock = socket(AF_INET,SOCK_DGRAM)

    cf = CFunctions(True, sock, addr)

    # Setup a rotaryEncoder with switch for volume control
    R1 = RotaryEnc(
            PinA=10,
            PinB=8,
            button=3,
            rotaryCallback=cf.volumeControl,
            buttonCallback=cf.buttonControl
         )

    R2 = RotaryEnc(
            PinA=13,
            PinB=11,
            button=15,
            rotaryCallback=cf.menuControl,
            buttonCallback=cf.menuSelect
         )


    def fake():
        # just a test for a second button without creating a new function
        return cf.volumeControl(True)

    B1 = Button(pin=7,callback=fake,single=False)

    # First packet must be HELO and can contain an icon
    packet = PacketHELO("BreadBoard Control", ICON_NONE)
    packet.send(sock, addr)

    cf.openMusic()

    while True:
        #CODE TO CATCH BUTTON PRESS HERE
        R1.read()
        R1.read_button()
        B1.read()
        R2.read()
        R2.read_button()

if __name__ == "__main__":
    main()
