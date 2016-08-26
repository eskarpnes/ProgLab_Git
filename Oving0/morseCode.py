from arduinoSerial import Arduino

class MorseController:
	def __init__(self):
		self.ard = Arduino()
		print('Initialized new Morse controller')
		self._decoded = ''
		self.word = ''
		self.symbol = ''
		
		self.morse_codes = {
		#http://stackoverflow.com/questions/32094525/morse-code-to-english-python3
			'A': '01',     'B': '1000',   'C': '1010', 
			'D': '100',    'E': '0',      'F': '0010',
			'G': '110',    'H': '0000',   'I': '00',
			'J': '0111',   'K': '101',    'L': '0100',
			'M': '11',     'N': '10',     'O': '111',
			'P': '0110',   'Q': '1101',   'R': '010',
			'S': '000',    'T': '1',      'U': '001',
			'V': '0001',   'W': '011',    'X': '1001',
			'Y': '1011',   'Z': '1100',

			'0': '11111',  '1': '01111',  '2': '00111',
			'3': '00011',  '4': '00001',  '5': '00000',
			'6': '10000',  '7': '11000',  '8': '11100',
			'9': '11110'}
		self.rev_morse = {value:key for key,value in self.morse_codes.items()}

		# all available functions to handle signals.
		# dicts don't support parametres, hence add_1 and add_0
		self.events = {
			'4': self.reset,
			'3': self.end_word,
			'2': self.continue_word,
			'1': self.add_1,
			'0': self.add_0
		}
		print(self.parse_morse("0000 0 00"))
	
	def parse_morse(self, s):
		s = self.validate_morse(s) # remove obvious invalid codes, length>5
		try:
			# gathers all the matches in the reverse morse list
			return ''.join(self.rev_morse.get(x) for x in s.split())
		except TypeError:
			# this error should never occur due to the validation, but security(!)
			print 'Invalid morse'
	
	def validate_morse(self, s):
		# only keep valid codes of length<5 and valid morse codes
		return ' '.join([x for x in s.split() if len(x)<5 and x in self.morse_codes.values()])
		
	def process_signal(self, e):
		if len(e)==1: # simple security check, even if the arduino is only allowed to send one at a time
			print '#', e
			self.events[e]()
			
	def read_one_signal(self):
		self.process_signal(self.ard.get_morse())
		
	# EVENTS BELOW
	def reset(self):
		print '>> RESET <<'
		self._decoded = ''
		self.word = ''
		self.symbol = ''
	
	def end_word(self):
		self._decoded += self.continue_word()
		print 'Ending word. \n', self._decoded
		self.word = ''
	
	def continue_word(self):
		self.word += self.symbol+' '
		self.symbol = ''
		parsed = self.parse_morse(self.word)+' '
		print self.word, ':', parsed
		return parsed
	
	def add_1(self):
		self.symbol+='1'
		
	def add_0(self):
		self.symbol+='0'
	# END EVENTS
	
	def on_close(self):
		self.ard.close()