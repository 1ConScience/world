from Tile import *
from Stag import *
from Object import *
import noise
from constvar import *

class World:
    def __init__(self,game):
        self.game = game

        self.subworlds = {}
        self.genWorld()

        self.actualsubworlds = {}
        self.actualtiles = []
        self.actualwater_group = pygame.sprite.Group()

        self.updateActualSubworlds((0,0))

    def genWorld(self):
        #gen first zone
        self.addSubWorld(0,0)

        self.addSubWorld(TILES_WIDTH,0)
        self.addSubWorld(0,TILES_HEIGHT)
        self.addSubWorld(TILES_WIDTH,TILES_HEIGHT)

        self.addSubWorld(-TILES_WIDTH,0)
        self.addSubWorld(0,-TILES_HEIGHT)
        self.addSubWorld(-TILES_WIDTH,-TILES_HEIGHT)

        self.addSubWorld(TILES_WIDTH,-TILES_HEIGHT)
        self.addSubWorld(-TILES_WIDTH,TILES_HEIGHT)

        #gen second zone
        self.addSubWorld(TILES_WIDTH*2,TILES_HEIGHT*2)

    def addSubWorld(self,x,y):
        if str(x)+";"+str(y) not in self.subworlds:
            self.subworlds[str(x)+";"+str(y)] = SubWorld(self.game,x,y)

    def updateActualTilesAndWaterGroup(self):
        self.actualtiles.clear()
        self.actualwater_group.empty()

        for cle, subworld in self.actualsubworlds.items():
            for tile in subworld.tiles:
                self.actualtiles.append(tile)
                if tile.id_ == "104" :
                    tile.add(self.actualwater_group)

        self.actualtiles.sort(key=lambda x: x.zindex, reverse=False)

    def updateSpecificActualSubworld(self,gnocchis):
        if str(gnocchis[0])+";"+str(gnocchis[1]) in self.subworlds:
            self.actualsubworlds[str(gnocchis[0])+";"+str(gnocchis[1])]=self.subworlds[str(gnocchis[0])+";"+str(gnocchis[1])]

    def updateActualSubworlds(self,gnocchis):
        self.actualsubworlds.clear()

        self.updateSpecificActualSubworld((gnocchis[0],gnocchis[1]))
        self.updateSpecificActualSubworld((gnocchis[0]+TILES_WIDTH,gnocchis[1]))
        self.updateSpecificActualSubworld((gnocchis[0],gnocchis[1]+TILES_HEIGHT))
        self.updateSpecificActualSubworld((gnocchis[0]+TILES_WIDTH,gnocchis[1]+TILES_HEIGHT))
        self.updateSpecificActualSubworld((gnocchis[0]-TILES_WIDTH,gnocchis[1]))
        self.updateSpecificActualSubworld((gnocchis[0],gnocchis[1]-TILES_HEIGHT))
        self.updateSpecificActualSubworld((gnocchis[0]-TILES_WIDTH,gnocchis[1]-TILES_HEIGHT))
        self.updateSpecificActualSubworld((gnocchis[0]-TILES_WIDTH,gnocchis[1]+TILES_HEIGHT))
        self.updateSpecificActualSubworld((gnocchis[0]+TILES_WIDTH,gnocchis[1]-TILES_HEIGHT))

        self.updateActualTilesAndWaterGroup()

class SubWorld:
    def __init__(self,game,centerx,centery):
        self.game = game

        self.centerx = centerx
        self.centery = centery


        self.objects = []
        self.animals = []
        self.tiles = []
        self.add_elements(self.centerx-round(TILES_WIDTH/2),self.centery-round(TILES_HEIGHT/2))

    def add_elements(self,start_x,start_y):
        end_x = start_x+TILES_WIDTH
        end_y = start_y+TILES_HEIGHT
        scale = 13
        octaves = 7
        lacunarity = 1.0
        persistence = 1.0
        for y in range (start_y,end_y,1):
            for x in range(start_x,end_x,1):
                value = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeatx=end_x,repeaty=end_y,base=0)
                tile = None
                if y%2 == 0:
                    tile = Tile((x*TILE_SIZE,y*TILE_SIZE/4),value,y)
                else :
                    tile = Tile((x*TILE_SIZE+TILE_SIZE/2,y*TILE_SIZE/4),value,y)
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
                    self.add_animals((x*TILE_SIZE,y*TILE_SIZE/4))

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
