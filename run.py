import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Node(object):
	def __init__(self, audio):
		self.no = None
		self.yes = None
		self.audio = audio
		self.isEnd = False

def waitForInput():
	timeout = time.time() + 30 # 30 seconds from now
	while True:
		input_state = GPIO.input(18)
		if input_state == False:
			return 'Yes'
		input_state = GPIO.input(12)
		if input_state == False:
			return 'No'
		if time.time() > timeout:
			return 'Timeout'

END = ['audio/goodbye.wav']

def buildTree():
	start =  Node('audio/start')
	start.yes = Node('y')
	start.no = Node('n')
	return start

def play(audio):
	print 'Playing ' + audio

def run():
	start = buildTree()
	currentNode = start
	while True:	
		input = waitForInput()
		time.sleep(0.2)
		print 'Input = ' + input
		print 'Start: ' + str(currentNode is start)
		if input != 'Timeout' and currentNode is start:
			print 'Starting'
			play(currentNode.audio)
			if input == 'Yes':
				currentNode = start.yes
			else:
				currentNode = start.no 
		elif input == 'Timeout' and not currentNode is start:
			print 'Timing Out'
			play(random.choice(END))
			currentNode = start
		elif input != 'Timeout':
			print 'Continuing'
			play(currentNode.audio)
			
			if currentNode.isEnd:
				currentNode = start
			
			if input == 'Yes':
				currentNode = currentNode.yes
			else:
				currentNode = currentNode.no

run()

