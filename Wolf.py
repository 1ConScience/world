from Animal import *

class Wolf(Animal):
    def __init__(self,pos,game,centerx,centery):
        super().__init__(game)  
        
        self.actualsubworld = (centerx,centery)

        self.idle_sheet = pygame.image.load("assets/animals/wolf/wolf-idle.png").convert_alpha()
        pre_h_frame = self.idle_sheet.get_height()/4
        self.idle_left_down_sheet = self.idle_sheet.subsurface((0,0,self.idle_sheet.get_width(),pre_h_frame))
        self.idle_right_down_shee = self.idle_sheet.subsurface((0,pre_h_frame,self.idle_sheet.get_width(),pre_h_frame))
        self.idle_left_up_sheet = self.idle_sheet.subsurface((0,pre_h_frame*2,self.idle_sheet.get_width(),pre_h_frame))
        self.idle_right_up_sheet = self.idle_sheet.subsurface((0,pre_h_frame*3,self.idle_sheet.get_width(),pre_h_frame))
        
        self.run_sheet = pygame.image.load("assets/animals/wolf/wolf-run.png").convert_alpha()
        self.run_left_down_sheet = self.run_sheet.subsurface((0,0,self.run_sheet.get_width(),pre_h_frame))
        self.run_right_down_shee = self.run_sheet.subsurface((0,pre_h_frame,self.run_sheet.get_width(),pre_h_frame))
        self.run_left_up_sheet = self.run_sheet.subsurface((0,pre_h_frame*2,self.run_sheet.get_width(),pre_h_frame))
        self.run_right_up_sheet = self.run_sheet.subsurface((0,pre_h_frame*3,self.run_sheet.get_width(),pre_h_frame))
        
        self.frames_number_idle = 4
        self.frames_number = 8

        self.w_frame = self.idle_right_up_sheet.get_width() / self.frames_number_idle
        self.h_frame = self.idle_right_up_sheet.get_height()

        self.surf = self.idle_right_up_sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/animals/wolf/wolf_mask.png").convert_alpha())

        self.pos = pos
        self.rect = self.surf.get_rect(midbottom = pos)

        self.index_frame_idle = 0 #that keeps track on the current index of the image list.
        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.


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
            self.surf = self.run_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_up"
        elif self.vel.x < 0 and self.vel.y < 0:
            self.surf = self.run_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_up"
        elif self.vel.x < 0 and self.vel.y > 0:
            self.surf = self.run_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "left_down"
        elif self.vel.x > 0 and self.vel.y > 0:
            self.surf = self.run_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            self.last_dir = "right_down"

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index_frame += 1
            if self.index_frame >= self.frames_number :
                self.index_frame = 0