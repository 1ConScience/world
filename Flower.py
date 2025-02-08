import pygame
import random
from Entity import *

class Flower(Entity):
    def __init__(self,rect):
        super().__init__() 
        self.id_ = self.getId()

        self.surf = pygame.image.load("assets/tiles/tile_"+self.id_+".png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(topleft = (rect.x,rect.y))
        self.rect.y -=8

    def getId(self):
        id = random.randint(41,44)
        return "0"+str(id)