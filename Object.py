import pygame
import random
from Entity import *

class Object(Entity):
    def __init__(self,rect,id,zindex):
        super().__init__(zindex) 
        self.id = id

        self.surf = pygame.image.load("assets/tiles/tile_"+self.id+".png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(topleft = (rect.x,rect.y))
        if self.id != "029_front" and self.id != "030_front" and self.id != "031_front" and self.id != "032_front" and self.id != "033_front" and self.id != "034_front" and self.id != "035_front" and self.id != "036_front":
            self.rect.y -=8
    
class Flower(Object):
    def __init__(self,rect,zindex):

        id = random.randint(41,45)
        idstr = "0"+str(id)

        super().__init__(rect,idstr,zindex) 
    
class Plant(Object):
    def __init__(self,rect,zindex,id):

        idstr = id+"_front"

        super().__init__(rect,idstr,zindex) 
    
class Wood(Object):
    def __init__(self,rect,zindex):

        id = random.randint(48,52)
        idstr = "0"+str(id)
        
        super().__init__(rect,idstr,zindex) 
    
class Rock(Object):
    def __init__(self,rect,zindex):

        id = random.randint(64,67)
        idstr = "0"+str(id)
        
        super().__init__(rect,idstr,zindex) 
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/tiles/rock_mask.png").convert_alpha())

class Tree(Entity):
    def __init__(self,rect,zindex):
        super().__init__(zindex) 

        self.surf = pygame.image.load("assets/tiles/tile_tree.png").convert_alpha()
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/tiles/tile_tree_mask.png").convert_alpha())
        self.rect = self.surf.get_rect(midbottom = rect.midbottom)