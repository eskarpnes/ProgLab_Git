from cipher import Caesar, Mult, Affine, Unbreakable, RSA

class Person:
	def __init__(self, cipher, key=0):
		self.cipher = cipher
		self.key = key
		
	def get_cipher_name(self):
		return self.cipher.__class__.__name__
		
	def set_key(self, key):
		if self.key != key:
			self.key = key
		
	def get_key(self):
		return self.key
		
	def operate_cipher(self, txt):
		print ('-> Operating cipher in person class!')
		

class Sender(Person):
	def __init__(self, cipher, key):
		super().__init__(cipher, key)
		print ('Creating a sender')
	
	def operate_cipher(self, txt):
		print ('Sender is operating',self.get_cipher_name(), 'with key', self.get_key())
		return self.cipher.encode(txt, self.get_key())
		
class Receiver(Person):
	def __init__(self, cipher, key):
		print ('Creating a receiver')
		super().__init__(cipher, key)
		
	def operate_cipher(self, txt):
		print ('Receiver is trying to crack', txt, 'with key', self.get_key())
		return self.cipher.decode(txt, self.get_key())

class Hacker(Person):
	def __init__(self, cipher, text):
		super().__init__(cipher)
		self.available_keys = cipher.available_keys()
		self.text = text
		self.word_list = []
		self.init_words()
		print ('The hacker is looking through his keys to solve the', self.get_cipher_name(),'cipher')
		print ('\nHacking away on', text)
		# print (self.available_keys)
		# self.hack()
					
	def init_words(self):
		with open ('englishwords.txt','r') as words:
			self.word_list = [word.strip() for word in words]
		words.close()

	def hack(self):  # ???
		# print (self.available_keys)
		for key in self.available_keys:
			tmp = self.operate_cipher(key)
			if tmp is not None and tmp.lower() in self.word_list:
				print ('Found a match:', tmp, '...Key used:',key)
				return tmp
	
	def operate_cipher(self, key):
		return self.cipher.decode(self.text, key)

class Communicate:
	def __init__(self, cipher_type):
		self.ciphers = {
			1:Caesar, 2:Mult, 3:Affine, 4:Unbreakable, 5: RSA
		}
		self.cipher = None
		self.is_RSA = (cipher_type == 5)
		if cipher_type > 0 and cipher_type < 6:
			self.cipher = self.ciphers[cipher_type]()
			print ('Set the cipher to',self.cipher.__class__.__name__)
		else:
			print ('Invalid cipher value!')

		if cipher_type == 5:  # RSA
			RSA_keys = self.cipher.generate_keys()
			self.r = Receiver(self.cipher, RSA_keys[1])
			self.s = Sender(self.cipher, RSA_keys[0])
		else:
			key = self.cipher.generate_keys()
			self.s = Sender(self.cipher, key)
			self.r = Receiver(self.cipher, key)
		
	def send(self, msg):
		encrypted = self.s.operate_cipher(msg)
		decrypted = self.r.operate_cipher(encrypted)
		print ('\nVerifying...')
		if self.cipher.verify(msg, decrypted):
			print ('>>> Decoding succeeded! <<<')
		else:
			print ('>>> Decoding failed! <<<')
		print()

	def hack(self, msg):
		encrypted = self.s.operate_cipher(msg)
		print ('\n!!!!!!!! A hacker has interfered!')
		if self.is_RSA:
			print ("... but a hacker ain't no match for RSA")
			return
		hacker = Hacker(self.cipher, encrypted)
		decrypted = hacker.hack()
		if decrypted is not None and self.cipher.verify(msg, decrypted):
			print ('>>> Decoding succeeded! <<<')
		else:
			print ('>>> Decoding failed! <<<')
		print()
