from users import Sender, Receiver, Hacker, Communicate
from cipher import Cipher, Caesar
def main():
	'''
	1: Caesar
	2: Multiplication
	3: Aff
	4: RSA
	'''
	# s = Sender(2)
	# r = Receiver(s)
	# s.operate_cipher(msg)
	# r.operate_cipher()
	comm = Communicate(1) # sets up sender and receiver
	send = comm.send
	# msg = ":-0 '^^,.-_:,;\+%/&# >~^.^~<"
	# send(msg)
	msg = 'KODE'
	send(msg)
	
	
	# h = Hacker()
	
	# c_ciph = Caesar(2)
	# enc = c_ciph.encode('python')
	# dec = c_ciph.decode(enc)
	# c_ciph.decode("mqfg")
	# print(c_ciph.verify("!!122~~kenny drives a tractor"))
	
main()