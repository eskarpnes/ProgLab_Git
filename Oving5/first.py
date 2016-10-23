'''
open an image. this should be the handle for all manipulations:
img = Image.open(filepath)
'''
from PIL import Image, ImageEnhance

class Img():
    pix_colors = {
        'r': (255,0,0),
        'g': (0,255,0),
        'b': (0,0,255),
        'white': (255,255,255),
        'black': (0,0,0)
    }
    
    def __init__(self,_file=False,image=False,_w=100,_h=100,_bg='black',_mode='RGB'):
        print 'Got file',_file
        self._file = _file
        self.image = image
        self.x = _w
        self.y = _h
        self.mode = _mode
        self.init_img(_bg)
        
    def init_img(self, bg='black'):
        print 'Initializing image...'
        if self._file:
            self.load_img()
        if self.image:
            self.get_image_size()
        else:
            self.image = self.plain_image(self.x, self.y, bg)
    
    def load_img(self):
        print 'Loading image'
        self.image = Image.open(self._file)
        if self.image.mode != self.mode:
            self.image = self.image.convert(self.mode)
            # translates to rgb mode
            
    def save_img(self, name='default', type='jpg'):
        print 'Saving image'
        file_name = name.strip().replace(' ','')
        self.image.save(file_name+'.'+type, format=type)
        
    def get_image_size(self):
        print 'Fetching image dimensions'
        self.x = self.image.size[0]
        self.y = self.image.size[1]
        
    def plain_image(self, w, h, bg, mode='RGB'):
        print 'Creating a blank image'
        return Image.new(mode, (w,h), self.get_color(bg))
    
    def get_color(self, color_name):
        print 'Fetching the RBG value for', color_name
        # makes sure the color_input isn't invalid, e.g. "yellow"
        if color_name not in Img.pix_colors:
            color_name = 'black'
        return Img.pix_colors[color_name]
        
    def resize(self, new_w, new_h):
        print 'Resizing image to',new_w, 'x',new_h
        return Img(image=self.image.resize((new_w,new_h)))
        
    def scale(self, xfac, yfac):
        print 'Scaling image by',xfac,'x',yfac
        return self.resize(round(xfac*self.x),round(yfac*self.y))
        
    def equalize_sizes(self, new_img):
        low_x = min(self.x, new_img.x)
        low_y = min(self.y, new_img.y)
        print 'Equalizing with size:',low_x,'x',low_y
        # return both images at same size
        tmp_1 = self.resize(low_x, low_y)
        tmp_2 = new_img.resize(low_x, low_y)
        self.set_image(tmp_1)
        new_img.set_image(tmp_2)
        # return self.image.thumbnail(low_x,low_y), new_img.image.thumbnail(low_x,low_y)
        
    
    # simple getters and setters, as well as display
    def get_image(self):
        print 'Getting image...'
        return self.image
        
    def set_image(self, img):
        print 'Setting image...'
        self.image = img
    
    def display(self):
        print 'Showing image'
        self.image.show()
        
    def get_pixel(self, x, y):
        try:
            return self.image.getpixel((x,y))
        except:
            pass
        
    def set_pixel(self, x, y, rgb):
        # rgb = (r,g,b)
        # print (rgb)
        # rgb = (int(x) for x in rgb)
        # print (rgb)
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        self.image.putpixel((x,y),(r,g,b))
        
    def combine_pixels(self, p1, p2, a=0.5):
        # alpha 0.5 for average color if nothing else specified
        return tuple([round(a*p1[i] + (1-a)*p2[i]) for i in range(len(p1))])
        
    def map_band(self, f):
        print 'Mapping the RGB bands'
        # eval applies the function f to all bands of a pixel
        return Img(image=Image.eval(self.image, f))
        
    def map_tuple(self, f):
        print 'Mapping the color tuples'
        img2 = self.image.copy()
        for x in range(self.x):
            for y in range(self.y):
                img2.putpixel((x,y),f(img2.getpixel((x,y))))
        return Img(_image = img2)
    
    def map_maxvalue(self):
        print 'Keeping only the highest color value'
        def high_value(pixel):  # is passed as 'f' in map_tuple
            return tuple([(band if band == max(pixel) else 0) for band in pixel])
        return self.map_tuple(high_value)
        
    def scale_colors(self, degree=0.5):
        return Img(image=ImageEnchance.Color(self.image).enhance(degree))
     
    def grayscale(self):
        return self.scale_colors(degree = 0)
        
    def paste(self, new_img, x0=0,y0=0):
        self.get_image().paste(new_img.get_image(),
                        (x0,y0,
                        x0+new_img.x,y0+new_img.y))
                        
    def concat_v(self, new_img=False, bg='black'):
        new_img = new_img if new_img else self
        concat = Img()
        concat.x = max(self.x, new_img.x)   # velger den storste av x-verdiene
        concat.y = self.y + new_img.y       # legger sammen hoyden
        concat.image = concat.plain_image(concat.x, concat.y, bg)
        concat.paste(self,0,0)
        concat.paste(new_img,0,self.y)
        return concat
        
    def concat_h(self, new_img=False, bg='black'):
        new_img = new_img if new_img else self
        concat = Img()
        concat.x = self.x + new_img.x
        concat.y = max(self.y, new_img.y)
        concat.image = concat.plain_image(concat.x, concat.y, bg)
        concat.paste(self,0,0)
        concat.paste(new_img, self.x, 0)
        return concat
        
    def morph(self, new_img, a=0.5):
        # alpha = 0.5 as default
        morphed = Img(_w=self.x, _h=self.y)  # plain image of size x,y
        for x in range(self.x):
            for y in range(self.y):
                rgb = self.combine_pixels(self.get_pixel(x,y), new_img.get_pixel(x,y), a=a)
                morphed.set_pixel(x,y,rgb)
        return morphed
        
    def morph_square(self, new_img):
        morphed_1 = self.morph(new_img, a=0.66)
        morphed_2 = self.morph(new_img, a=0.33)
        return self.concat_h(morphed_1).concat_v(morphed_2.concat_h(new_img))
        
    def blend(self, new_img):
        self.equalize_sizes(new_img)
        return Image.blend(self.image, new_img.image, 0.5)