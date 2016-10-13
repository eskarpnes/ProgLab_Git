	
#define a set of valid strings.

# del_set = ''.join(ch for ch in map(chr, range(256)) if ch not in letter_set)
# print (del_set)
# uni_set = ''.join(x for x in "ers µ, æ, Å, Ç, ß,... S" if unicodedata.category(x) != 'Po')

# def trim_unicode(s):
	# return [x for x in s if x==' ' or (unicodedata.category(x) == 'Lu' or unicodedata.category(x) == 'Ll')]
	
# s = "YO hello xD ;æ128938192 I didnt like this ;P '9'7231@@o312å3æ1231æø¨åø¨0"
# pattern = re.compile('[\W_]+') # used to remove a certain pattern from each string
# data =  re.sub(pattern, ' ', s.replace("'",""))
# print (data)
# letter_set = frozenset(string.ascii_lowercase + string.ascii_uppercase)
# tab = str.maketrans(string.ascii_lowercase + string.ascii_uppercase, string.ascii_lowercase * 2)
# deletions = ''.join(ch for ch in map(chr,range(256)) if ch not in letter_set)

# def cleanify(s):
	# return filter(letter_set.__contains__, s.lower())
	
	
# s = ' '.join([x for x in rev.read().replace("'",'').lower().split() if x not in stopwords])
# s = s.translate({ord(c): None for c in delchars if c != ' '})
# data = set(s.split())
# print(data)

def prune(percent, words, all):
	count = 0
	_size = len(all)
	new_set = set()
	for word in words:
		count = 0
		for review in all:
			if word in review:
				count += 1
		if count/_size>percent:# 0.5 is usually a word that has only appeared once
			# print (word, 'found in',count,'out of',total,'reviews. Score =',score)
			new_set.add(word)
	return new_set

		
# creates a folder if it doesn't exist
def create_folder(path):
	if not os.path.isdir(path):
		os.makedirs(path)
		
def check_files(path, files):
	for f in files:
		if not os.path.exists(path+'\\'+f):
			return False
	return True
	
	# used to store already parsed data
	parsed_data = path + '\\parsed'
	create_folder(parsed_data)
	parse_files = 'pos_w pos_list neg_w neg_list'.split()
	got_parsed = check_files(parsed_data, parse_files)
	print ('Already parsed data?', got_parsed)
		
	# parse when done
	# if not got_parsed:
		# parsed_lists = [pos_words, pos_list, neg_words, neg_list]
		# # for p in parsed_lists:
			# # print (type(p))
		# current_file = 0
		# for f in parse_files:
			# with open(parsed_data+'\\'+f, 'w') as p:
				# if type(parsed_lists[current_file][0]) == type(set()):
					# for _set in parsed_lists[current_file]:
						# for item in _set:
							# p.write(item)
							# p.write(' ')
					# p.write('\n')
				# else:
					# for item in parsed_lists[current_file]:
						# p.write(item)
						# p.write(' ')
			# p.close()
			# current_file+=1
				
				
	
# def show_popularity(name, words, specific, other=None):
	# local_word,word_total = 0,0
	# popularity = []
	# info_val = other is not None
	
	# for word in words:
		# local_word,word_total = 0,0
		# for review in specific:
			# if word in review:
				# local_word += 1
			# if not info_val:
				# word_total += 1

		# # if other is None:
		# if info_val:
			# for review in other:
				# if word in review:
					# word_total += 1
			# word_total += local_word 
			# # as word_total is only the words found in the other half (neg for pos etc)
		# score = local_word/word_total
		# popularity.append((word,score))
		
	# shown = 1
	# print ('\nTop 25:',name,'\n')
	# popularity = sorted(popularity, key = lambda x:x[1], reverse=True)
	# print('# \t Score \t Word\n')
	# for wordscore in popularity:
		# if shown<=25:
			# print (shown,'\t',round(wordscore[1],2),'\t', wordscore[0])
		# shown+=1
	# print ()
	# return popularity
	
def show_info_val(name, words, reviews, other_reviews):
	local,total = 0,0
	vals = []
	for word in words:
		local,total = 0,0
		for review in reviews:
			if word in review:
				local += 1
		for r2 in other_reviews:
			if word in r2:
				total += 1
		total += local
		vals.append((word, local/total))
	
	shown = 1
	print ('\nInfo Top 25:',name,'\n')
	vals = rev_sort(vals)
	print('# \t Score \t Word\n')
	for wordscore in vals:
		if shown<=25:
			print (shown,'\t',round(wordscore[1],2),'\t', wordscore[0])
		shown+=1
	print ()
	return vals
	