import string
from collections import OrderedDict
from random import randint
from crypto_utils import modular_inverse as modInv
class Cipher:
	def __init__(self):
		self.LOW = 65 #32
		self.HIGH = 91 #127
		self.M = self.HIGH-self.LOW #95 or 26 for the normal alphabet
		self.encoded = ''
		self.decoded = ''

	def verify(self, str):
		str = str.upper()
		print ('Verifying '+str)
		return self.decode(self.encode(str))==str
		
	def generate_keys(self):
		# generate keys to be passed to the sender and receiver
		return randint(0,self.M) #-1 to prevent full circle
		
class Caesar(Cipher):
	def __init__(self): # default key: 0
		super().__init__()
		
	def encode(self, str, key):
		print ('Encoding ('+str+')...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,'=',n,'-->',(self.LOW + (n - self.LOW + key)%self.M),chr (self.LOW + (n - self.LOW + key)%self.M))
			self.encoded += chr (self.LOW + (n - self.LOW + key)%self.M)
		print (self.encoded)
		return self.encoded
		
	def decode(self, str, key):
		print ('Decoding '+str+'...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,'=',n,'-->',(self.LOW+(n - self.LOW - key)%self.M),chr (self.LOW + (n - self.LOW - key)%self.M))
			self.decoded += chr (self.LOW + (n - self.LOW - key)%self.M)
		print (self.decoded)

class Mult(Cipher):
	def __init__(self):
		super().__init__()
		
	def encode(self, str, key):
		print ('Encoding ('+str+')...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,n,'-->',(self.LOW + ((n - self.LOW) * key) % self.M),chr (self.LOW + ((n - self.LOW) * key) % self.M))
			self.encoded += chr (self.LOW + ((n - self.LOW) * key) % self.M)
		print (self.encoded)
		return self.encoded
		
	def decode(self, str, key):
		print ('Decoding '+str+'...',end='')
		print()
		x = modInv(key, self.M)
		print ('find solving key...',x)
		for c in str:
			n = ord(c)
			solved = self.LOW+ x*(n-self.LOW) % self.M
			print (c,n,'->',chr(solved), solved)
			self.decoded += chr(solved)
		print (self.decoded)		
			
	
class Affine(Cipher):
	def __init__(self, key=2):
		super().__init__()
		self.key = key
		
		self.first_step = Mult()
		self.second_step = Caesar()
		
		self.encoded = None
		self.decoded = None
				
	def update_key(self, key):
		print ('Updating keys for both mult and caesar')
		self.first_step.update_key(key)
		self.second_step.update_key(key)
		
	def encode(self, str):
		print ('Encoding mult...')
		self.encoded = self.first_step.encode(str)
		print (self.encoded)
		print ('Encoding caesar...')
		self.encoded = self.second_step.encode(self.encoded)
		print ('Done')
		print (self.encoded)
		return self.encoded
		
	def decode(self, str):
		print ('Decoding caesar...')
		self.decoded = self.second_step.decode(str)
		print (self.decoded)
		print ('Decoding mult..')
		self.decoded = self.first_step.decode(self.decoded)
		print ('..Done!')
		print (self.decoded)
		return self.decoded
		
		
class RSA(Cipher):
	def __init__(self, key=2):
		super().__init__()