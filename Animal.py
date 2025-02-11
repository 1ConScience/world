import pygame
from Entity import *
import random

class Animal(Entity):
    def __init__(self,game):
        super().__init__() 
        self.game = game 
        self.pos = vec(0,0)
        self.vel = vec(0,0)        
        
        list_dir = ["right_up","right_down","left_up","left_down"]
        self.last_dir = random.choice(list_dir)

    def checkCollide(self,group):
        collide = pygame.sprite.spritecollide(self, group, False, collided = pygame.sprite.collide_mask)
        if collide :
            return True
        return False

    def move(self):
        self.control()#toujours avoir du self control
        
        if self.vel != vec(0,0):
            pygame.math.Vector2.scale_to_length(self.vel, VELOCITY)

        self.pos += self.vel

        self.rect.midbottom = self.pos 
            
        if self.checkCollide(self.game.world.actualwater_group):
            self.pos -= self.vel*0.5
            self.rect.midbottom = self.pos 
            
        if self.checkCollide(self.game.world.actualcollide_group):
            self.pos -= self.vel
            self.rect.midbottom = self.pos 

        self.updateZindex()

    def control(self):
        pass