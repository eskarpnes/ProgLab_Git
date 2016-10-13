from imdbReviews import ReadReviews
import os

def main():
	PERCENT, NGRAMS = 0.01, 2
	reviews = ReadReviews(os.getcwd(), PERCENT, NGRAMS)  # ngrams optional
	
main()