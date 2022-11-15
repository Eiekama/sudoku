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
    
    def contains(self,point):
        if self.align == 'top-left':
            return (self.left<point[0]<self.left+self.width and
                    self.top<point[1]<self.top+self.height)
        elif self.align == 'center':
            return (self.left-0.5*self.width<point[0]<self.left+0.5*self.width and
                    self.top-0.5*self.height<point[1]<self.top+0.5*self.height)

class Screen:
    id = 0

    def __init__(self,app):
        self.app = app
        self.buttons = set()
        self.id = Screen.id
        Screen.id += 1
    
    def drawScreen():
        pass

class StartScreen(Screen):
    def __init__(self,app):
        super().__init__(app)
        self.buttons = [
            Button('Start',200,200,80,50,fill='lavender',align='center',labelSize=25),
            Button('Help',200,270,80,50,fill='lavender',align='center',labelSize=25)
        ]
        self.buttons[0].AddListener(self.goToLevelSelectScreen)
        self.buttons[1].AddListener(self.goToHelpScreen)
    
    def goToLevelSelectScreen(self):
        self.app.currentScreen = self.app.screens[1]
    
    def goToHelpScreen(self):
        self.app.currentScreen = self.app.screens[2]

    def drawScreen(self):
            drawLabel('Sudoku',200,100,size=30,align='center')
            for button in self.buttons:
                button.drawButton()

class LevelSelectScreen(Screen):
    def __init__(self,app):
        super().__init__(app)
        self.buttons = [
            Button('Easy',200,50,90,35,fill='lavender',align='center',labelSize=24),
            Button('Medium',200,100,90,35,fill='lavender',align='center',labelSize=24),
            Button('Hard',200,150,90,35,fill='lavender',align='center',labelSize=24),
            Button('Expert',200,200,90,35,fill='lavender',align='center',labelSize=24),
            Button('Evil',200,250,90,35,fill='lavender',align='center',labelSize=24),
            Button('Manual',200,300,90,35,fill='lavender',align='center',labelSize=24),
            Button('Back',200,350,90,35,fill='lavender',align='center',labelSize=24),
        ]
        self.buttons[-1].AddListener(self.goToStartScreen)

    def goToStartScreen(self):
        print('test')
        self.app.currentScreen = self.app.screens[0]

    def drawScreen(self):
            for button in self.buttons:
                button.drawButton()

class HelpScreen(Screen):
    def __init__(self,app):
        super().__init__(app)
        self.buttons = [
            Button('Back',200,350,90,35,fill='lavender',align='center',labelSize=24),
        ]
        self.buttons[-1].AddListener(self.goToStartScreen)

    def goToStartScreen(self):
        print('test')
        self.app.currentScreen = self.app.screens[0]

    def drawScreen(self):
        drawLabel('insert helpful text here',200,150,size=20,align='center')
        for button in self.buttons:
            button.drawButton()

############################################

def onAppStart(app):
    app.screens = [None,None]
    app.screens = [StartScreen(app),LevelSelectScreen(app),HelpScreen(app)]
    app.currentScreen = app.screens[0]

def redrawAll(app):
    app.currentScreen.drawScreen()

def onMousePress(app,mouseX,mouseY):
    for button in app.currentScreen.buttons:
        if button.contains((mouseX,mouseY)):
            button.onClicked()

def main():
    runApp()

main()