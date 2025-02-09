from Tile import *
from Stag import *
from Object import *
import noise

nb_tiles_x = 22
nb_tiles_y = 48

class World:
    def __init__(self,game):
        self.game = game

        self.subworlds = {}

        self.actualsubworlds = {}
        self.addSubWorld(0,0)
        self.addSubWorld(nb_tiles_x,0)
        self.addSubWorld(0,nb_tiles_y)
        self.addSubWorld(nb_tiles_x,nb_tiles_y)

        self.actualtiles = []
        self.actualwater_group = pygame.sprite.Group()
        for cle, subworld in self.actualsubworlds.items():
            for tile in subworld.tiles:
                self.actualtiles.append(tile)
                if tile.id_ == "104" :
                    tile.add(self.actualwater_group)

        self.actualtiles.sort(key=lambda x: x.zindex, reverse=False)
        
    def addSubWorld(self,x,y):
        if str(x)+";"+str(y) not in self.actualsubworlds:
            self.actualsubworlds[str(x)+";"+str(y)] = SubWorld(self.game,x,y)

class SubWorld:
    def __init__(self,game,centerx,centery):
        self.game = game

        self.centerx = centerx
        self.centery = centery


        self.objects = []
        self.animals = []
        self.tiles = []
        self.add_elements(self.centerx-round(nb_tiles_x/2),self.centery-round(nb_tiles_y/2))

    def add_elements(self,start_x,start_y):
        end_x = start_x+nb_tiles_x
        end_y = start_y+nb_tiles_y
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
                    
                luck = random.randint(0,200)
                if luck == 0 :
                    self.add_animals((x*32,y*8))

    def add_animals(self,pos):
        animal = Stag(pos)
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
