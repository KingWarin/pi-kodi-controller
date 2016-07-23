from xbmcclient import *
from socket import *
from controls import RotaryEnc
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
#    GPIO.setmode(GPIO.BOARD)
#    GPIO.setup(8, GPIO.IN)
#    GPIO.setup(10, GPIO.IN)

#    def volumeControl(direction):
#        if direction == True:
#            # clockwise -> volume Up
#            print "Volume Up"
#            packet = PacketBUTTON(map_name="KB", button_name="plus", repeat=0)
#            packet.send(sock, addr)
#        else:
#            # counterclockwise -> volume Down
#            print "Volume Down"
#            packet = PacketBUTTON(map_name="KB", button_name="minus", repeat=0)
#            packet.send(sock, addr)
#
#    def buttonControl():
#        print "Switch Volume Direction"

    R1 = RotaryEnc(
        PinA=7,
        PinB=5,
        button=3,
        rotaryCallback=cf.volumeControl,
        buttonCallback=cf.buttonControl
    )

#    sock = socket(AF_INET,SOCK_DGRAM)

    # First packet must be HELO and can contain an icon
    packet = PacketHELO("BreadBoard Control", ICON_NONE)
    packet.send(sock, addr)


    while True:
        #CODE TO CATCH BUTTON PRESS HERE
#        volup = GPIO.input(8)
#        voldown = GPIO.input(10)
#        if volup == False:
#            print "Volume Up"
#            packet = PacketBUTTON(map_name="KB", button_name="plus", repeat=0)
#            packet.send(sock, addr)
#        elif voldown == False:
#            print "Volume Down"
#            packet = PacketBUTTON(map_name="KB", button_name="minus", repeat=0)
#            packet.send(sock, addr)
        R1.read()
        R1.read_button()
#        time.sleep(0.1)

if __name__ == "__main__":
    main()
