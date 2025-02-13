import pygame
import random
from Util import *
from Entity import *

class Tile(Entity):
    def __init__(self,pos,value,zindex,specific_id = None):
        super().__init__(zindex) 
        
        if specific_id != None :
            self.id_ = specific_id
        else :
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
            self.water = AnimatedObject("tiles/water_animation",6,12,pos)
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
        
    def animate(self):
        if self.id_ == "104":
            self.water.animate()
            self.surf = self.water.surf

class Door():
    def __init__(self,centerx,centery):
        self.tiles = []
        for i in range(1,10,1):
            tile_bis = Tile((-TILE_SIZE*2+centerx,-TILE_SIZE4*i+centery),0,1*i,"063")
            self.tiles.append(tile_bis)
        for i in range(1,10,1):
            tile_bis = Tile((TILE_SIZE*2+centerx,-TILE_SIZE4*i+centery),0,1*i,"063")
            self.tiles.append(tile_bis)
        for i in range(-1,2,1):
            tile_bis = Tile((TILE_SIZE*i+centerx,-TILE_SIZE4*9+centery),0,1*i,"063")
            self.tiles.append(tile_bis)

    def display(self,surf,camera):
        for tile in self.tiles:
            tile.display(surf,camera)
