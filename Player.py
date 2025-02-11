import pygame
from Entity import *
from constvar import *
from Animal import *

class Player(Animal):
    def __init__(self,game):
        super().__init__(game) 
        
        self.idle_right_up_sheet = pygame.image.load("assets/character/Idle/idle_right_up.png").convert_alpha()
        self.idle_up_sheet = pygame.image.load("assets/character/Idle/idle_up.png").convert_alpha()
        self.idle_left_up_sheet = pygame.image.load("assets/character/Idle/idle_left_up.png").convert_alpha()
        self.idle_left_down_sheet = pygame.image.load("assets/character/Idle/idle_left_down.png").convert_alpha()
        self.idle_down_sheet = pygame.image.load("assets/character/Idle/idle_down.png").convert_alpha()
        self.idle_right_down_sheet = pygame.image.load("assets/character/Idle/idle_right_down.png").convert_alpha()
        
        self.walk_right_up_sheet = pygame.image.load("assets/character/Walk/walk_right_up.png").convert_alpha()
        self.walk_up_sheet = pygame.image.load("assets/character/Walk/walk_up.png").convert_alpha()
        self.walk_left_up_sheet = pygame.image.load("assets/character/Walk/walk_left_up.png").convert_alpha()
        self.walk_left_down_sheet = pygame.image.load("assets/character/Walk/walk_left_down.png").convert_alpha()
        self.walk_down_sheet = pygame.image.load("assets/character/Walk/walk_down.png").convert_alpha()
        self.walk_right_down_sheet = pygame.image.load("assets/character/Walk/walk_right_down.png").convert_alpha()

        self.frames_number = 8

        self.w_frame = self.idle_right_up_sheet.get_width() / self.frames_number
        self.h_frame = self.idle_right_up_sheet.get_height()

        self.surf = self.idle_right_up_sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.shadow = pygame.image.load("assets/character/ShadowBetter.png").convert_alpha()
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/character/mask.png").convert_alpha())
        
        self.rect = self.surf.get_rect(midbottom = self.pos)

        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.

    def animate(self):
        if self.vel.x == 0 and self.vel.y == 0:
            if self.last_dir == "right":
                self.surf = self.idle_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "right_up":
                self.surf = self.idle_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "up":
                self.surf = self.idle_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left_up":
                self.surf = self.idle_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left":
                self.surf = self.idle_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left_down":
                self.surf = self.idle_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "down":
                self.surf = self.idle_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "right_down":
                self.surf = self.idle_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
        elif self.vel.x > 0 and self.vel.y == 0:
            self.surf = self.walk_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right"
        elif self.vel.x > 0 and self.vel.y < 0:
            self.surf = self.walk_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_up"
        elif self.vel.x == 0 and self.vel.y < 0:
            self.surf = self.walk_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "up"
        elif self.vel.x < 0 and self.vel.y < 0:
            self.surf = self.walk_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_up"
        elif self.vel.x < 0 and self.vel.y == 0:
            self.surf = self.walk_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left"
        elif self.vel.x < 0 and self.vel.y > 0:
            self.surf = self.walk_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_down"
        elif self.vel.x == 0 and self.vel.y > 0:
            self.surf = self.walk_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "down"
        elif self.vel.x > 0 and self.vel.y > 0:
            self.surf = self.walk_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_down"

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame += 1
            if self.index_frame >= self.frames_number :
                self.index_frame = 0

    def display(self,surf,camera):
        surf.blit(self.shadow, (self.rect.x - camera.x, self.rect.y - camera.y))
        surf.blit(self.surf, (self.rect.x - camera.x, self.rect.y - camera.y))