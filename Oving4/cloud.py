from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Wordcloud:
	def __init__(self, text1, text2):
		plt.figure(figsize=(10,10))
		self.init_plot(211, 'Positive', text1)
		self.init_plot(212, 'Negative', text2)
		plt.show()
		
	def init_plot(self, pos, title, text):
		plt.subplot(pos)
		plt.title(title)
		self.show_cloud(text)
		plt.axis("off")
		
	def get_cloud(self, text):
		return WordCloud(max_font_size=40, relative_scaling=1).generate(text)
		
	def show_cloud(self, text):
		plt.imshow(self.get_cloud(text), interpolation='nearest', aspect='auto')