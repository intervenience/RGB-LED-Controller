import time
import board
import neopixel
from enum import Enum

pixels = neopixel.NeoPixel(board.D18, 45)

print ("Initialising...")
pixels.fill ((255,0,0))
pixels.show()
time.sleep (1)
while True:
	pixels.fill ((0,255,0))
	time.sleep (1)
	pixels.fill ((0,0,255))
	time.sleep (1)
	pixels.fill ((150,0,150))
	time.sleep (1)
	pixels.fill ((255,0,0))
	#for i in range (30):
	#	pixels[i] = (0,0,255)
	#	time.sleep (0.25)
	#pixels.fill ((0,0,0))
	time.sleep (1)