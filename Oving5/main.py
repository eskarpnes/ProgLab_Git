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
    cam = False
    cam = input('Use cam? y/n > ')
    if cam == 'y':
        im = Img()
        im.whatup()
    else:
        img1 = Img(get_file())
        print ('Select another file!\n')
        img2 = Img(get_file())
        print ('\n..Applying a bunch of stuff')
        resized = img1.resize(img2.getSize())
        resized.show()
        cropped = img1.cropTopLeft(500,500)
        cropped.show()
        cropped2 = img1.cropMiddle(300,300)
        cropped2.show()
        rot45 = img1.rotate(45,zoom=False)
        rot45.show()
        zoomed = img1.zoom(5, 0.8,center=True)
        zoomed.show()
        fadedmatrix = img1.fadeMat(fade=20)
        fadedmatrix.show()
        blended = img1.blend(img2,0.7)
        blended.show()
        blendmatrix = img1.blendMat(img2)
        blendmatrix.show()
        gray = img1.gray()
        gray.show()
        bw = img1.bw()
        bw.show()
        sharp = img1.sharpen(factor=0.0)  # blur = 0.0, sharp = 2.0
        sharp.show()
        test = img1.fadeMat(3)
        test.show()
        m = img1.keepMax()
        m.show()
        edge = img1.edge()
        edge.show()
        emboss = img1.emboss()
        emboss.show()



main()
