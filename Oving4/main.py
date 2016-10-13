import os
import re
import itertools
import codecs
from collections import defaultdict
from copy import copy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import timeit
# delchars = {str(c) for c in map(chr, range(256)) if not c.isalnum()}
# print (delchars)

_time = timeit.default_timer

def rev_sort(arr):
	return sorted(arr, key = lambda x:x[1], reverse=True)

def n_grams(data, n):
	return ['_'.join(w for w in [data[i+j]
			for j in range(n)])
			for i in range(0,len(data)-n, n)]
	
def get_words(folder, stopwords, ngrams=0):
	t0 = _time()
	
	_path = os.listdir(folder)
	words = set()
	all_reviews = []  # cannot be a set, as it's a list of sets
	for review in _path:
		with open(folder+"\\"+review,'r', encoding = 'utf-8') as rev:
			data = [x for x in re.findall("\w+", rev.read().lower().replace("'",'')) if x not in stopwords]
			# n_gram_set = n_grams(data, ngrams)
			# # print(n_gram_set)
			# data = set(itertools.chain(data, n_gram_set))
			data = set(data)
			all_reviews.append(data)
			words |= data
		rev.close()
		# print ('Added review')
		
	t1 = _time()
	print ('Got words in',t1-t0,'seconds')
	return words, all_reviews

	
def prune(percent, pos, neg, all):
	t0 = _time()
	
	_size = len(all)
	c = defaultdict(int)
	for review in all:
		for word in review:
			c[word] += 1
	# _pos = [w for w,count in c.items() if w in pos and count/_size > percent]
	# _neg = [w for w,count in c.items() if w in neg and count/_size > percent]
	# valid_words = [w for w,count in c.items() if count/_size > percent]
	_pos, _neg = [], []
	for w,count in c.items():
		if count/_size > percent and len(w)>3:
			if w in pos:
				_pos.append(w)
			if w in neg:
				_neg.append(w)
	
	t1 = _time()
	print ('Pruned words in',t1-t0,'seconds')
	return set(_pos), set(_neg)
	
	
def show_pop(name, words, reviews):
	local,total = 0,0
	popularity = []

	for word in words:
		local,total = 0,0
		for review in reviews:
			if word in review:
				local += 1
			total += 1
		popularity.append((word, local / total))

		shown = 1
	print ('\nTop 25:',name,'\n')
	popularity = rev_sort(popularity)
	print('# \t Score \t Word\n')
	for wordscore in popularity:
		if shown<=25:
			print (shown,'\t',round(wordscore[1],2),'\t', wordscore[0])
		shown+=1
	print ()
	return popularity
	
	
def gen_wordcloud(text1, text2):
	# cloud = WordCloud().generate(text)
	# plt.imshow(cloud)
	cloud1 = WordCloud(max_font_size=50, relative_scaling=1).generate(text1)
	plt.figure(figsize=(10,10))
	plt.subplot(211)
	plt.title('Positive')
	plt.imshow(cloud1, interpolation='nearest', aspect='auto')
	plt.axis("off")
	
	cloud2 = WordCloud(max_font_size=50, relative_scaling=1).generate(text2)
	plt.subplot(212)
	plt.title('Negative')
	plt.imshow(cloud2, interpolation='nearest', aspect='auto')
	plt.axis("off")
	plt.show()
	
	
def info_val (percent, pos_word, neg_word, pos_rev, neg_rev):
	_pos, _neg = defaultdict(int), defaultdict(int)

	for rev in pos_rev:
		for word in rev:
			_pos[word] += 1	
			
	for rev in neg_rev:
		for word in rev:
			_neg[word] += 1
	
	pos_scores, neg_scores = [], []
	
	for k,v in _neg.items():
		# compare values for pos and neg:
		# print ('Pos for',k,'=',_pos[k])
		# print ('Neg for',k,'=',v)
		# _total = v + _pos[k]  # the value of both dicts at word k
		# pos_scores.append((k, round(_pos[k] / _total, 2)))
		neg_scores.append((k, round(v/(v+_pos[k]), 2)))
	for k,v in _pos.items():
		pos_scores.append((k, round(v/(v+_neg[k]), 2)))
	
	pos_scores = rev_sort(pos_scores)
	neg_scores = rev_sort(neg_scores)
	
	shown = 1
	print ('\nPositive\t\t Negative\n')
	pos_text, neg_text = '', ''  # used for wordcloud
	for sc1,sc2 in zip(pos_scores, neg_scores):
		if shown < 26:
			# print (sc1[1],'\t',sc1[0],'\t\t',sc2[1],'\t',sc2[0])
			print ("%4s %15s \t %4s %15s" % (sc1[1],sc1[0], sc2[1], sc2[0]))
			pos_text+=sc1[0]+' '
			neg_text+=sc2[0]+' '
		shown+=1

	gen_wordcloud(pos_text, neg_text)

	
def update_stopwords(path):
	t0 = _time()
	
	stop_words = None
	with open(path, 'r') as stoplist:
		stop_words = {w.strip() for w in stoplist.readlines()}  # set for faster lookup later on
	stoplist.close()
	
	t1 = _time()
	print ('Registered stopwords in',t1-t0,'seconds')
	return stop_words

	
def main():
	path = os.getcwd()
	data_folder = path + '\\data\\alle\\'
	stop_words = update_stopwords(path+'\\data\\stop_words.txt')
	# print(os.listdir(data_folder))
	# test_folder = data_folder + 'test'
	pos_reviews = data_folder + 'train\\pos'
	neg_reviews = data_folder + 'train\\neg'
	
	N_GRAMS = 2
	PERCENT = 0.02
	
	pos_words, pos_list = get_words(pos_reviews, stop_words, N_GRAMS)
	neg_words, neg_list = get_words(neg_reviews, stop_words, N_GRAMS)
	
	
	all_reviews = list(itertools.chain(pos_list, neg_list))
	print ('Found',len(pos_words)+len(neg_words),' words, damn!')
	
	print ('Pruning away words that are not found in more than',PERCENT*100,'% of the reviews')
	pos_words, neg_words = prune(PERCENT, pos_words, neg_words, all_reviews)
	print ("There's now",len(pos_words)+len(neg_words),' words!')
	
	# prune the words in the reviews
	pos_list = [{w for w in s if w in pos_words} for s in pos_list]
	neg_list = [{w for w in s if w in neg_words} for s in neg_list]

	
	# print (pos_list)
	# popularity value
	# pop_pos = show_pop('Popularity positive',pos_words, pos_list)
	# pop_neg = show_pop('Popularity negative',neg_words, neg_list)
	
	# information value
	info_val(PERCENT, pos_words, neg_words, pos_list, neg_list)
	

	
t0 = _time()
main()
t1 = _time()
print ('Completed program in',t1-t0,'seconds')