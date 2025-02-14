import pygame
import random
from Entity import *

class Object(Entity):
    def __init__(self,rect,id,zindex):
        super().__init__(zindex) 
        self.id_ = id

        self.surf = pygame.image.load("assets/tiles/tile_"+self.id_+".png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(topleft = (rect.x,rect.y))
        self.rect.y -=8
    
class Flower(Object):
    def __init__(self,rect,zindex):

        id = random.randint(41,44)
        id_str = "0"+str(id)

        super().__init__(rect,id_str,zindex) 
    
class Wood(Object):
    def __init__(self,rect,zindex):

        id = random.randint(48,52)
        id_str = "0"+str(id)
        
        super().__init__(rect,id_str,zindex) 
    
class Rock(Object):
    def __init__(self,rect,zindex):

        id = random.randint(64,65)
        id_str = "0"+str(id)
        
        super().__init__(rect,id_str,zindex) 
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/tiles/rock_mask.png").convert_alpha())