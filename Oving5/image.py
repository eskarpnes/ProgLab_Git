from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps, ImageGrab
import os
import cv2
import winsound
from math import log2, pow

class Img:

    def __init__(self, file=False, img=False, name=None):
        super(Img, self).__init__()
        self.name = name
        self.x, self.y = 0, 0
        if file:
            if name is None:
                self.name = os.path.basename(file)
            print ('Loading...',self.name)
            self.image = self.open(file)
            self.x, self.y = self.image.size
            print (self.image.size)
        elif img:
            self.image = img
            self.x, self.y = self.image.size
        else:
            print('initializing an empty Image class')
        
        self.effects = [
            self.emboss,
            self.blur,
            self.bw,
            self.keepMax]
            

    '''
    Final test
    capture webcam
    capture screen
    put webcam in top left corner
    create a matrix of 4 of these images
    top left: normal
    top right: mirrored
    bottom left: embossed flipped
    bottom right: black white flipped and mirrored
    '''
    def whatup(self):
        print ('\nSmile :)\n')
        cam_images = []
        amount = int(pow(2,2))
        img_size = int(1080/(amount/2))
        
        for i in range(amount):
            capture = Img(img=self.capture(i),name='webcam pic')
            cam_images.append(Img(img=capture.square(img_size)))
        
        # create a blending image from the first and last pic
        # blended_cam = cam_images[0].blendMat(cam_images[-1]).show()
        
        # create a collage of the 4 images
        self.collage(cam_images)
        # cam_images = [you.rotate(i,zoom=True) for i in range(0,271,90)]
        # screen = self.screenshot()        
        # screen.paste(you.getImage(),(0,0,you.x,you.y))
        # env = Img(img=screen)
        # env.show()
        # make another 3 images, listed above

    def collage(self,_list):
        # collage must be of 2^N * 2^N size
        x = _list[0].x
        side = int(x * log2(len(_list)))
        added = 0
        print ('Creating',side,'x',side,'collage...')
        # print ('Each image is of the size',x,'x',x)
        bg = self.getBlank(side,side)
        for i in range(0,side,x):
            for j in range(0,side,x):
                # apply an effect to the image
                print ('\nApplying effect:',end='')
                img = Img(img=_list[added].effects[added]())
                if added==1:
                    img = img.flip(vertical=False)
                elif added==2:
                    img = img.flip()
                elif added==3:
                    img = img.flip(both=True)
                else:
                    img = img.getImage()
                print()
                bg.paste(img,(i,j))
                added += 1
        bg.show()
        return bg
                
                
        # creating blank image
        
        

    '''System based (screenshot and webcam)'''
    def capture(self,num=0):
        cap = cv2.VideoCapture(0) # captures one frame
        empty,img = cap.read()
        # print(img)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        shots = ['Nice!','Looking handsome!','Neat!','The perfect shot!']
        print('\n',shots[num])
        winsound.PlaySound("smile.wav",winsound.SND_ALIAS)
        return pil_img

    def screenshot(self):
        return ImageGrab.grab()

    '''Ops library'''
    def flip(self,vertical=True, both=False):
        img = self.getCopy()
        if both:
            vert = ImageOps.flip(img)
            return ImageOps.mirror(vert)
        elif vertical:
            return ImageOps.flip(img)
        else:
            return ImageOps.mirror(img)

    '''Filter library'''
    def applyFilter(self,f,levels):
        filter = self.image.filter(f)
        for i in range(levels):
            filter = filter.filter(f)
        return filter
    def edge(self,levels=3):
        print ('Finding edges...')
        return self.applyFilter(ImageFilter.EDGE_ENHANCE,levels)
    def emboss(self,levels=1):
        print ('Embossssssssss...')
        return self.applyFilter(ImageFilter.EMBOSS,levels)

    def blur(self,r=5):
        print ('Blurring with r =',r)
        return self.image.filter(ImageFilter.GaussianBlur(r))
    def blurMat(self, max_blur=50):
        def f(i,j,layers,size):
            step = max_blur/(2*layers*size)
            return self.blur((i+j)*step)
        return self.makeMatrix(f,img=True)

    '''Enhancements library'''
    def gray(self,factor=0.0):
        print ('Throwing',self.name,'back to the 19th century')
        color = ImageEnhance.Color(self.image)
        return color.enhance(factor)
        return self.image.convert('1')

    def brightness(self,factor=0.5):
        print ('Brightening...')
        bright = ImageEnhance.Brightness(self.image)
        return bright.enhance(factor)

    def sharpen(self,factor=2.0): # 0 = blurry, 2 = sharp
        print ('Sharpening...')
        sharp = ImageEnhance.Sharpness(self.image)
        return sharp.enhance(factor)

    '''Manipulations'''
    def aspectSquare(self):
        print ('Making a square of',self.name,', but keeping aspect ratio')
        long_side = max(self.image.size)
        hor = (long_side - self.x)/2
        ver = (long_side - self.y)/2
        return self.crop(-hor,-ver,hor+self.x,ver+self.y)
         
    def zoom(self, layers=10, scale=0.8, center=False):
        print ('Zoooooming in on',self.name)
        zoomed = self.getCopy()
        for i in range(layers):
            smaller = self.scale(scale**(i+1))
            if center:
                zoomed.paste(smaller, self.getCentreTuple(smaller))
            else:
                zoomed.paste(smaller,(0,0,smaller.size[0],smaller.size[1]))
        return zoomed

    def makeMatrix(self,func,layers=5,size=200,img=False):
        # if img is true: handle an image instead of each pixel
        print('Creating a', layers, 'x', layers, 'matrix')
        # universal function to apply functions
        # to each image in an NxN matrix
        s = layers*size
        sq = Image.new('RGB',(s,s)) # background
        tmp = self.square(size)
        for i in range(0,s,size):
            for j in range(0,s,size):
                # lambda applies a function f on each pixel x
                q = None
                if img:
                    q = Img(img=func(i,j,layers,size))
                    q = q.square(size)
                else:
                    q = Image.eval(tmp, lambda x: func(x,i,j))
                sq.paste(q, (i,j))
        return sq

    def fadeMat(self,fade):
        print ('Initializing matrix with function fade')
        def f(x,i,j):
            return x+(i+j)/fade
        return self.makeMatrix(f)

    def blendMat(self, other):
        def f(i,j,layers,size):
            step = 1 / (1.5*layers*size)
            return self.blend(other,(i+j)*step)
        return self.makeMatrix(f,img=True)

    def blend(self, other, alpha):
        # print ('Blending images',self.name, '|',other.name)
        # fetch the minimum size of the two imgs
        min_x = min(self.x, other.x)
        min_y = min(self.y, other.y)
        # resize both images to min_x, min_y
        im1 = self.resize((min_x, min_y))
        im2 = other.resize((min_x, min_y))
        return Image.blend(im1, im2, alpha)

    '''Color modification'''
    # remove red, green, blue respectively
    def apply(self,f):
        # applies a function on each pixel (rgb)
        img = self.getCopy()
        for x in range(self.x):
            for y in range(self.y):
                img.putpixel((x,y),f(img.getpixel((x,y))))
        return img

    def keepMax(self):
        # leaves only the dominant band in each pixel
        print ('~~The winner takes it allllllllllll~~')
        def f(x):
            _max = max(x)
            return tuple([(i if i == _max else 0) for i in x])
        return self.apply(f)

    def bw(self):
        print ('Making a B&W image')
        im = self.getCopy()
        return im.convert('1')

    '''Necessary getters/setters'''
    def getBlank(self, x, y):
        return Image.new('RGB',(x,y)) # background
        
    def getPixel(self, x, y):
        return self.image.getpixel((x, y))

    def setPixel(self, x, y, rgb):
        self.image.putpixel((x, y), rgb)

    def getCopy(self):
        # print('Generating a copy of', self.name)
        return self.image.copy()

    def getCenter(self):
        return (self.x / 2, self.y / 2)

    def getCentreTuple(self, other):
        # returns a quadtuple of x0,y0,x1,y1
        # used to place another image in the centre
        x0 = int(self.x / 2 - other.size[0] / 2)
        y0 = int(self.y / 2 - other.size[1] / 2)
        x1 = int(self.x / 2 + other.size[0] / 2)
        y1 = int(self.y / 2 + other.size[1] / 2)
        return (x0, y0, x1, y1)

    def getSize(self):
        return self.image.size

    def setImage(self, image, name='someNewImage.jpeg'):
        print('Updating image from', self.name, 'to', name)
        self.name = name
        self.image = image
        self.x = self.image.size[0]
        self.y = self.image.size[1]

    def getImage(self):
        return self.image

    '''Show, open and close'''
    def show(self):
        self.image.show()

    def open(self, file):
        print('Opening', self.name, end=' ')
        return Image.open(file)

    def close(self):
        print('Closing', self.name)
        self.image.close()

    '''Basic manipulations'''
    def rotate(self, degrees, zoom=False):
        print('Rotating', self.name, 'by', degrees, 'degrees')
        return self.image.rotate(degrees, expand=zoom)

    def resize(self, size=(150, 150)):
        # print('Resizing', self.name, 'from', self.image.size, 'to', size)
        return self.image.resize(size)

    def scale(self, percent):
        # print ('Scaling image to',round(100*percent),'%')
        x = int(self.x * percent)
        y = int(self.y * percent)
        return self.image.resize((x, y))

    def crop(self, x0, y0, x1, y1):
        return self.image.crop((x0, y0, x1, y1))

    def cropTopLeft(self, x, y):
        return self.crop(0, 0, x, y)

    def cropMiddle(self, x, y):
        halfX = self.x / 2
        halfY = self.y / 2
        _x, _y = x / 2, y / 2
        return self.crop(halfX - _x, halfY - _y, halfX + _x, halfY + _y)

    def square(self, size):
        # print('Creating a', size, 'x', size, 'square')
        _min = min(self.getSize())
        tmp = self.cropMiddle(_min, _min)
        return tmp.resize((size, size), Image.BILINEAR)
