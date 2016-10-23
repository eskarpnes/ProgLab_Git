# from imdbReviews import ReadReviews
import os
from PIL import Image
# from rev2 import ReadReviews
from readreviews import Reviews


def main():
	_percent, _ngrams, cutoff = 0.02, 2, 0.4
	path = os.getcwd()
	reviews = Reviews(path, _percent)  # ngrams optional
	
	reviews.learn()
	reviews.test(cutoff)
	
	Image.open('Information_cloud.png').show()
	Image.open('Popularity_cloud.png').show()
main()