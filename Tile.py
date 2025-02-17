import pygame
import random
from Util import *
from Entity import *

class Tile(Entity):
    def __init__(self,pos,zindex,value = None,specific_id = None):
        super().__init__(zindex) 
        
        if value != None :
            self.id = self.getId(value)
        if specific_id != None :
            self.id = specific_id

        self.pos = pos

        '''value +=1
        value *=128
        value -=1
        self.surf = pygame.Surface((32,32))
        self.surf.fill((value,value,value))'''

        self.surf = IMAGES_DICT["tile_"+self.id+".png"]
        self.rect = self.surf.get_rect(center = self.pos)
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/tiles/mask.png").convert_alpha())

        self.water = None
        if self.id == "104":
            self.water = AnimatedObject("tiles/water_animation",6,12,pos)
            self.surf = self.water.surf
            self.rect.y += TILE_SIZE4+1

        if value != None :
            self.topography(value)

    def topography(self,value):
        if value > 0.3 :
            self.rect.y += TILE_SIZE4

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
            id = random.randint(61,62)
            return "0"+str(id)
        else :
            id = random.randint(17,21)
            return "0"+str(id)
        
    def animate(self):
        if self.id == "104":
            self.water.animate()
            self.surf = self.water.surf
