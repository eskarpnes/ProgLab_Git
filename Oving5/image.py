from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import os

class Img():
    def __init__(self, file):
        self.name = os.path.basename(file)
        print (self.name)
        self.image = self.open(file)
        self.x, self.y = self.image.size
        print (self.image.size)
        
        
    '''Manipulations'''
    def makeSquare(self):
        long_side = max(self.image.size)
        hor = (long_side - self.x)/2
        ver = (long_side - self.y)/2
        return self.crop(-hor,-ver,hor+self.x,ver+self.y)
        
    # def zoom(self, levels=3, scale=0.75):
        # if levels == 0: return self
        # else:
            # next = self.scale(scale)
            # next.zoom(levels-1,scale)
            # xpos = round((1-scale)*self.x/2)
            # ypos = round((1-scale)*self.y/2)
            # self.paste(next,dx,dy)
            # return self
        
    def zoom(self, layers, scale, centre=False):
        steps = int(100/layers)
        zoomed = self.image.copy()
        for i in range(layers):
            smaller = self.scale(scale**(i+1))
            if centre:
                zoomed.paste(smaller, self.getCentreTuple(smaller))
            else:
                zoomed.paste(smaller,(0,0,smaller.size[0],smaller.size[1]))
        return zoomed
        
    '''End Manipulations'''

    '''Basic manipulations'''
    def rotate(self, degrees,zoom=False):
        return self.image.rotate(degrees,expand=zoom)
        
    def thumbnail(self, size=(150,150)):
        return self.image.thumbnail(size, Image.ANTIALIAS)
        
    def resize(self, size=(150,150)):
        print ('Resizing',self.name,'from',self.image.size,'to',size)
        return self.image.resize(size)
        
    def scale(self, percent):
        print ('Scaling image to',100*percent,'%')
        x = int(self.x * percent)
        y = int(self.y * percent)
        return self.image.resize((x,y))
                
    def crop(self, x0, y0, x1, y1):
        return self.image.crop((x0,y0,x1,y1))
    def cropTopLeft(self, x, y):
        return self.crop(0,0,x,y)
    def cropMiddle(self, x, y):
        halfX = self.x/2
        halfY = self.y/2
        _x,_y = x/2,y/2
        return self.crop(halfX-_x,halfY-_y,halfX+_x,halfY+_y)

    '''End basic manipulations'''
    
    '''Necessary getters/setters'''
    def getCentreTuple(self, other):
        # returns a quadtuple of x0,y0,x1,y1
        # used to place another image in the centre
        x0 = int(self.x / 2 - other.size[0] / 2)
        y0 = int(self.y / 2 - other.size[1] / 2)
        x1 = int(self.x / 2 + other.size[0] / 2)
        y1 = int(self.y / 2 + other.size[1] / 2)
        return (x0,y0,x1,y1)
        
    def getSize(self):
        return self.image.size
    
    def setImage(self, image):
        self.image = image
    
    def getImage(self):
        return self.image
        
    '''End getters/setters'''
    
    '''Show, open and close'''
    def show(self):
        self.image.show()
    def open(self, file):
        print ('Opening',self.name,end=' ')
        return Image.open(file)
    def close(self):
        print ('Closing',self.name)
        self.image.close()
    '''End of file'''