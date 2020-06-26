
import socket
import math
import threading
import time
import binascii
import board
import neopixel

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

#Global light update frequency (1 by default)
frequency = 1

#LED and board setup
LIGHTS = 45
pixels = neopixel.NeoPixel(board.D18, LIGHTS, auto_write=False)

# Socket port
PORT = 20001

#Lighting options for socket data input
lightingOptions = [ "rainbow", "rgb", "pulse", "xmas", "random"]

def socketInput ():
	_socket = socket.socket ()
	_socket.bind (('', PORT))
	_socket.listen (5)
	while True:
		conn, addr = _socket.accept ()
		print ("Got connection from", addr)
		line = (conn.recv(1024).decode())
		received = line.split()[0]
		print (received)
		if (received == "ping"):
			conn.send("pong".encode())
		elif (received == "frequency"):
			changeFrequency (line.split ()[1])
		elif (received in lightingOptions):
			parseInputs (line)
		conn.close ()


def changeFrequency (n):
	global frequency
	try:
		frequency = float (n)
	except:
		print ("invalid frequency input")
		frequency = 1

def readUserInput ():
	print ("Initialising...")
	line = input ("Input theme: ")
	
	while line != "":
		parseInputs (line)
		line = input ("Input theme: ")


def parseInputs (inputLine):
	global activeLoop, glRed, glGr, glBl, t
	lineArgs = inputLine.split()
	length = len (lineArgs)
	effect = lineArgs[0]

	if effect == "rainbow":
		if length > 1:
			changeFrequency (lineArgs[1])
		else:
			changeFrequency (1)
		if activeLoop == ActiveDisplay.rainbow:
			activeLoop = ActiveDisplay.none
		else:
			activeLoop = ActiveDisplay.rainbow
			t.join ()
			t = threading.Thread (target = rainbow)
			t.start ()
	elif effect == "rgb":
		if length == 4:
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
	elif effect == "wave":
		if length == 5:
			glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
			changeFrequency (lineArgs [4])
			if activeLoop != ActiveDisplay.wave:
				activeLoop = ActiveDisplay.wave
				t.join ()
				t = threading.Thread (target = wave)
				t.start ()
		else:
			if activeLoop != ActiveDisplay.wave:
				activeLoop = ActiveDisplay.wave
				t.join ()
				changeFrequency (lineArgs[1])
				t = threading.Thread (target = wave)
				t.start ()
	elif effect == "pulse":
		glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
		if activeLoop != ActiveDisplay.pulse:
			activeLoop = ActiveDisplay.pulse
			t.join()
			changeFrequency (lineArgs[4])
			t = threading.Thread (target = pulse)
			t.start ()
	elif effect == "reset":
		if activeLoop != ActiveDisplay.init:
			activeLoop = ActiveDisplay.init
			t.join ()
			t = threading.Thread (target = initialise)
			t.start ()
	elif effect == "xmas":
		if activeLoop != ActiveDisplay.xmas:
			activeLoop = ActiveDisplay.xmas
			t.join ()
			changeFrequency (lineArgs[1])
			t = threading.Thread (target = xmas)
			t.start ()
	elif effect == "random":
		if activeLoop != ActiveDisplay.random:
			activeLoop = ActiveDisplay.random
			t.join ()
			changeFrequency (lineArgs[1])
			t = threading.Thread (target = random)
			t.start ()
	elif effect == "waveflash":
		glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])
		if activeLoop != ActiveDisplay.waveflash:
			activeLoop = ActiveDisplay.waveflash
			t.join ()
			changeFrequency (lineArgs[4])
			t = threading.Thread (target = waveAndFlash)
			t.start()
	elif effect == "colours":
		glRed, glGr, glBl = int (lineArgs[1]), int (lineArgs[2]), int (lineArgs[3])



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


def waveAndFlash ():
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
		


def rainbow ():
	global frequency
	
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
		delay = (1.0/frequency)/LIGHTS
		time.sleep (delay)

		
def wave ():
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
		
		
def pulse ():
	global frequency
	#how many changes are made per length to smooth the colour transition
	smoothness = 20
	
	while activeLoop == ActiveDisplay.pulse:
		for i in range (1, smoothness, 1):
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

			pixels.fill ((incR * i, incG * i, incB * i))
			pixels.show ()
			length = 1.0/frequency
			delay = (length / smoothness)/2.0
			time.sleep (delay)
		for i in range (smoothness, 1, -1):
			pixels.fill ((incR * i, incG * i, incB * i))
			pixels.show ()
			length = 1.0/frequency
			delay = (length / smoothness)/2.0
			time.sleep (delay)
		

def xmas ():
	global frequency
	
	pixels.fill ((0,0,0))
	while activeLoop == ActiveDisplay.xmas:
		for i in range (0, LIGHTS, 2):
			pixels[i] = (200, 0,0)
		pixels.show()
		delay = 1.0/frequency
		time.sleep (delay)
		pixels.fill ((0,0,0))
		for j in range (1, LIGHTS, 2):
			pixels[j] = (0, 200, 0)
		pixels.show()
		delay = 1.0/frequency
		time.sleep (delay)
		pixels.fill ((0,0,0))
		

def random ():
	global frequency

	while activeLoop == ActiveDisplay.random:
		delay = 1.0/float (frequency)
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
	t = threading.Thread (target = initialise)
	t.start()
	ct = threading.Thread (target = socketInput)
	ct.start()
	readUserInput()
