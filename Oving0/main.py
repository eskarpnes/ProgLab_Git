from morseCode import MorseController
import time
import sys

def main():
	morse = None
	try:
		morse = MorseController()
		while True:
			morse.read_one_signal()
			time.sleep(1/10) #10 hz
	except KeyboardInterrupt:
		sys.tracebacklimit=0
		print 'Interrupted by user! Quitting...'
		if morse!=None:
			morse.on_close()

if __name__ == '__main__':
	main()