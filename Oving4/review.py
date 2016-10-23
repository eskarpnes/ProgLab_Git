import helpers
import re
import itertools

class Review:
	def __init__(self, ngrams, stopwords):
		self.ngrams = ngrams
		self.words = set()
		self.reviews = []
		self.info = []
		self.info_dict = None
		self.pop_dict = None
		self.popularity = []
		self.stopwords = stopwords
		
		self.getter = self.data
		if ngrams > 0:
			self.getter = self.ngram_data
	
	def update(self, r):
		data = self.getter(r)
		self.reviews.append(data)
		self.words |= data

	def ngram_data(self, r):
		data = [x for x in re.findall("\w+", r.read().lower().replace("'",''))]
		ng = ['_'.join(w for w in [data[i+j]
				for j in range(self.ngrams)] if w != 'br')
				for i in range(0,len(data)-self.ngrams, self.ngrams)]
		data = [x for x in data if x not in self.stopwords]
		return set(itertools.chain(data, ng))
		
	def data(self, r):
		data = [x for x in re.findall("\w+", r.read().lower().replace("'",'')) if x not in self.stopwords]
		return set(data)
		
	def prune(self, words):
		if type(words) == type(set()):
			self.words = words
			self.cleanify()
		
	def cleanify(self):
		# removes irrelevant words from the reviews
		# after the pruned words have been updated
		self.reviews = [{w for w in s if w in self.words} for s in self.reviews]
		
	def hasWord(self, w):
		return True if w in self.words else False
		
	def countable(self):
		return helpers.get_count_dict(self.reviews)
		
	def word_popularity(self, other):
		other_ = other.countable()
		for k,v in self.countable().items():
			self.info.append((k, round(v / (v+other_[k]), 2)))
			self.popularity.append((k, round(v/len(self.reviews),2)))
		self.info = helpers.rev_sort(self.info)
		self.popularity = helpers.rev_sort(self.popularity)
		self.info_dict = dict(self.info)
		self.pop_dict = dict(self.popularity)
