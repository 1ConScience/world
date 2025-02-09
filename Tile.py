import pygame
import random
from Util import *
from Entity import *

class Tile(Entity):
    def __init__(self,pos,value,zindex):
        super().__init__(zindex) 
        
        self.id_ = self.getId(value)

        '''value +=1
        value *=128
        value -=1
        self.surf = pygame.Surface((32,32))
        self.surf.fill((value,value,value))'''

        self.surf = pygame.image.load("assets/tiles/tile_"+self.id_+".png").convert_alpha()
        self.rect = self.surf.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/tiles/mask.png").convert_alpha())

        self.water = None
        if self.id_ == "104":
            self.water = AnimatedObject("tiles/water_animation",6,8,pos)
            self.surf = self.water.surf

    def getId(self,value):
        if value < -0.3 :
            luck = random.randint(0,10)
            if luck == 0 :
                return "068"
            else :
                return "104"
        elif value < -0.2 :
            id = random.randint(33,36)
            return "0"+str(id)
        elif value < -0.0 :
            id = random.randint(29,33)
            return "0"+str(id)
        elif value < 0.10 :
            id = random.randint(27,29)
            return "0"+str(id)
        elif value < 0.2 :
            id = random.randint(25,28)
            return "0"+str(id)
        elif value < 0.3 :
            id = random.randint(36,40)
            return "0"+str(id)
        elif value < 0.4 :
            id = random.randint(61,63)
            return "0"+str(id)
        else :
            id = random.randint(17,21)
            return "0"+str(id)

    #min -0.5382837653160095
    #max : 0.7629426717758179
    def getIdindev(self,value):
        if value < -0.30 :
            return "104"
        elif value < -0.25 :
            return "040"
        elif value < -0.20 :
            return "036"
        elif value < -0.15 :
            return "035"
        elif value < -0.10 :
            return "034"
        elif value < -0.05 :
            return "033"
        elif value < 0.00 :
            return "032"
        elif value < 0.05 :
            return "031"
        elif value < 0.10 :
            return "028"
        elif value < 0.15 :
            return "027"
        elif value < 0.20 :
            return "026"
        elif value < 0.25 :
            return "025"
        elif value < 0.30 :
            return "015"
        elif value < 0.35 :
            return "014"
        elif value < 0.40 :
            return "011"
        else :
            return "013"
        
    def animate(self):
        if self.id_ == "104":
            self.water.animate()
            self.surf = self.water.surf
