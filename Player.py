import pygame
from Entity import *
from constvar import *
from Animal import *
from Tile import *

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
        self.surf_shadow = pygame.image.load("assets/character/ShadowBetter.png").convert_alpha()
        self.surf_tile_selected = pygame.image.load("assets/tiles/tile_061.png").convert_alpha()
        self.surf_tile_selected = pygame.transform.scale(self.surf_tile_selected,(self.surf_tile_selected.get_width()/3,self.surf_tile_selected.get_height()/3))
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/character/mask.png").convert_alpha())

        self.pos.y -=TILE_SIZE4
        self.rect = self.surf.get_rect(center = self.pos)

        self.index_frame = 0 #that keeps track on the current index of the image list.
        self.current_frame = 0 #that keeps track on the current time or current frame since last the index switched.
        self.animation_frames = 8 #that define how many seconds or frames should pass before switching image.

        self.mouse_frames_cpt = 0

    def getKeyStrSubWorld(self):
        return str(self.actualsubworld[0])+";"+str(self.actualsubworld[1])

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

        if newsubworldkey != None:
            print(newsubworldkey)
        return newsubworldkey
    
    def getTileUnderPlayer(self):
        subworld = self.game.world.subworlds[self.getKeyStrSubWorld()]
        for tile in subworld.tiles:
            if pygame.sprite.collide_mask(self, tile):
                return tile
    
    def action(self):
        pressed_mouse_buttons = pygame.mouse.get_pressed(num_buttons=5)
        if pressed_mouse_buttons[2] or pressed_mouse_buttons[3] or pressed_mouse_buttons[4]:
            if self.mouse_frames_cpt == 0:
                subworld_tmp = self.game.world.subworlds[self.getKeyStrSubWorld()]
                tile = self.getTileUnderPlayer()
                if tile != None :
                    if pressed_mouse_buttons[2]:
                        subworld_tmp.addTile(tile)
                    if pressed_mouse_buttons[4]:
                        subworld_tmp.removeTile(tile)
                    if pressed_mouse_buttons[3]:
                        subworld_tmp.removeTile(tile,order_remove_reversed=True)

            self.mouse_frames_cpt +=1

        if self.mouse_frames_cpt > 10: 
            self.mouse_frames_cpt = 0

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
            

        dict_collision_actualrock = self.checkCollide(self.game.world.actualrock_group)
        if dict_collision_actualrock :
            sprite = dict_collision_actualrock[0]
            sprite.kill()
            if sprite in self.game.world.subworlds[self.getKeyStrSubWorld()].rocks :
                self.game.world.subworlds[self.getKeyStrSubWorld()].rocks.remove(sprite)

        dict_collision_actualwood = self.checkCollide(self.game.world.actualwood_group)
        if dict_collision_actualwood :
            sprite = dict_collision_actualwood[0]
            sprite.kill()
            if sprite in self.game.world.subworlds[self.getKeyStrSubWorld()].woods :
                self.game.world.subworlds[self.getKeyStrSubWorld()].woods.remove(sprite)

        dict_collision_actualflower = self.checkCollide(self.game.world.actualflower_group)
        if dict_collision_actualflower :
            sprite = dict_collision_actualflower[0]
            sprite.kill()
            if sprite in self.game.world.subworlds[self.getKeyStrSubWorld()].flowers :
                self.game.world.subworlds[self.getKeyStrSubWorld()].flowers.remove(sprite)


        if self.checkCollide(self.game.world.actualinoffensiveanimal_group) or self.checkCollide(self.game.world.actualtree_group) :
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

        surf.blit(self.surf_shadow, (self.rect.x - camera.x, self.rect.y - camera.y))
        surf.blit(self.surf, (self.rect.x - camera.x, self.rect.y - camera.y))
        surf.blit(self.surf_tile_selected, (self.rect.x - camera.x + 19, self.rect.y - camera.y + 32))
