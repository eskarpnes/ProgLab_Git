import sys

class LoadingBar:
	def __init__(self, _size, text):
		self.bar_size = 42
		self.tick = int(_size / self.bar_size)
		self.bar_size+=1
		self.count = 0
		self._size = _size
		
		print('Reading from',text)
		load = " Loading..."
		sys.stdout.write("[%s]" % (" " * self.bar_size))
		sys.stdout.write(load)
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.bar_size+1+len(load))) #added the length of "Loading..."

	def update(self):
		if self.count % self.tick == 0:
			sys.stdout.write('=')
			sys.stdout.flush()
		self.count += 1
		
		
	def finished(self):
		if self.count == self._size:
			sys.stdout.write("] DONE!     \n")
		pass
		# print (self.count, '%', self.tick, '=',self.count%self.tick,' (',)