import os
import timeit
import itertools
import re
import codecs
# import sys
from collections import defaultdict
from cloud import Wordcloud
from loadbar import LoadingBar

_time = timeit.default_timer

class ReadReviews:
	def __init__(self, path, percent, ngrams=0):
		data_folder = path + '\\data\\alle\\train\\'
		self.PERCENT = percent
		self.ngrams = ngrams
		
		self.stop_words = self.update_stopwords(path+'\\data\\stop_words.txt')
		self.pos_reviews = data_folder + 'pos'
		self.neg_reviews = data_folder + 'neg'
		
		self.pos_words, self.pos_list = None, None
		self.neg_words, self.neg_list = None, None
		self.all_reviews = None
		
		self.pos_info, self.neg_info = [], []	# information value
		self.pos_pop, self.neg_pop = [], []		# popularity value
		
		self.learn()
	
	def update_stopwords(self, path):
		with open(path, 'r') as stoplist:
			stop_words = {w.strip() for w in stoplist.readlines()}
			# set for faster lookup later on
		stoplist.close()
		return stop_words

		
	def n_grams(self, data, n):
		return ['_'.join(w for w in [data[i+j]
				for j in range(n)])
				for i in range(0,len(data)-n, n)]

				
	def get_words(self, folder):
		t0 = _time()
		words = set()
		reviews = []  # cannot be a set, as it's a list of sets
		path = os.listdir(folder)
		print ('Size of reviews:',len(os.listdir(folder)))
		
		loading_bar = LoadingBar(len(path))

		for review in path:
			with open(folder+"\\"+review,'r', encoding = 'utf-8') as r:
				data = [x for x in
				re.findall("\w+", r.read().lower().replace("'",''))
				if x not in self.stop_words]
				# n_gram_set = n_grams(data, self.ngrams)
				# print(n_gram_set)
				# data = set(itertools.chain(data, n_gram_set))
				data = set(data)
				reviews.append(data)
				words |= data
				
				# loading bar
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
			if count/_size > self.PERCENT and len(w)>3:
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
		
		
	def display_top(self, high, pos, neg):
		print ('\nPositive\t\t Negative\n')
		pos_text, neg_text = '', ''  # used for wordcloud
		shown = 0
		for sc1,sc2 in zip(pos, neg):
			if shown < 25:
				print ("%4s %15s \t %4s %15s" % (sc1[1],sc1[0], sc2[1], sc2[0]))
				pos_text+=sc1[0]+' '
				neg_text+=sc2[0]+' '
			shown+=1
		Wordcloud(pos_text, neg_text)
		
		
	def pop_val(self):
		print ('\nPopularity values:')
		self.display_top(25, self.pos_pop, self.neg_pop)
		
	def info_val(self):
		print ('\nInformation values:')
		self.display_top(25, self.pos_info, self.neg_info)
		
	
	def learn(self):
		self.pos_words, self.pos_list = self.get_words(self.pos_reviews)
		self.neg_words, self.neg_list = self.get_words(self.neg_reviews)
		self.all_reviews = list(itertools.chain(self.pos_list, self.neg_list))
		print ('Found',len(self.pos_words)+len(self.neg_words),' words, damn!')
		print ('Pruning away words that are not found in more than',self.PERCENT*100,'% of the reviews')
		self.prune()
		print ("There's now",len(self.pos_words)+len(self.neg_words),' words!')
		
		self.init_word_popularity()
		self.pop_val()
		self.info_val()
		
		print ('Creating a list of all known words and their information value...')
		return list(itertools.chain(self.pos_info, self.neg_info))
		print ('...Done!')
