import string
from collections import OrderedDict
from random import randint
from crypto_utils import modular_inverse as modInv
class Cipher:
	def __init__(self):
		self.LOW = 65 #32
		self.HIGH = 91 #127
		self.A = list((chr(i))for i in range(self.LOW, self.HIGH))
		# self.A = list((chr(i),i-32)for i in range(32, 127))
		# self.A = list((chr(i),i-65) for i in range(65,91))
		self.M = len(self.A) #95
		self.ciphered = '' #used to store the ciphered alphabet

	def encode(self, str, key):
		# str = str.upper()
		print ('Encoding ('+str+')...',end='')
		encoded = ''.join(self.ciphered[self.A.index(c)] for c in str)
		
		# for c in str:
			# n = ord(c)
			# self.ciphered += chr((n+key)%self.M)
		# print ()
		# print (self.ciphered)
		
		print(encoded)
		return encoded
		
	def decode(self, str, key):
		#str = str.upper()
		print ('Decoding...',end='')
		decoded = ''.join(self.A[self.ciphered.index(c)] for c in str)
		# print()
		# for c in str:
			# n = ord(c)
			# print ('Mod value:',(n-key)%self.M)
			# print (c,'to',n,'-->',chr(n-key))
		
		print(decoded)
		return decoded

	def verify(self, str):
		str = str.upper()
		print ('Verifying '+str)
		return self.decode(self.encode(str))==str
		
	def generate_keys(self):
		# generate keys to be passed to the sender and receiver
		return randint(self.M-1) #-1 to prevent full circle
		
		
class Caesar(Cipher):
	def __init__(self): # default key: 0
		super().__init__()
		
	def update_key(self, key):
		self.ciphered = list(
				(chr((key+(i-self.LOW))%self.M+self.LOW)
				for i in range(self.LOW,self.HIGH)))
		print (self.A)
		print (self.ciphered)
		# return self.ciphered

class Mult(Cipher):
	def __init__(self):
		super().__init__()
	
	def update_key(self, key):
		# self.ciphered = list(
				# chr(((key*(i-self.LOW)))%self.M+self.LOW)
				# for i in range(self.LOW,self.HIGH))
		self.ciphered = list(
				chr(((modInv(key*(i-self.LOW),self.M)))%self.M+self.LOW)
				for i in range(self.LOW,self.HIGH))				
		print (self.A)
		print (self.ciphered)
		# for i in range(self.LOW, self.HIGH):
		# return self.ciphered
		
			
	
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