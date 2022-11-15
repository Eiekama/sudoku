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
    def __init__(self,label,left,top,width,height,
                 fill='black',border=None,borderWidth=0, align='left-top',
                 labelSize=12):
        self.label, self.labelSize = label, labelSize
        self.left, self.top, self.width, self.height = left, top, width, height
        self.fill, self.border, self.borderWidth, self.align = fill, border, borderWidth, align
        self.onClicked = Event()
    
    def AddListener(self,method):
        self.onClicked += method

    def RemoveListener(self,method):
        self.onClicked -= method

    def __eq__(self,other):
        return (isinstance(other,Button) and
                self.label == other.label and
                self.left == other.left and self.top == other.top and
                self.width == other.width and self.height == other.height and
                self.align == other.align)
    
    def __repr__(self):
        return f'Button({self.label},{self.left},{self.top},{self.width},{self.height})'
    
    def __hash__(self):
        return hash(str(self))
    
    def drawButton(self):
        drawRect(self.left, self.top, self.width, self.height,
                 fill=self.fill, border=self.border, borderWidth=self.borderWidth, align=self.align)
        if self.label != None:
            drawLabel(self.label,self.left, self.top,
                      size=self.labelSize,fill='black',align=self.align)
    
    def contains(self,x,y):
        if self.align == 'top-left':
            return (self.left<x<self.left+self.width and
                    self.top<y<self.top+self.height)
        elif self.align == 'center':
            return (self.left-0.5*self.width<x<self.left+0.5*self.width and
                    self.top-0.5*self.height<y<self.top+0.5*self.height)