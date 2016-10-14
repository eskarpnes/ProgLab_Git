import os
import timeit
import itertools
import re
import codecs
import math
# import sys
from collections import defaultdict
#from cloud import Wordcloud
from loadbar import LoadingBar


_time = timeit.default_timer

class ReadReviews:
	def __init__(self, path, percent, ngrams=0):
		data_folder = path + '\\data\\alle\\train\\'
		self.test_folder = path + '\\data\\alle\\test\\'
		self.pos_test = os.listdir(self.test_folder + 'pos\\')
		self.neg_test = os.listdir(self.test_folder + 'neg\\')
		print (data_folder)
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
		
		self.pos_dict = defaultdict(float)
		self.neg_dict = defaultdict(float)
		self.pos_info_dict = defaultdict(float)
		self.neg_info_dict = defaultdict(float)
	
	def update_stopwords(self, path):
		with open(path, 'r') as stoplist:
			stop_words = {w.strip() for w in stoplist.readlines()}
			# set for faster lookup later on
		stoplist.close()
		return stop_words

		
	def n_grams(self, data, n):
		return ['_'.join(w for w in [data[i+j]
				for j in range(n)] if w != 'br')
				for i in range(0,len(data)-n, n)]

				
	def get_data(self, r):
		# data = [x for x in re.findall("\w+", r.read().lower().replace("'",''))]				
		# ng = self.n_grams(data, self.ngrams)
		# remove stopwords
		# data = [x for x in data if x not in self.stop_words]
		data = [x for x in re.findall("\w+", r.read().lower().replace("'",'')) if x not in self.stop_words]	
		return set(data)
		# return set(itertools.chain(data, ng))
				
	def get_words(self, folder):
		t0 = _time()
		words = set()
		reviews = []  # cannot be a set, as it's a list of sets
		path = os.listdir(folder)
		print ('Size of reviews:',len(path))
		
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
			
			self.pos_dict[k] = round(v/len(self.pos_list),2)
			self.pos_info_dict[k] = round(v / (v+_neg[k]),2)
			
		for k,v in _neg.items():
			self.neg_info.append((k, round(v / (v+_pos[k]), 2)))
			self.neg_pop.append((k, round(v/len(self.neg_list),2)))
			
			self.neg_dict[k] = round(v/len(self.neg_list),2)
			self.neg_info_dict[k] = round(v / (v+_pos[k]), 2)
		
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
		#Wordcloud(pos_text, neg_text)
		
	def pop_val(self):
		print ('\nPopularity values:')
		self.display_top(25, self.pos_pop, self.neg_pop)
		
	def info_val(self):
		print ('\nInformation values:')
		self.display_top(25, self.pos_info, self.neg_info)
		
	
	def learn(self):
		t0 = _time()
		
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
		
		print ('Learned some stuff in',_time()-t0,'seconds!')
		return self.pos_pop, self.neg_pop
		print ('...Done!')
		
	def analyze(self, data, review):
		pos_score, neg_score = 0,0
		for c in data:
			if c in self.pos_info_dict:
				if self.pos_info_dict[c] < 0.3:
					pass
			elif c in self.neg_info_dict:
				if self.neg_info_dict[c] < 0.3:
					pass
			else:
				pos_score += self.pos_dict[c]
				neg_score += self.neg_dict[c]
			
			# neg_score += math.log(self.neg_dict[c])
		# print ('Pos score:',pos_score,'\tNeg score:',neg_score)
		
		root = self.neg_test
		if pos_score > neg_score:
			root = self.pos_test
		if review in root:
			return True
	
		
	def test(self):
		t0 = _time()
		words = set()
		reviews = []
		correct = 0
		total = len(self.pos_test) + len(self.neg_test)
		for folder in os.listdir(self.test_folder):
			path = os.listdir(self.test_folder + '\\' + folder)
			loading_bar = LoadingBar(len(path), self.test_folder)
			for review in path:
				with open(self.test_folder+'\\'+folder+'\\'+review, 'r', encoding = 'utf-8') as r:
					data = self.get_data(r)
					if self.analyze(data, review):
						correct += 1
					loading_bar.update()
				r.close()
			loading_bar.finished()
			
		print ('Guessed',correct,'right out of',total,'...',round(100*(correct/total), 2),'%')