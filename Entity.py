import pygame
from constvar import *

class Entity(pygame.sprite.Sprite):
    def __init__(self,zindex=0):
        super().__init__()  
        self.zindex = zindex
    
    def updateZindex(self):
        self.zindex = self.rect.bottom/TILE_SIZE4
        self.zindex -= 1.5
    def animate(self):
        pass

    def display(self,surf,camera):
        self.animate()
        surf.blit(self.surf, (self.rect.x - camera.x, self.rect.y - camera.y))