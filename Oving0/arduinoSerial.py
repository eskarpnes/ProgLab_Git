import serial
import time

class Arduino:
	def __init__(self):
		print 'Initializing Arduino on serial port...'
		self.ard = serial.Serial()
		self.init_COM()
		self.COMPORT = None
		
	def get_com(self):
		return self.COMPORT
		
	def get_morse(self):
		return str(self.ard.readline()[:-2])
	
	def init_COM(self):
		available = False
		for comPort in range (6,12): #had another arduino at com 5
			if self.try_port(comPort):
				available = True
				self.COMPORT = comPort
				print ("Connection established at COM"+str(comPort)+", please wait.")
				time.sleep(2)
				break
		if available:
			print ("Everything OK. Listening...")
			
	def try_port(self, com):
		port_name = "COM"+str(com)
		try:
			global ard
			self.ard = serial.Serial(port_name,9600,timeout=0)
			return True
		except:
			print(port_name+" unavailable")
			return False