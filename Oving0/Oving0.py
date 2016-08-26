from morseCode import MorseController
import time

def main():
	morse = MorseController()
	while (True):
		morse.read_one_signal()
		time.sleep(1/10) #10 hz
	morse.on_close()
main()