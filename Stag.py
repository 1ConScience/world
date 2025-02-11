from Animal import *

class Stag(Animal):
    def __init__(self,pos,game):
        super().__init__(game)  
        
        self.idle_right_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NE_idle.png").convert_alpha()
        self.idle_left_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NW_idle.png").convert_alpha()
        self.idle_left_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SW_idle.png").convert_alpha()
        self.idle_right_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SE_idle.png").convert_alpha()
        
        self.run_right_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NE_run.png").convert_alpha()
        self.run_left_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NW_run.png").convert_alpha()
        self.run_left_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SW_run.png").convert_alpha()
        self.run_right_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SE_run.png").convert_alpha()
        
        self.walk_right_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NE_walk.png").convert_alpha()
        self.walk_left_up_sheet = pygame.image.load("assets/animals/stag/critter_stag_NW_walk.png").convert_alpha()
        self.walk_left_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SW_walk.png").convert_alpha()
        self.walk_right_down_sheet = pygame.image.load("assets/animals/stag/critter_stag_SE_walk.png").convert_alpha()

        self.frames_number_idle = 24
        self.frames_number = 10

        self.w_frame = self.idle_right_up_sheet.get_width() / self.frames_number_idle
        self.h_frame = self.idle_right_up_sheet.get_height()

        self.surf = self.idle_right_up_sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/animals/stag/stag_mask.png").convert_alpha())

        self.pos = pos
        self.rect = self.surf.get_rect(midbottom = pos)

        self.index_frame_idle = 0 #that keeps track on the current index of the image list.
        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.

        self.running = False

    def animate(self):
        if self.vel == vec(0,0):
            self.idleAnimation()
        else:
            self.RunWalkAnimation()

    def idleAnimation(self):
        if self.last_dir == "right_up":
            self.surf = self.idle_right_up_sheet.subsurface((self.w_frame*self.index_frame_idle,0,self.w_frame,self.h_frame))
        elif self.last_dir == "left_up":
            self.surf = self.idle_left_up_sheet.subsurface((self.w_frame*self.index_frame_idle,0,self.w_frame,self.h_frame))
        elif self.last_dir == "left_down":
            self.surf = self.idle_left_down_sheet.subsurface((self.w_frame*self.index_frame_idle,0,self.w_frame,self.h_frame))
        elif self.last_dir == "right_down":
            self.surf = self.idle_right_down_sheet.subsurface((self.w_frame*self.index_frame_idle,0,self.w_frame,self.h_frame))

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame_idle += 1
            if self.index_frame_idle >= self.frames_number_idle :
                self.index_frame_idle = 0

    def RunWalkAnimation(self):
        if self.vel.x > 0 and self.vel.y < 0:
            self.surf = self.walk_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_up"
        elif self.vel.x < 0 and self.vel.y < 0:
            self.surf = self.walk_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_up"
        elif self.vel.x < 0 and self.vel.y > 0:
            self.surf = self.walk_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_down"
        elif self.vel.x > 0 and self.vel.y > 0:
            self.surf = self.walk_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_down"
        elif self.running and self.vel.x > 0 and self.vel.y < 0:
            self.surf = self.run_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_up"
        elif self.running and self.vel.x < 0 and self.vel.y < 0:
            self.surf = self.run_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_up"
        elif self.running and self.vel.x < 0 and self.vel.y > 0:
            self.surf = self.run_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_down"
        elif self.running and self.vel.x > 0 and self.vel.y > 0:
            self.surf = self.run_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_down"

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame += 1
            if self.index_frame >= self.frames_number :
                self.index_frame = 0