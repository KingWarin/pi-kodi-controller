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

    def volumeControl(self, direction):
        if direction == self.direction:
            # clockwise -> volume Up
            print "Volume Up"
            packet = PacketBUTTON(map_name="KB", button_name="plus", repeat=0)
            packet.send(self.sock, self.addr)
        else:
            # counterclockwise -> volume Down
            print "Volume Down"
            packet = PacketBUTTON(map_name="KB", button_name="minus", repeat=0)
            packet.send(self.sock, self.addr)

    def buttonControl(self):
        print "Switch Volume Direction"
        self.direction = False if self.direction else True 


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

    def fake():
        # just a test for a second button without creating a new function
        return cf.volumeControl(True)

    B1 = Button(pin=7,callback=fake,single=False)

    # First packet must be HELO and can contain an icon
    packet = PacketHELO("BreadBoard Control", ICON_NONE)
    packet.send(sock, addr)


    while True:
        #CODE TO CATCH BUTTON PRESS HERE
        R1.read()
        R1.read_button()
        B1.read()

if __name__ == "__main__":
    main()
