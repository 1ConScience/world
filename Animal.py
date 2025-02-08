import pygame
from Entity import *

class Animal(Entity):
    def __init__(self,name,frames,pos):
        super().__init__() 

        self.sheet = pygame.image.load("assets/animals/"+name+"_NE_idle.png").convert_alpha()

        self.w_frame = self.sheet.get_width() / frames
        self.h_frame = self.sheet.get_height()

        self.surf = self.sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.rect = self.surf.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.surf)

        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.

        self.frames_number = frames

    def animate(self):
        self.surf = self.sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame += 1
            if self.index_frame >= self.frames_number :
                self.index_frame = 0