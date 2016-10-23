from collections import defaultdict

def file_as_list(path):
	with open(path, 'r') as s:
		return {w.strip() for w in s.readlines()}
		# set for faster lookup later on
	s.close()

def rev_sort(arr):
	return sorted(arr, key = lambda x:x[1], reverse=True)
		
	
def get_count_dict(reviews):
	# list of reviews
	c = defaultdict(int)
	for r in reviews:
		for w in r:
			c[w] += 1
	return c

def analyze(other, word, cutoff):
	if word in other.info_dict:
		if other.info_dict[word] > cutoff:
			return other.info_dict[word]
	return 0