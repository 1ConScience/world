import pygame
import random
from Util import *
from Entity import *

class Tile(Entity):
    def __init__(self,pos,zindex,value = None,topographic_value = None,specific_id = None):
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

        self.surf = IMAGES_DICT["tile_"+self.id+".png"].copy()
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

class Door(Entity):
    def __init__(self,key):
        centerx = key[0]
        centery = key[1]
        super().__init__(centery) 

        centerx*=TILE_SIZE
        centery*=TILE_SIZE4

        self.tiles = []
        self.tiles_for_collision = []

        for i in range(0,11,1):
            tile_bis = Tile((-TILE_SIZE+centerx,-TILE_SIZE4*i+centery),i-1+centery,specific_id = "061")
            self.tiles.append(tile_bis)
            if i <= 1 :
                self.tiles_for_collision.append(tile_bis)
        for i in range(0,11,1):
            tile_bis = Tile((TILE_SIZE+centerx,-TILE_SIZE4*i+centery),i-1+centery,specific_id = "061")
            self.tiles.append(tile_bis)
            if i <= 1 :
                self.tiles_for_collision.append(tile_bis)
            
        tile_bis = Tile((centerx,-TILE_SIZE4*9+centery),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

        tile_bis = Tile((centerx+TILE_SIZE2,-TILE_SIZE4*9+centery+TILE_SIZE4),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

        tile_bis = Tile((centerx-TILE_SIZE2,-TILE_SIZE4*9+centery+TILE_SIZE4),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

    def display(self,surf,camera):
        for tile in self.tiles:
            tile.display(surf,camera)
