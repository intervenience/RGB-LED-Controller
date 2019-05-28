
import math
import threading
import time
import board
import neopixel
from random import randint
from enum import Enum

pixels = neopixel.NeoPixel(board.D18, 90)

class ActiveDisplay (Enum):
	none = 0
	init = 1
	rainbow = 2
	rgb = 3
	wave = 4
	pulse = 5
	xmas = 6
	random = 7

activeLoop = ActiveDisplay.init

def parseInput ():
	print ("Initialising...")
	t = threading.Thread (target = initialise)
	t.start()
	line = input ("Input theme: ")
	
	while line != "":
		lineArgs = line.split()
		print (lineArgs)
		if lineArgs[0] == "rainbow":
			if len (lineArgs) > 1:
				delay = float (lineArgs[1])
			else:
				delay = 0.25
			global activeLoop 
			activeLoop = ActiveDisplay.rainbow
			t.join ()
			t = threading.Thread (target = rainbow)
			t.start ()
		elif lineArgs[0] == "rgb":
			print ("Got rgb")
			if len (lineArgs) == 4:
				print ("args == 4")
				global activeLoop 
				activeLoop = ActiveDisplay.rgb
				t.join ()
				print ("got past join()")
				t = threading.Thread (target = rgb, args=[lineArgs[1], lineArgs[2], lineArgs[3]])
				t.start()
			elif len (lineArgs) == 2:
				print ("args == 2")
				global activeLoop 
				activeLoop = ActiveDisplay.none
				print (activeLoop)
				t.join ()
				print ("got here")
				colourByName (lineArgs[1])
			else:
				print ("doing init loop")
				global activeLoop 
				activeLoop = ActiveDisplay.init
				t.join ()
				t = threading.Thread (target = initialise)
				t.start ()
		elif lineArgs[0] == "wave":
			print ("Got wave")
			if len (lineArgs) == 5:
				global activeLoop 
				activeLoop = ActiveDisplay.wave
				t.join ()
				t = threading.Thread (target = wave, args=[lineArgs[1], lineArgs[2], lineArgs[3], lineArgs[4]])
				t.start ()
		elif lineArgs[0] == "pulse":
			global activeLoop
			activeLoop = ActiveDisplay.pulse
			t.join()
			t = threading.Thread (target = pulse, args=[int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3]), float (lineArgs[4])])
			t.start ()
		elif lineArgs[0] == "reset":
			global activeLoop
			activeLoop = ActiveDisplay.init
			t.join ()
			t = threading.Thread (target = initialise)
			t.start ()
		elif lineArgs[0] == "xmas":
			global activeLoop
			activeLoop = ActiveDisplay.xmas
			t.join ()
			t = threading.Thread (target = xmas, args=[float (lineArgs[1])])
			t.start ()
		elif lineArgs[0] == "random":
			global activeLoop
			activeLoop = ActiveDisplay.random
			t.join ()
			t = threading.Thread (target = random, args=[lineArgs[1]])
			t.start ()
		line = input ("Input theme: ")


def initialise ():
	while activeLoop == ActiveDisplay.init:
		#print (activeLoop)
		for i in range (3):
			if i == 0:
				pixels.fill ((0,255,0))
			elif i == 1:
				pixels.fill ((255,0,0))
			elif i == 2:
				pixels.fill ((200,0,255))
			time.sleep (1)
			


def rainbow ():
	red = 255
	green = 0
	blue = 0
	reds = []
	greens = []
	blues = []
	for i in range (90):
		pixels[i] = (red, green, blue)
		if green < 255 and red == 255:
			green += 17
		if green == 255 and red <= 255:
			red -= 17
		if green == 255 and blue < 255:
			blue += 17
		if green <= 255 and blue == 255:
			green -= 17
		if blue == 255 and red < 255:
			red += 17
		if red == 255 and blue > 0:
			blue -= 17
		reds.append (red)
		greens.append (green)
		blues.append (blue)
	outer = 0
	while activeLoop == ActiveDisplay.rainbow:
		if outer == 89:
			outer = 0
		for i in range (90):
			j = i + 1 + outer
			if j < 90:
				pixels[i] = (reds[j], greens[j], blues[j])
			else:
				k = j - 90
				pixels[i] = (reds[k], greens[k], blues[k])
		outer += 1

def wave (r, g, b, delay):
	mod = 0
	while activeLoop == ActiveDisplay.wave:
		while mod < 6:
			for i in range (5):
				for j in range (6):
					red = int (r * ((14 * ((j + mod)**2)) - 100 * (j+mod) + 190))
					green = int (g * ((14 * ((j + mod)**2)) - 100 * (j + mod) + 190))
					blue = int (b * ((14 * ((j + mod)**2)) - 100 * (j + mod) + 190))
					pixels[i*6+j] = (r,g,b)
			time.sleep (delay)
			mod += 1
		mod = 0
		
def pulse (r, g, b, delay):
	incR = int (0.1 * r)
	incG = int (0.1 * g)
	incB = int (0.1 * b)
	if ((incR * 10) > 255):
		incR -= 1
	if ((incG * 10) > 255):
		incG -= 1
	if ((incB * 10) > 255):
		incB -= 1

	while activeLoop == ActiveDisplay.pulse:
		for i in range (1, 10, 1):
			pixels.fill ((incR * i, incG * i, incB * i))
			time.sleep (delay)
		for i in range (10,1, -1):
			pixels.fill ((incR * i, incG * i, incB * i))
			time.sleep (delay)
		
def xmas (delay):
	pixels.fill ((0,0,0))
	while activeLoop == ActiveDisplay.xmas:
		for i in range (0, 90, 2):
			pixels[i] = (200, 0,0)
		time.sleep (delay)
		pixels.fill ((0,0,0))
		for j in range (1, 90, 2):
			pixels[j] = (0, 200, 0)
		time.sleep (delay)
		pixels.fill ((0,0,0))
		
def random (delay):
	while activeLoop == ActiveDisplay.random:
		for i in range (90):
			pixels[i] = ((randint (0, 255)), (randint (0, 255)), (randint (0, 255)))
		time.sleep (float (delay))
		
def rgb (r, g, b):
	print ("rgb ", r, g, b)
	pixels.fill ((int (r), int(g), int(b)))

def colourByName (colour):
	print (colour)
	if colour == "Red" or colour == "red":
		pixels.fill ((150,0,0))
	elif colour == "Green" or colour == "green":
		pixels.fill ((0,150,0))
	elif colour == "Blue" or colour == "blue":
		pixels.fill ((0,0,150))
	elif colour == "White" or colour == "white":
		pixels.fill ((255,255,255))
	elif colour == "Purple" or colour == "purple":
		pixels.fill ((150,0,150))
	elif colour == "Yellow" or colour == "yellow":
		pixels.fill ((150, 75, 0))
	else:
		print ("Missing colour or couldn't parse input")
		initialise ()

if __name__ == '__main__':
    parseInput()
