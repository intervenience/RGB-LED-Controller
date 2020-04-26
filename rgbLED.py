
import socket
import math
import threading
import time
import board
import neopixel
#from sys import Exit
from random import randint
from enum import Enum

class ActiveDisplay (Enum):
	none = 0
	init = 1
	rainbow = 2
	rgb = 3
	wave = 4
	pulse = 5
	xmas = 6
	random = 7
	waveflash = 8

refresh = False
activeLoop = ActiveDisplay.init
#Global RGB values
glRed = 0
glGr = 0
glBl = 0

LIGHTS = 45
pixels = neopixel.NeoPixel(board.D18, LIGHTS, auto_write=False)

HOST = '127.0.0.1'
PORT = 7777

def connections ():
	with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind ((HOST, POR))
		s.listen ()
		conn, addr = s.accept ()
		with conn:
			print ("Connection from ", addr)
			while True:
				data = conn.recv (1024)
				if not data:
					break
				conn.sendall (data)


def parseInput ():
	print ("Initialising...")
	t = threading.Thread (target = initialise)
	t.start()
	line = input ("Input theme: ")
	
	while line != "":
		global activeLoop, glRed, glGr, glBl
		lineArgs = line.split()
		if lineArgs[0] == "rainbow":
			if len (lineArgs) > 1:
				delay = float (lineArgs[1])
			else:
				delay = 0.25
			if activeLoop == ActiveDisplay.rainbow:
				activeLoop = ActiveDisplay.none
			else:
				activeLoop = ActiveDisplay.rainbow
				t.join ()
				t = threading.Thread (target = rainbow, args=[delay])
				t.start ()
		elif lineArgs[0] == "rgb":
			if len (lineArgs) == 4:
				glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
				activeLoop = ActiveDisplay.none
				t.join ()
				pixels.fill ((int (glRed), int(glGr), int(glBl)))
				pixels.show()
			else:
				if activeLoop != ActiveDisplay.init:
					activeLoop = ActiveDisplay.init
					t.join ()
					t = threading.Thread (target = initialise)
					t.start ()
		elif lineArgs[0] == "wave":
			if len (lineArgs) == 5:
				glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
				if activeLoop != ActiveDisplay.wave:
					activeLoop = ActiveDisplay.wave
					t.join ()
					t = threading.Thread (target = wave, args=[lineArgs[4]])
					t.start ()
			else:
				if activeLoop != ActiveDisplay.wave:
					activeLoop = ActiveDisplay.wave
					t.join ()
					t = threading.Thread (target = wave, args=[lineArgs[1]])
					t.start ()
		elif lineArgs[0] == "pulse":
			glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
			if activeLoop != ActiveDisplay.pulse:
				activeLoop = ActiveDisplay.pulse
				t.join()
				t = threading.Thread (target = pulse, args=[float (lineArgs[4])])
				t.start ()
		elif lineArgs[0] == "reset":
			if activeLoop != ActiveDisplay.init:
				activeLoop = ActiveDisplay.init
				t.join ()
				t = threading.Thread (target = initialise)
				t.start ()
		elif lineArgs[0] == "xmas":
			if activeLoop != ActiveDisplay.xmas:
				activeLoop = ActiveDisplay.xmas
				t.join ()
				t = threading.Thread (target = xmas, args=[float (lineArgs[1])])
				t.start ()
		elif lineArgs[0] == "random":
			if activeLoop != ActiveDisplay.random:
				activeLoop = ActiveDisplay.random
				t.join ()
				t = threading.Thread (target = random, args=[lineArgs[1]])
				t.start ()
		elif lineArgs[0] == "waveflash":
			glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
			if activeLoop != ActiveDisplay.waveflash:
				activeLoop = ActiveDisplay.waveflash
				t.join ()
				t = threading.Thread (target = waveAndFlash, args=[float (lineArgs [4])])
				t.start()
		elif lineArgs[0] == "colours":
			glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
		line = input ("Input theme: ")


def initialise ():
	while activeLoop == ActiveDisplay.init:
		for i in range (3):
			if i == 0:
				pixels.fill ((0,255,0))
			elif i == 1:
				pixels.fill ((255,0,0))
			elif i == 2:
				pixels.fill ((200,0,255))
			pixels.show()
			time.sleep (1)
			if activeLoop != ActiveDisplay.init:
				return
	
		
def waveAndFlash (delay):
	global activeLoop, glRed, glGr, glBl
	reds = []
	greens = []
	blues = []
	for i in range (10):
		reds.append (int (glRed * i/10))
		greens.append (int (glGr * i/10))
		blues.append (int (glBl * i/10))
	for i in range (10, LIGHTS - 10):
		reds.append (0)
		greens.append (0)
		blues.append (0)
	print (reds)
	print (greens)
	print (blues)
	#for i in range (LIGHTS + 10):
		


def rainbow (frequency):
	delay = (1.0/frequency)/LIGHTS
	
	red = 255
	green = 0
	blue = 0
	reds = []
	greens = []
	blues = []
	for i in range (LIGHTS):
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
		if outer == (LIGHTS - 1):
			outer = 0
		for i in range (LIGHTS):
			j = i + 1 + outer
			if j < LIGHTS:
				pixels[i] = (reds[j], greens[j], blues[j])
			else:
				k = j - LIGHTS
				pixels[i] = (reds[k], greens[k], blues[k])
		outer += 1
		pixels.show()
		time.sleep (delay)

		
def wave (delay):
	print ("wave")
	#reds = []
	#for i in range glRed
	#while activeLoop == ActiveDisplay.wave:
		
	#mod = 0
	#while activeLoop == ActiveDisplay.wave:
	#	while mod < 6:
	#		for i in range (5):
	#			for j in range (6):
	#				red = int (glRed * ((14 * ((j + mod)**2)) - 100 * (j+mod) + 190))
	#				green = int (glGr * ((14 * ((j + mod)**2)) - 100 * (j + mod) + 190))
	#				blue = int (glBl * ((14 * ((j + mod)**2)) - 100 * (j + mod) + 190))
	#				pixels[i*6+j] = (glRed,glGr,glBl)
	#		time.sleep (float (delay))
	#		mod += 1
	#	mod = 0
		
#Where frequency is times per second
def pulse (frequency):
	length = 1.0/frequency
	#how many changes are made per length to smooth the colour transition
	smoothness = 20
	delay = (length / smoothness)/2.0
	incR = int (glRed / smoothness)
	incG = int (glGr / smoothness)
	incB = int (glBl / smoothness)
	
	#clamp values so we don't accidentally exceed 255 when we increment
	if ((incR * smoothness) > 255):
		incR -= 1
	if ((incG * smoothness) > 255):
		incG -= 1
	if ((incB * smoothness) > 255):
		incB -= 1
	
	while activeLoop == ActiveDisplay.pulse:
		for i in range (1, smoothness, 1):
			pixels.fill ((incR * i, incG * i, incB * i))
			pixels.show ()
			time.sleep (delay)
		for i in range (smoothness, 1, -1):
			pixels.fill ((incR * i, incG * i, incB * i))
			pixels.show ()
			time.sleep (delay)
		

def xmas (frequency):
	delay = 1.0/frequency
	
	pixels.fill ((0,0,0))
	while activeLoop == ActiveDisplay.xmas:
		for i in range (0, LIGHTS, 2):
			pixels[i] = (200, 0,0)
		pixels.show()
		time.sleep (delay)
		pixels.fill ((0,0,0))
		for j in range (1, LIGHTS, 2):
			pixels[j] = (0, 200, 0)
		pixels.show()
		time.sleep (delay)
		pixels.fill ((0,0,0))
		

def random (frequency):
	delay = 1.0/frequency
	
	while activeLoop == ActiveDisplay.random:
		for i in range (LIGHTS):
			pixels[i] = ((randint (0, 255)), (randint (0, 255)), (randint (0, 255)))
		pixels.show()
		time.sleep (float (delay))

		
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
