from Tile import *
from Stag import *
from Object import *
import noise

nb_tiles_x = 28
nb_tiles_y = 61

class World:
    def __init__(self,game):
        self.game = game

        self.objects = []

        self.animals = []
        self.add_animals()

        self.tiles = []
        self.add_tiles(0,0,nb_tiles_x,nb_tiles_y)
        self.topincognita = 0-1
        self.bottomincognita = nb_tiles_y
        self.leftincognita = 0-1
        self.rightincognita = nb_tiles_x

    def expand(self):
        if self.game.player.pos.x > self.rightincognita*32 - (nb_tiles_x/2)*32 :
            self.add_tiles(self.rightincognita,0,1,nb_tiles_y)
            self.rightincognita +=1

        if self.game.player.pos.y > self.bottomincognita*8 - (nb_tiles_y/2)*8 :
            self.add_tiles(0,self.bottomincognita,nb_tiles_x,1)
            self.bottomincognita +=1

        if self.game.player.pos.x < self.leftincognita*32 + (nb_tiles_x/2)*32 :
            self.add_tiles(self.leftincognita,0,1,nb_tiles_y)
            self.leftincognita -=1

        if self.game.player.pos.y < self.topincognita*8 + (nb_tiles_y/2)*8 :
            self.add_tiles(0,self.topincognita,nb_tiles_x,1)
            self.topincognita -=1

    def add_tiles(self,start_x,start_y,range_x,range_y):
        end_x = start_x+range_x
        end_y = start_y+range_y
        scale = 13
        octaves = 7
        lacunarity = 1.0
        persistence = 1.0
        for y in range (start_y,end_y,1):
            for x in range(start_x,end_x,1):
                value = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeatx=end_x,repeaty=end_y,base=0)
                tile = None
                if y%2 == 0:
                    tile = Tile((x*32,y*8),value,y)
                else :
                    tile = Tile((x*32+16,y*8),value,y)
                self.tiles.append(tile)
                
                if tile.id_ == "040" :
                    luck = random.randint(0,2)
                    if luck == 0 :
                        self.add_flower(tile.rect)
                elif tile.id_ == "028" :
                    luck = random.randint(0,10)
                    if luck == 0 :
                        self.add_wood(tile.rect)
                elif tile.id_ == "063" :
                    luck = random.randint(0,10)
                    if luck == 0 :
                        self.add_rock(tile.rect)
                elif tile.id_ == "104" :
                    tile.add(self.game.water_group)

        self.tiles.sort(key=lambda x: x.zindex, reverse=False)

    def add_animals(self):
        for i in range(3):
            animal = Stag((random.randint(0,self.game.w_),random.randint(0,self.game.h_)))
            self.animals.append(animal)

    def add_flower(self,pos):
        flower = Flower(pos)
        self.objects.append(flower)

    def add_wood(self,pos):
        wood = Wood(pos)
        self.objects.append(wood)

    def add_rock(self,pos):
        rock = Rock(pos)
        self.objects.append(rock)
