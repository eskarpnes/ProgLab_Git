from users import Sender, Receiver, Hacker, Communicate
from cipher import Cipher, Caesar
from string import ascii_uppercase
def main():
	'''
	1: Caesar
	2: Multiplication
	3: Affine
	4: Unbreakable
	5: RSA
	
	'''
	print ('Proglab Exercise 3 - Cryptography')
	while True:
		print('Select a cryptography level:')
		print('1: Caesar')
		print('2: Multiplication')
		print('3: Affine')
		print('4: Unbreakable')
		print('5: RSA')
		level = int(input('>'))
		comm = Communicate(level)
		msg = ''
		while len(msg)<1:
			msg = input('Enter a message to be encrypted: ')
		print ('Message received.')
		enable_hack = input('Hack this message? (Y/N)...')
		send = comm.send
		if enable_hack.lower() == 'y':
			if not msg.isalpha():
				print ('Oops, the message must only contain letters! Solving this one normally')
			else:
				send = comm.hack
		send(msg)
		# comm.send(msg)
	comm = Communicate(2) # sets up sender and receiver
	send = comm.send
	hack = comm.hack
	# msg = ":-0 '^^,.-_:,;\+%/&# >~^.^~<"
	# send(msg)
	msg = 'maximal'
	hack(msg)
	# send(msg)
	
	
	# h = Hacker()
	
	# c_ciph = Caesar(2)
	# enc = c_ciph.encode('python')
	# dec = c_ciph.decode(enc)
	# c_ciph.decode("mqfg")
	# print(c_ciph.verify("!!122~~kenny drives a tractor"))
	
main()