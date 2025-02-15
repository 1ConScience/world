from Tile import *
from Stag import *
from Badger import *
from Wolf import *
from Object import *
import noise
from constvar import *
import threading

class World:
    def __init__(self,game):
        self.game = game

        self.subworlds = {}

        self.actualsubworlds = {}

        self.actualtiles = []

        self.list_front_tiles = []
        for i in range(29,37,1):
            self.list_front_tiles.append("0"+str(i))

        #for collisions and other mechanics
        self.actualwater_group = pygame.sprite.Group()
        self.actualinoffensiveanimal_group = pygame.sprite.Group()
        self.actualrock_group = pygame.sprite.Group()
        self.actualwood_group = pygame.sprite.Group()

        self.genWorldStart()

    def genWorldStart(self):
        for y in range (-1,2,1):
            for x in range(-1,2,1):
                self.addSubWorld(x*TILES_WIDTH,y*TILES_HEIGHT)

    def addSubWorld(self,x,y):
        self.subworlds[str(x)+";"+str(y)] = SubWorld(self.game,(x,y))
        self.actualsubworlds[str(x)+";"+str(y)]=self.subworlds[str(x)+";"+str(y)]
        self.updateActualTilesnGroups()

    def updateActualTilesnGroups(self):
        #for display
        self.actualtiles.clear()

        #for collisions and other mechanics
        self.actualwater_group.empty()
        self.actualinoffensiveanimal_group.empty()
        self.actualrock_group.empty()
        self.actualwood_group.empty()

        #fill both
        for cle, subworld in self.actualsubworlds.items():
            for tile in subworld.tiles:
                self.actualtiles.append(tile)
                if tile.id == "104" :
                    tile.add(self.actualwater_group)
            for inoffensiveanimal in subworld.inoffensiveanimals:
                inoffensiveanimal.add(self.actualinoffensiveanimal_group)
            for rock in subworld.rocks:
                rock.add(self.actualrock_group)
            for wood in subworld.woods:
                wood.add(self.actualwood_group)

            for tile in subworld.door.tiles_for_collision:
                tile.add(self.actualrock_group)
        
        self.actualtiles.sort(key=lambda x: x.zindex, reverse=False)

    def updateSpecificActualSubworld(self,gnocchis):
        if str(gnocchis[0])+";"+str(gnocchis[1]) not in self.subworlds:
            a = threading.Thread(None, self.addSubWorld, None, (gnocchis[0],gnocchis[1]), {})
            a.start()
        else :
            self.actualsubworlds[str(gnocchis[0])+";"+str(gnocchis[1])]=self.subworlds[str(gnocchis[0])+";"+str(gnocchis[1])]
            self.updateActualTilesnGroups()

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

class SubWorld:
    def __init__(self,game,key):
        self.game = game

        self.key = key

        self.flowers = []
        self.plants = []
        self.rocks = []
        self.woods = []
        self.inoffensiveanimals = []

        self.tiles = []

        self.add_elements(self.key[0]-round(TILES_WIDTH2),self.key[1]-round(TILES_HEIGHT2))

        self.door = Door(key)

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
                #topographic_value = noise.pnoise2(x/32,y/32,octaves=1,persistence=persistence,lacunarity=lacunarity,repeatx=end_x,repeaty=end_y,base=0)
                topographic_value = None
                tile = None
                if y%2 == 0:
                    tile = Tile((x*TILE_SIZE,y*TILE_SIZE4),y,value=value,topographic_value=topographic_value)
                else :
                    tile = Tile((x*TILE_SIZE+TILE_SIZE2,y*TILE_SIZE4),y,value=value,topographic_value=topographic_value)
                self.tiles.append(tile)
                
                if x!=0 and y!=0 :
                    if tile.id == "040" :
                        luck = random.randint(0,2)
                        if luck == 0 :
                            self.add_flower(tile.rect,y+1)
                    elif tile.id == "036" :
                        self.add_plant(tile.rect,y+1)
                    elif tile.id == "028" :
                        luck = random.randint(0,10)
                        if luck == 0 :
                            self.add_wood(tile.rect,y+1)
                    elif tile.id == "063" :
                        luck = random.randint(0,10)
                        if luck == 0 :
                            self.add_rock(tile.rect,y+1)
                    elif tile.id != "104" :
                        luck = random.randint(0,300)
                        if luck == 0 :
                            self.add_inoffensiveanimals((x*TILE_SIZE,y*TILE_SIZE4))

    def add_inoffensiveanimals(self,pos):
        inoffensiveanimal = None
        luck = random.randint(0,1)
        if luck == 0 :
            inoffensiveanimal = Badger(pos,self.game,self.key)
        else :
            inoffensiveanimal = Stag(pos,self.game,self.key)
        self.inoffensiveanimals.append(inoffensiveanimal)

    def add_flower(self,pos,zindex):
        flower = Flower(pos,zindex)
        self.flowers.append(flower)

    def add_plant(self,pos,zindex):
        plant = Plant(pos,zindex)
        self.plants.append(plant)

    def add_wood(self,pos,zindex):
        wood = Wood(pos,zindex)
        self.woods.append(wood)

    def add_rock(self,pos,zindex):
        rock = Rock(pos,zindex)
        self.rocks.append(rock)
