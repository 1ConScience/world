import pygame
from Entity import *

class Text(pygame.sprite.Sprite):
    def __init__(self,txt,color,size,pos, font = 'Lucida Console'):
        super().__init__()  

        my_font = pygame.font.SysFont(font, size)
        self.surf = my_font.render(txt, True, color)
        self.rect = self.surf.get_rect(center = pos)

    def display(self,surf):
        surf.blit(self.surf, self.rect)


class AnimatedObject(Entity):
    def __init__(self,name,frames,freq,pos):
        super().__init__()  

        self.sheet = pygame.image.load("assets/"+name+".png").convert_alpha()

        self.w_frame = self.sheet.get_width() / frames
        self.h_frame = self.sheet.get_height()

        self.surf = self.sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.rect = self.surf.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.surf)

        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = freq #that define how many seconds or frames should pass before switching image.

        self.frames_number = frames

    def animate(self):
        self.surf = self.sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame += 1
            if self.index_frame >= self.frames_number :
                self.index_frame = 0