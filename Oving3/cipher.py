import string
from collections import OrderedDict
import random
from crypto_utils import modular_inverse as modInv, rabin_miller_is_prime as randPrime,generate_random_prime as randPrime
class Cipher:
	def __init__(self):
		self.LOW = 65 #32
		self.HIGH = 91 #127
		self.M = self.HIGH-self.LOW #95 or 26 for the normal alphabet
		# self.A = list((chr(i),i-32)for i in range(32, 127))
		# print (self.A)
	
	def encode(self):
		pass
		
	def decode(self):
		pass
		
	def verify(self, str, key): #from scramble to txt
		# str = str.upper()
		print ('Verifying '+str)
		return self.decode(self.encode(str, key), key)==str
		
	def generate_keys(self):
		# generate keys to be passed to the sender and receiver
		return random.randint(1,self.M-1) #-1 to prevent full circle
		
class Caesar(Cipher):
	def __init__(self): # default key: 0
		super().__init__()
		
	def encode(self, str, key):
		encoded = ''
		print ('Encoding ('+str+')...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,n,'->',(self.LOW + (n - self.LOW + key)%self.M),chr (self.LOW + (n - self.LOW + key)%self.M))
			encoded += chr (self.LOW + (n - self.LOW + key)%self.M)
		print (encoded)
		return encoded
		
	def decode(self, str, key):
		decoded = ''
		print ('Decoding '+str+'...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,n,'->',(self.LOW+(n - self.LOW - key)%self.M),chr (self.LOW + (n - self.LOW - key)%self.M))
			decoded += chr (self.LOW + (n - self.LOW - key)%self.M)
		print (decoded)
		return decoded


class Mult(Cipher):
	def __init__(self):
		super().__init__()
		self.primes = [i for i in range(0,self.M) if isPrime(i) and self.M % i != 0]		
		
	def generate_keys(self):
		n = random.choice(self.primes)
		while n%self.M==0:
			n = random.choice(self.primes)
		return n
		
	def encode(self, str, key):
		encoded = ''
		print ('Encoding ('+str+')...',end='')
		print()
		for c in str:
			n = ord(c)
			print (c,n,'-->',(self.LOW + ((n - self.LOW) * key) % self.M),chr (self.LOW + ((n - self.LOW) * key) % self.M))
			encoded += chr (self.LOW + ((n - self.LOW) * key) % self.M)
		print (encoded)
		return encoded
		
	def decode(self, str, key):
		decoded = ''
		print ('Decoding '+str+'...',end='')
		print()
		x = modInv(key, self.M)
		print ('find solving key...',x)
		for c in str:
			n = ord(c)
			solved = self.LOW+ x*(n-self.LOW) % self.M
			print (c,n,'->',chr(solved), solved)
			decoded += chr(solved)
		print (decoded)
		return decoded	
	
class Affine(Cipher):
	def __init__(self):
		super().__init__()
		
		self.mult = Mult()
		self.caesar = Caesar()
		encoded = None
		decoded = None
		
	def generate_keys(self):
		n1 = self.mult.generate_keys()
		n2 = self.caesar.generate_keys()
		return (n1,n2)
		
	def encode(self, str, key):
		encoded = self.mult.encode(str, key[0])
		encoded = self.caesar.encode(encoded, key[1])
		return encoded
		
	def decode(self, str, key):
		decoded = self.caesar.decode(str, key[1])
		decoded = self.mult.decode(decoded, key[0])
		return decoded
		
class Unbreakable(Cipher):
	def __init__(self):
		super().__init__()
		
	def generate_keys(self):
		return 'PASTA'
	
	def encode(self, str, key):
		encoded = ''
		for i in range(len(str)):
			c = str[i]
			k = key[i%len(key)]
			sum = ord(c)+ord(k)
			# print (sum)
			sum = self.LOW + sum % self.M
			print (c, ord(c)-self.LOW,'\t->\t',
					k, ord(k)-self.LOW,
					'\t\tSum:\t',sum-self.LOW,'\t',chr(sum))
			encoded += chr(sum)
		print (encoded)
		return encoded
			
	def decode(self, str, key):
		decrypt, decoded = '', ''
		print ('Finding decrypting key...', end = '')
		for c in key:
			# print (c, ord(c)-self.LOW)
			new = (self.M - (ord(c)-self.LOW))%self.M
			decrypt += chr(new + self.LOW)
		print (decrypt)
		for i in range (len(str)):
			decrypt_val = ord(decrypt[i%len(decrypt)])-self.LOW
			str_val = ord(str[i])-self.LOW
			new = (str_val + decrypt_val) % self.M
			print (str_val,'\t+\t',decrypt_val,'mod',self.M,'=\t',new,'\t->\t',new+self.LOW, chr (new+self.LOW))
			decoded += chr(new+self.LOW)
		print (decoded)
		# code_index = 0
		# for c in str:
			# n = ord(c)
			# new = (self.M - n) % self.M
			# print(c, n, new)
			# decoded += chr(new)
		# print (decoded)
		
class RSA(Cipher):
	def __init__(self, key=2):
		super().__init__()
		
	def encode(self, str, key):
		pass
		
	def decode(self, str, key):
		p = randPrime(4)
		q = randPrime(4)
		print ('p =',p,', q =',q)
		n = p*q
		phi = (p-1) * (q-1)
		e = random.randint(3, phi-1)
		d = modInv(e, phi)
		
		print ('Using: (',n,',',e,') as key')
		
		
		