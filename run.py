import sys
from subprocess import call

keyboard = False
if len(sys.argv) > 1 and sys.argv[1] == '-k':
    keyboard = True

if not keyboard:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

import time
import random
import select

class Node(object):
    def __init__(self, ID, yes, no):
        self.ID = ID
        self.no = no
        self.yes = yes

def waitForKeyboardInput():
    i, e, o = select.select([sys.stdin], [], [], 30)
    if i:
        if sys.stdin.readline().strip() == 'y':
            return 'Yes'
        else:
            return 'No'
    else:
        return 'Timeout'        

def waitForInput():
    if keyboard:
        return waitForKeyboardInput()

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

END = ['goodbye']

def buildGraph():
    graph = {}
    graph[-1] = Node(-1, -1, -1)
    graph[1] = Node(1, 3, 2)
    graph[2] = Node(2, 3, 2)
    graph[3] = Node(3, 6, 4)
    graph[4] = Node(4, 5, 7)
    graph[5] = Node(5, 6, 7)
    graph[6] = Node(6, 9, 8)
    graph[7] = Node(7, -1, -1)
    graph[8] = Node(8, 9, 14)
    graph[9] = Node(9, 10, 11)
    graph[10] = Node(10, 12, 13)
    graph[11] = Node(11, 19, 18)
    graph[12] = Node(12, 19, 18)
    graph[13] = Node(13, 19, 18)
    graph[14] = Node(14, 17, 16)
    graph[15] = Node(15, -1, -1)
    graph[16] = Node(16, 9, 15)
    graph[17] = Node(17, -1, -1)
    graph[18] = Node(18, -1, -1)
    graph[19] = Node(19, 20, 21)
    graph[20] = Node(20, 22, 23)
    graph[21] = Node(21, 20, 24)
    graph[22] = Node(22, 26, 25)
    graph[23] = Node(23, -1, -1)
    graph[24] = Node(24, -1, -1)
    graph[25] = Node(25, -1, -1)
    graph[26] = Node(26, 27, 25)
    graph[27] = Node(27, 28, 25)
    graph[28] = Node(28, -1, -1)

    return graph

def play(audioID):
    print 'Playing {0}'.format(audioID)
    f = 'audio/{0}.m4a'.format(audioID)
    if keyboard:
        call(['afplay', f])
    else:        
        call(['aplay', f])

def run():
    graph = buildGraph()
    start = graph[1]
    currentNode = None
    while True:  
        if currentNode != None and currentNode.ID == -1:
            print 'asfd'
            currentNode = None  

        input = waitForInput()
        time.sleep(0.2)

        if input != 'Timeout' and currentNode is None:
            play(start.ID)
            currentNode = start
        elif input == 'Timeout' and not currentNode is None:
            play(random.choice(END))
            currentNode = None
        elif currentNode != None and currentNode.ID == -1:
            currentNode = None
        elif input != 'Timeout':
            if input == 'Yes':
                currentNode = graph[currentNode.yes]
            else:
                currentNode = graph[currentNode.no]

            if currentNode.ID != -1:
                play(currentNode.ID)

            if currentNode.yes == -1:
                currentNode = None
            
run()
