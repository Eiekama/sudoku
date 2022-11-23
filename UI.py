from cmu_cs3_graphics import *

class Event(object): # taken from https://www.geeksforgeeks.org/mimicking-events-python/
 
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)

class Button:
    def __init__(self,image,cx,cy,scale=None):
        self.image = image
        self.cx, self.cy = cx, cy
        if scale == None:
            self.width = image.image.width
            self.height = image.image.height
        else:
            self.width = image.image.width * scale
            self.height = image.image.height * scale
        self.onClicked = Event()

    def AddListener(self,method):
        self.onClicked += method

    def RemoveListener(self,method):
        self.onClicked -= method

    def __eq__(self,other):
        return (isinstance(other,Button) and
                self.cx == other.cx and self.cy == other.cy and
                self.width == other.width and self.height == other.height)
    
    def __repr__(self):
        return f'Button({self.cx},{self.cy},{self.width},{self.height})'
    
    def __hash__(self):
        return hash(str(self))
    
    def drawButton(self):
        drawImage(self.image, self.cx, self.cy, align='center',
                  width=self.width, height=self.height)
    
    def contains(self,x,y):
        return (self.cx-0.5*self.width < x < self.cx+0.5*self.width and
                self.cy-0.5*self.height < y < self.cy+0.5*self.height)