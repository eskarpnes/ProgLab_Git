from cipher import Caesar, Mult, Affine, RSA

class Person:
	def __init__(self, cipher_num):
		self.ciphers = {
			1:Caesar, 2:Mult, 3:Affine, 4:RSA
		}
		self.cipher_num = cipher_num
		self.cipher = self.ciphers[self.cipher_num]()
		self.key = 0 #default
		# self.set_key (3) #default
		self.txt = None
		
	def set_cipher(self, cipher):
		if cipher>0 and cipher<5:
			self.cipher = self.ciphers[cipher]()
			print ('Set the cipher to',self.ciphers[cipher].__name__)
		else:
			raise KeyError('Invalid cipher value!')
			
	def get_cipher_type(self):
		return self.cipher_num
		
	def set_key(self, key, from_class = 'Unknown'):
		if self.key != key:
			self.key = key
		
	def get_key(self):
		return self.key
		
	def operate_cipher(self, str):
		print ('-> Operating cipher in person class!')

class Sender(Person):
	def __init__(self, cipher, key):
		super().__init__(cipher)
		print ('Creating a sender with crypto level:',self.cipher.__class__.__name__)
		super().set_key(self.cipher.generate_keys() if key is None else key)
	
	def operate_cipher(self, str):
		print ('Sender is operating cipher with',self.cipher.__class__.__name__, 'with key',self.get_key())
		self.txt = self.cipher.encode(str, self.key)
		
class Receiver(Person):
	def __init__(self, sender):
		print ('Creating a receiver')
		super().__init__(sender.get_cipher_type())
		self.sender = sender
		
	def operate_cipher(self):
		super().set_key(self.sender.get_key())
		print ('Receiver is trying to crack',self.sender.txt, 'with key',self.key)
		s = self.cipher.decode(self.sender.txt, self.key)


class Hacker(Person):
	def __init__(self):
		super().__init__()
		print ('Creating a hacker!')
		
	def operate_cipher(self):
		print ('Hacker is operating cipher')
		super().operate_cipher()

class Communicate:
	def __init__(self, cipher_type, key=None):
		self.s = Sender(cipher_type, key)
		self.r = Receiver(self.s)
		
	def send(self, msg):
		self.s.operate_cipher(msg)
		self.r.operate_cipher()