from commands import *
import math, pygame

MAP_SCALE_FACTOR = 10
SCREEN_SIZE = (800, 800)
STARTX = SCREEN_SIZE[0] / 2
STARTY = SCREEN_SIZE[1] / 2

class GenerateMap:
    def __init__(self):
        self.x = STARTX
        self.y = STARTY
        self.pointX = []
        self.pointY = []
        self.bearing = 0

        pygame.init()
        screen_size = SCREEN_SIZE
        self.screen = pygame.display.set_mode(screen_size)
        self.background = pygame.Surface(self.screen.get_size()) 
        self.Update()  
        
    def GetX(self):
        return self.x * MAP_SCALE_FACTOR

    def GetY(self):
        return self.y * MAP_SCALE_FACTOR

    def GetDirection(self):
        return self.bearing

    def GetMapScale(self):
        return MAP_SCALE_FACTOR

    def SetX(self, x):
        self.x = x

    def SetY(self, y):
        self.y = y

    def SetDirection(self, bearing):
        self.bearing = bearing

    def AddPoint(self, x, y):
        self.pointX.append(x)
        self.pointY.append(y)
        
    def Update(self):
        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen, (255,0,0), (self.x, self.y, 10, 10), 0)       
        for i in range(len(self.pointX)):
            self.screen.set_at((int(self.pointX[i])/10, int(self.pointY[i])/10), (0, 0, 255))
        pygame.display.flip()   

    def Run(self):
        for i in range(10):                 
            self.Scan(False)
            self.Update()  
            #self.Forward(10)
            #self.Left(90)
            #self.Scan(False)  
            #self.Update()    


        
