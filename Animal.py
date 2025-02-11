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

        self.actualsubworld = (0,0)

    def testNewSubworldkey(self):
        newsubworldkey = None

        if self.pos.x > self.actualsubworld[0]*TILE_SIZE + (TILES_WIDTH2)*TILE_SIZE :
            self.actualsubworld = (self.actualsubworld[0]+TILES_WIDTH,self.actualsubworld[1])
            newsubworldkey = self.actualsubworld
        if self.pos.x < self.actualsubworld[0]*TILE_SIZE - (TILES_WIDTH2)*TILE_SIZE :
            self.actualsubworld = (self.actualsubworld[0]-TILES_WIDTH,self.actualsubworld[1])
            newsubworldkey = self.actualsubworld
        if self.pos.y > self.actualsubworld[1]*TILE_SIZE4 + (TILES_HEIGHT2)*(TILE_SIZE4) :
            self.actualsubworld = (self.actualsubworld[0],self.actualsubworld[1]+TILES_HEIGHT)
            newsubworldkey = self.actualsubworld
        if self.pos.y < self.actualsubworld[1]*TILE_SIZE4 - (TILES_HEIGHT2)*(TILE_SIZE4) :
            self.actualsubworld = (self.actualsubworld[0],self.actualsubworld[1]-TILES_HEIGHT)
            newsubworldkey = self.actualsubworld

        return newsubworldkey

    def checkCollide(self,group):
        collide = pygame.sprite.spritecollide(self, group, False, collided = pygame.sprite.collide_mask)
        if collide :
            return True
        return False

    def move(self):
        self.vel = vec(0,0)

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