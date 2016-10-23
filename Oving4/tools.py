import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
				

class Wordcloud:
	def __init__(self, type, text1, text2):
		file_name = type+'_cloud'+'.png'
		print ('Generating',file_name)
		plt.figure(figsize=(20,10))
		self.init_plot(211, 'Positive', text1)
		self.init_plot(212, 'Negative', text2)
		# plt.show()
		plt.savefig(file_name, facecolor='k',bbox_inches = 'tight')
		
	def init_plot(self, pos, title, text):
		plt.subplot(pos)
		plt.title(title)
		# self.show_cloud(text)
		plt.imshow(self.get_cloud(text))
		plt.axis("off")
		
	def get_cloud(self, text):
		return WordCloud(width=1600, height=800).generate(text)