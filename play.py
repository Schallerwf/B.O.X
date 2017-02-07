from subprocess import call
import sys

call(['aplay', sys.argv[1]])
