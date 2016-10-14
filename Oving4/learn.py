from imdbReviews import ReadReviews
import os

def main():
	PERCENT, NGRAMS = 0.02, 2
	path = os.getcwd()
	reviews = ReadReviews(path, PERCENT, NGRAMS)  # ngrams optional
	pos_values, neg_values = reviews.learn()
	
	analyzed = reviews.test()
main()