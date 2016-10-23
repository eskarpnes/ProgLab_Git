import os
import timeit
import itertools
import re
import codecs
import math
from collections import defaultdict
from tools import Wordcloud, LoadingBar, Stopwords
import sys


_time = timeit.default_timer

class ReadReviews:
	def __init__(self, path, percent, ngrams=0):
		data_folder = path + '\\data\\subset\\train\\'
		self.test_folder = path + '\\data\\subset\\test\\'
		self.pos_test = os.listdir(self.test_folder + 'pos\\')
		self.neg_test = os.listdir(self.test_folder + 'neg\\')
		self.stop_words = Stopwords(path+'\\data\\stop_words.txt').get()

		self.percent = percent
		self.ngrams = ngrams
		
		
		self.pos_reviews = data_folder + 'pos'
		self.neg_reviews = data_folder + 'neg'
		
		self.pos_words, self.pos_list = None, None
		self.neg_words, self.neg_list = None, None
		self.all_reviews = None
		
		self.pos_info, self.neg_info = [], []	# information value
		self.pos_pop, self.neg_pop = [], []		# popularity value
	
		self.pos_info_dict = None
		self.neg_info_dict = None
		
	def n_grams(self, data, n):
		return ['_'.join(w for w in [data[i+j]
				for j in range(n)] if w != 'br')
				for i in range(0,len(data)-n, n)]

				
	def get_data(self, r):
		if self.ngrams > 0:
			data = [x for x in re.findall("\w+", r.read().lower().replace("'",''))]				
			ng = self.n_grams(data, self.ngrams)
			data = [x for x in data if x not in self.stop_words]
			return set(itertools.chain(data, ng))
		else:
			data = [x for x in re.findall("\w+", r.read().lower().replace("'",'')) if x not in self.stop_words]	
			return set(data)
			
			
	def get_words(self, folder):
		t0 = _time()
		words = set()
		reviews = []  # cannot be a set, as it's a list of sets
		path = os.listdir(folder)
		print ('Scanning',len(path), 'reviews')
		
		loading_bar = LoadingBar(len(path), folder)

		for review in path:
			with open(folder+"\\"+review,'r', encoding = 'utf-8') as r:
				data = self.get_data(r)
				reviews.append(data)
				words |= data

				loading_bar.update()
				
			r.close()
		loading_bar.finished()
		print ('\nGot words in',_time()-t0,'seconds')
		return words, reviews

	def prune(self):
		t0 = _time()
		_size = len(self.all_reviews)
		c = defaultdict(int)
		for review in self.all_reviews:
			for word in review:
				c[word] += 1
				
		_pos, _neg = [], []
		for w,count in c.items():
			if count/_size > self.percent and len(w)>3:
				if w in self.pos_words:
					_pos.append(w)
				if w in self.neg_words:
					_neg.append(w)
		
		print ('Pruned words in',_time()-t0,'seconds')
		self.pos_words, self.neg_words = set(_pos), set(_neg)
		# removes irrelevant words from the reviews
		self.pos_list = [{w for w in s if w in self.pos_words} for s in self.pos_list]
		self.neg_list = [{w for w in s if w in self.neg_words} for s in self.neg_list]
		
	def rev_sort(self, arr):
		return sorted(arr, key = lambda x:x[1], reverse=True)
		

	def get_count_dict(self, reviews):
		c = defaultdict(int)
		for r in reviews:
			for w in r:
				c[w] += 1
		return c
		
		
	def init_word_popularity(self):
		# populates two dicts with the usage of each word
		_pos = self.get_count_dict(self.pos_list)
		_neg = self.get_count_dict(self.neg_list)
				
		for k,v in _pos.items():
			self.pos_info.append((k, round(v / (v+_neg[k]), 2)))
			self.pos_pop.append((k, round(v/len(self.pos_list),2)))
			
		for k,v in _neg.items():
			self.neg_info.append((k, round(v / (v+_pos[k]), 2)))
			self.neg_pop.append((k, round(v/len(self.neg_list),2)))
		
		self.pos_info = self.rev_sort(self.pos_info)
		self.neg_info = self.rev_sort(self.neg_info)
		self.pos_pop = self.rev_sort(self.pos_pop)
		self.neg_pop = self.rev_sort(self.neg_pop)
		
		self.neg_info_dict = dict(self.neg_info)
		self.pos_info_dict = dict(self.pos_info)
		
		
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
		self.display_top(25, self.pos_pop, self.neg_pop, 'Popularity')
		
	def info_val(self):
		print ('\nInformation values:')
		self.display_top(25, self.pos_info, self.neg_info, 'Information')
		
	
	def learn(self):
		t0 = _time()
		
		self.pos_words, self.pos_list = self.get_words(self.pos_reviews)
		self.neg_words, self.neg_list = self.get_words(self.neg_reviews)
		self.all_reviews = list(itertools.chain(self.pos_list, self.neg_list))
		print ('Found',len(self.pos_words)+len(self.neg_words),' words, damn!')
		print ('Pruning away words that are not found in more than',self.percent*100,'% of the reviews')
		self.prune()
		print ("There's now",len(self.pos_words)+len(self.neg_words),' words!')
		
		self.init_word_popularity()
		self.pop_val()
		self.info_val()
		
		print ('\nLearned some stuff in',_time()-t0,'seconds!')
		
	def analyze(self, data, review, cutoff):
		pos_score, neg_score = 0,0
		for c in data:
			if c in self.pos_info_dict:
				if self.pos_info_dict[c] > cutoff:
					pos_score += self.pos_info_dict[c]
			if c in self.neg_info_dict:
				if self.neg_info_dict[c] > cutoff:
					neg_score += self.neg_info_dict[c]
		# print ('Pos score:',pos_score,'\tNeg score:',neg_score)
		
		root = self.pos_test if pos_score > neg_score else self.neg_test
		return True if review in root else False
	
		
	def test(self):
		t0 = _time()
		total = len(self.pos_test) + len(self.neg_test)
		cutoff = 0.3
		correct = 0
		for folder in os.listdir(self.test_folder):
			path = os.listdir(self.test_folder + '\\' + folder)
			loading_bar = LoadingBar(len(path), self.test_folder)
			for review in path:
				with open(self.test_folder+'\\'+folder+'\\'+review, 'r', encoding = 'utf-8') as r:
					data = self.get_data(r)
					if self.analyze(data, review, cutoff):
						correct += 1
					loading_bar.update()
				r.close()
			loading_bar.finished()
		print ('Guessed',correct,'right out of',total,'...',round(100*(correct/total), 2),'% with cutoff',cutoff)