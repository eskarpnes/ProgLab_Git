from image import Img
from PIL import Image
import os
import time
import random

def handle_input(input_list):
    for num,img in enumerate(input_list):
        print (num,'\t',img)
    try:
        return int(input('\n> Select an image: '))
    except:
        print ('Invalid input, giving you a random image...')
        return random.randint(0,len(input_list)-1)
        
def get_file():
    path = 'images\\'
    folder = os.listdir(path)
    selected = handle_input(folder)
    print ('\nYou selected:', folder[selected])
    return path+folder[selected]

def main():
    # img1 = Img(get_file())
    img1 = Img('images\\kdfinger.jpeg')
    # img1.show()
    img2 = Img('images\\einstein.jpeg')
    # resized = img1.resize(img2.getSize())
    # resized.show()
    # cropped = img1.cropTopLeft(500,500)
    # cropped.show()
    # cropped2 = img1.cropMiddle(300,300)
    # cropped2.show()
    # sq = img1.makeSquare()
    # sq.show()
    # rot45 = img1.rotate(45,zoom=False)
    # rot45.show()
    # scaled = img1.scale(0.5)
    # scaled.show()
    zoomed = img1.zoom(5, 0.8,centre=True,deg=20)
    zoomed.show()
    
    
main()

# def other():
    # opens the einstein pic in the background
    # im = Image.open(path+"einstein.jpeg") 
    # empty image to store different once on:
    # empty = Image.new('RGB', (400,400))
    # im.thumbnail((100,100))
    # for img in img_folder:
    # for i in range(0,500,100):
        # for j in range(0,500,100):
            # im = Image.eval(im, lambda x: x+(i/20+j/40))
            # empty.paste(im, (i,j))
    # empty.show()
    