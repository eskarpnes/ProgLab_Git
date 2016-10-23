import os
import timeit
import sys
import itertools
from tools import LoadingBar
from reviews import Reviews

_time = timeit.default_timer

class ReadReviews(Reviews):
	def __init__(self, path, percent, ngrams=0):
		super().__init__(path, percent, ngrams)
		
	def learn(self):
		t0 = _time()
		
		self.scan_reviews()
		
		print ('Found',len(self.positive.words)+len(self.negative.words),' words, damn!')
		print ('Pruning away words that are not found in more than',self.percent*100,'% of the reviews')
		self.prune()
		print ("There's now",len(self.positive.words)+len(self.negative.words),' words!')
		
		self.init_word_popularity()
		self.pop_val()
		self.info_val()
		
		print ('\nLearned some stuff in',_time()-t0,'seconds!')
		

	def test(self, cutoff):
		pos_path = os.listdir(self.test_folder + 'pos\\')
		neg_path = os.listdir(self.test_folder + 'neg\\')
		total = len(pos_path) + len(neg_path)
		correct = 0
		for folder in os.listdir(self.test_folder):
			sub = self.test_folder + '\\' + folder
			path = os.listdir(sub)
			loading_bar = LoadingBar(len(path), self.test_folder)
			for review in path:
				with open(sub+'\\'+review, 'r', encoding = 'utf-8') as r:
					data = self.get_data(r)
					if self.analyze(data, review, cutoff, pos_path, neg_path):
						correct += 1
					loading_bar.update()
				r.close()
			loading_bar.finished()
		print ('Guessed',correct,'right out of',total,'...',round(100*(correct/total), 2),'% with cutoff',cutoff)