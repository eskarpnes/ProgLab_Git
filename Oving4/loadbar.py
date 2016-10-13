import sys

class LoadingBar:
	def __init__(self, _size):
		self.bar_size = 50
		self.tick = _size / self.bar_size
		self.count = 0
		self._size = _size

		sys.stdout.write("[%s]" % (" " * self.bar_size))
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.bar_size+1))
		
	def get_tick(self):
		return self.tick
	
	def update(self):
		if self.count % self.tick == 0:
			sys.stdout.write('-')
			sys.stdout.flush()
		self.count += 1
		
	def finished(self):
		if self.count == self._size:
			sys.stdout.write("] DONE!\n")
		