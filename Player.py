import pygame
from Entity import *
from constvar import *
from Animal import *

class Player(Animal):
    def __init__(self,game):
        super().__init__(game) 

        self.offset_zindex = 1.5

        main_sheet = pygame.image.load("assets/character/main_sheet.png").convert_alpha()
        w_frame_pre = main_sheet.get_width()
        h_frame_pre = main_sheet.get_height() / 16

        tab_sheet = []
        for i in range(16):
            surf_tmp = main_sheet.subsurface((0,h_frame_pre*i,w_frame_pre,h_frame_pre))
            tab_sheet.append(surf_tmp)

        self.walk_down_sheet = tab_sheet[0]
        self.walk_left_down_sheet = tab_sheet[1]
        self.walk_left_up_sheet = tab_sheet[2]
        self.walk_up_sheet = tab_sheet[3]
        self.walk_right_up_sheet = tab_sheet[4]
        self.walk_right_down_sheet = tab_sheet[5]
        self.walk_left_sheet = tab_sheet[6]
        self.walk_right_sheet = tab_sheet[7]

        self.idle_down_sheet = tab_sheet[8]
        self.idle_left_down_sheet = tab_sheet[9]
        self.idle_left_up_sheet = tab_sheet[10]
        self.idle_up_sheet = tab_sheet[11]
        self.idle_right_up_sheet = tab_sheet[12]
        self.idle_right_down_sheet = tab_sheet[13]
        self.idle_left_sheet = tab_sheet[14]
        self.idle_right_sheet = tab_sheet[15]

        self.frames_number = 8

        self.w_frame = self.idle_right_up_sheet.get_width() / self.frames_number
        self.h_frame = self.idle_right_up_sheet.get_height()

        self.surf = self.idle_right_up_sheet.subsurface((0,0,self.w_frame,self.h_frame))
        self.shadow = pygame.image.load("assets/character/ShadowBetter.png").convert_alpha()
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/character/mask.png").convert_alpha())

        self.pos.y -=TILE_SIZE4
        self.rect = self.surf.get_rect(center = self.pos)

        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.

        self.mouse_free = True

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
    
    def getBlockPos(self):


        x = self.pos.x/TILE_SIZE
        y = self.pos.y/TILE_SIZE4

        x -= 0.5
        y += 1.5

        pos = (round(x),round(y))
        return pos
    
    def action(self):
        print(self.getBlockPos())
        pressed_mouse_buttons = pygame.mouse.get_pressed()
        if pressed_mouse_buttons[0]:

            if self.mouse_free:
        
                pos_tmp = self.getBlockPos()
                subworld_tmp = self.game.world.subworlds[str(self.actualsubworld[0])+";"+str(self.actualsubworld[1])]
                subworld_tmp.addBlock(pos_tmp[0],pos_tmp[1])

                self.mouse_free = False

        else :
            self.mouse_free = True

    def move(self):
        self.vel = vec(0,0)

        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[pygame.K_z] or pressed_keys[pygame.K_UP]:
            self.vel.y = -1
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.vel.y = 1
        if pressed_keys[pygame.K_q] or pressed_keys[pygame.K_LEFT]:
            self.vel.x = -1
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.vel.x = 1
        
        if self.vel != vec(0,0):
            pygame.math.Vector2.scale_to_length(self.vel, VELOCITY)

        self.pos += self.vel

        self.rect.center = self.pos 
            
        if self.checkCollide(self.game.world.actualwater_group):
            self.pos -= self.vel*0.5
            self.rect.center = self.pos 
            
        if self.checkCollide(self.game.world.actualinoffensiveanimal_group) or self.checkCollide(self.game.world.actualrock_group) or self.checkCollide(self.game.world.actualwood_group) :
            self.pos -= self.vel
            self.rect.center = self.pos 

        self.updateZindex()

    def animate(self):
        if self.vel.x == 0 and self.vel.y == 0:
            if self.last_dir == "right":
                self.surf = self.idle_right_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "right_up":
                self.surf = self.idle_right_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "up":
                self.surf = self.idle_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left_up":
                self.surf = self.idle_left_up_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left":
                self.surf = self.idle_left_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "left_down":
                self.surf = self.idle_left_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "down":
                self.surf = self.idle_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
            elif self.last_dir == "right_down":
                self.surf = self.idle_right_down_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
        elif self.vel.x > 0 and self.vel.y == 0:
            self.surf = self.walk_right_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
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
            self.surf = self.walk_left_sheet.subsurface((self.w_frame*self.index_frame,0,self.w_frame,self.h_frame))
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

        self.animate()

        surf.blit(self.shadow, (self.rect.x - camera.x, self.rect.y - camera.y))
        surf.blit(self.surf, (self.rect.x - camera.x, self.rect.y - camera.y))