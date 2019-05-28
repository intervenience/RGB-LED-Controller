import time
import board
import neopixel
from enum import Enum

pixels = neopixel.NeoPixel(board.D18, 90)

print ("Initialising...")
while True:
	for i in range (90):
		pixels[i] = (0,0,255)
		time.sleep (0.25)
	pixels.fill ((0,0,0))
	time.sleep (1)