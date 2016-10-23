import os
import timeit
import itertools
import re
import helpers
from tools import Wordcloud, LoadingBar
from review import Review
from math import log10


_time = timeit.default_timer

class Reviews:
	def __init__(self, path, percent, ngrams=0):
		self.data_folder = path + '\\data\\alle\\train\\'
		self.test_folder = path + '\\data\\alle\\test\\'
		
		self.percent = percent
		stopwords = helpers.file_as_list(path+'\\data\\stop_words.txt')
		self.positive = Review(ngrams, stopwords)
		self.negative = Review(ngrams, stopwords)
		self.test_pos = Review(ngrams, stopwords)
		self.test_neg = Review(ngrams, stopwords)

	def scan_reviews(self):
		self.scan(self.data_folder+'pos', self.positive)
		self.scan(self.data_folder+'neg', self.negative)
		
	def test_reviews(self):
		self.scan(self.test_folder+'pos', self.test_pos)
		self.scan(self.test_folder+'neg', self.test_neg)
		
	def scan(self, folder, review_handler):
		t0 = _time()
		path = os.listdir(folder)		
		print ('Scanning',len(path), 'reviews')
		loading_bar = LoadingBar(len(path), folder)
		for review in path:
			with open(folder+"\\"+review,'r', encoding = 'utf-8') as r:
				review_handler.update(r)
				loading_bar.update()
			r.close()
		loading_bar.finished()
		print ('\nScanned words in',_time()-t0,'seconds')

	def prune(self, pos, neg):
		t0 = _time()
		all_reviews = list(itertools.chain(pos.reviews, neg.reviews))
		c = helpers.get_count_dict(all_reviews)
		print ('There are',len(c),'reviews in total!')
		_pos, _neg = [], []
		for w,count in c.items():
			if count/len(all_reviews) > self.percent and len(w)>3:
				if self.positive.hasWord(w):
					_pos.append(w)
				if self.negative.hasWord(w):
					_neg.append(w)
		
		print ('Pruned words in',_time()-t0,'seconds')
		pos.prune(set(_pos))
		neg.prune(set(_neg))
		
	def init_word_popularity(self):
		self.positive.word_popularity(self.negative)
		self.negative.word_popularity(self.positive)

	def display_top(self, high, pos, neg, type):
		print ('\nPositive\t\t Negative\n')
		pos_text, neg_text = '', ''  # used for wordcloud
		shown = 0
		for sc1,sc2 in zip(pos, neg):
			if shown < 25:
				print ("%4s %15s \t %4s %15s" % (sc1[1],sc1[0], sc2[1], sc2[0]))
				pos_text+=sc1[0]+' '
				neg_text+=sc2[0]+' '
			shown+=1
		Wordcloud(type, pos_text, neg_text)
		
	def pop_val(self):
		print ('\nPopularity values:')
		self.display_top(25, self.positive.popularity, self.negative.popularity, 'Popularity')
		
	def info_val(self):
		print ('\nInformation values:')
		self.display_top(25, self.positive.info, self.negative.info, 'Information')
				
				
	def learn(self):
		t0 = _time()
		
		self.scan_reviews()
		
		print ('Found',len(self.positive.words)+len(self.negative.words),' words, damn!')
		print ('Pruning away words that are not found in more than',self.percent*100,'% of the reviews')
		self.prune(self.positive, self.negative)
		print ("There's now",len(self.positive.words)+len(self.negative.words),' words!')
		
		self.init_word_popularity()
		self.pop_val()
		self.info_val()
		
		print ('\nLearned some stuff in',_time()-t0,'seconds!')
		
	
	def check(self, obj, review, cutoff, positive):
		pos, neg = 0.0, 0.0
		for w in review:
			pos += helpers.analyze(self.positive, w, cutoff)
			neg += helpers.analyze(self.negative, w, cutoff)
		
		if pos>neg and positive:
			return True
		elif neg>pos and not positive:
			return True
		else:
			return False
				
	def test(self, cutoff):
		self.test_reviews()
		self.prune(self.test_pos, self.test_neg)
		correct = 0
		total = len(self.test_pos.reviews) + len(self.test_neg.reviews)
		print (total,'reviews to check...')
		for r in self.test_pos.reviews:
			if self.check(self.test_pos, r, cutoff, True):
				correct += 1
				
		for r in self.test_neg.reviews:
			if self.check(self.test_neg, r, cutoff, False):
				correct += 1
				
		
		print ('Guessed',correct,'out of',total,round(100*(correct/total), 2),'%')