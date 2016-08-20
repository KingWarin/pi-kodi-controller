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

    def playPause(self):
        print "PlayPause"
        self._sender("space")

    def nextTrack(self):
        print "NextTrack"
        self._sender("period")

    def prevTrack(self):
        print "PrevTrack"
        self._sender("comma")

    def levelBack(self):
        print "LevelBack"
        self._sender("backspace")

    def menuSelect(self):
        print "Select"
        self._sender("enter")


def main():
    host = "localhost"
    port = 9777
    addr = (host, port)
    sock = socket(AF_INET,SOCK_DGRAM)

    cf = CFunctions(True, sock, addr)

    # Setup a rotaryEncoder with switch for volume control
    R1 = RotaryEnc(
            PinA=7,
            PinB=3,
            button=11,
            rotaryCallback=cf.volumeControl,
            buttonCallback=cf.buttonControl
         )

    # Setup a rotaryEncoder with switch for menu control
    R2 = RotaryEnc(
            PinA=29,
            PinB=23,
            button=31,
            rotaryCallback=cf.menuControl,
            buttonCallback=cf.menuSelect
         )


    # Setup play/pause button
    B1 = Button(pin=15,callback=cf.playPause)

    # Setup play next button
    B2 = Button(pin=13,callback=cf.nextTrack)

    # Setup play prev button
    B3 = Button(pin=21,callback=cf.prevTrack)

    # Setup one level back button
    B4 = Button(pin=19,callback=cf.levelBack)

    # First packet must be HELO and can contain an icon
    packet = PacketHELO("BreadBoard Control", ICON_NONE)
    packet.send(sock, addr)

    while True:
        #CODE TO CATCH BUTTON PRESS HERE
        R1.read()
        R1.read_button()
        B1.read()
        B2.read()
        B3.read()
        B4.read()
        R2.read()
        R2.read_button()

if __name__ == "__main__":
    main()
