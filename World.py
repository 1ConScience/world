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
        self.actualtree_group = pygame.sprite.Group()
        self.actualflower_group = pygame.sprite.Group()

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
        self.actualtree_group.empty()
        self.actualflower_group.empty()

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
            for tree in subworld.trees:
                tree.add(self.actualtree_group)
            for flower in subworld.flowers:
                flower.add(self.actualflower_group)
        
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
        self.trees = []
        self.inoffensiveanimals = []

        self.playerTiles = {}
        self.playerTiles_alreadySorted = []

        self.tiles = []

        self.addElements(self.key[0]-round(TILES_WIDTH2),self.key[1]-round(TILES_HEIGHT2))

    def addTile(self,tile):
        x = int(tile.pos[0])
        y = int(tile.pos[1])

        if str(x)+";"+str(y) not in self.playerTiles:
            self.playerTiles[str(x)+";"+str(y)] = []

        level = len(self.playerTiles[str(x)+";"+str(y)])

        tile = Tile((x,y-level*TILE_SIZE4),tile.zindex,specific_id = "wooden")

        self.playerTiles[str(x)+";"+str(y)].append(tile)


        self.playerTiles_alreadySorted.append(tile)
        self.playerTiles_alreadySorted.sort(key=lambda x: x.zindex, reverse=False)

    def removeTile(self,tile,order_remove_reversed = False):
        x = int(tile.pos[0])
        y = int(tile.pos[1])

        if str(x)+";"+str(y) in self.playerTiles:
            level = len(self.playerTiles[str(x)+";"+str(y)])
            if level > 0 :
                if order_remove_reversed :
                    self.playerTiles[str(x)+";"+str(y)].pop(0)
                else :
                    self.playerTiles[str(x)+";"+str(y)].pop(level-1)

        self.playerTiles_alreadySorted.clear()
        for cle, column in self.playerTiles.items():
            for tile in column :
                self.playerTiles_alreadySorted.append(tile)
        self.playerTiles_alreadySorted.sort(key=lambda x: x.zindex, reverse=False)

    def addElements(self,start_x,start_y):
        end_x = start_x+TILES_WIDTH
        end_y = start_y+TILES_HEIGHT
        scale = 25#13
        octaves = 10#7
        lacunarity = 1.0
        persistence = 1.0
        for y in range (start_y,end_y,1):
            for x in range(start_x,end_x,1):
                value = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeatx=end_x,repeaty=end_y,base=0)
                tile = None
                if y%2 == 0:
                    tile = Tile((x*TILE_SIZE,y*TILE_SIZE4),y,value=value)
                else :
                    tile = Tile((x*TILE_SIZE+TILE_SIZE2,y*TILE_SIZE4),y,value=value)
                self.tiles.append(tile)
                
                if not(x==0 and y==0) :
                    if tile.id == "040" :
                        luck = random.randint(0,4)
                        if luck == 0 :
                            self.add_rock(tile.rect,y+1)
                    if tile.id == "025" :
                        luck = random.randint(0,8)
                        if luck == 0 :
                            self.add_tree(tile.rect,y+1)
                    if tile.id == "027" :
                        luck = random.randint(0,4)
                        if luck == 0 :
                            self.add_flower(tile.rect,y+1)
                    elif tile.id == "029" or tile.id == "030" or tile.id == "031" or tile.id == "032" or tile.id == "033" or tile.id == "034" or tile.id == "035"  or tile.id == "036"  :
                        self.add_plant(tile.rect,y+1,tile.id)
                    elif tile.id == "028" :
                        luck = random.randint(0,10)
                        if luck == 0 :
                            self.add_wood(tile.rect,y+1)
                    elif tile.id != "104" :
                        luck = random.randint(0,150)
                        if luck == 0 :
                            self.add_inoffensiveanimals((x*TILE_SIZE,y*TILE_SIZE4))

    def add_inoffensiveanimals(self,pos):
        inoffensiveanimal = Stag(pos,self.game,self.key)
        self.inoffensiveanimals.append(inoffensiveanimal)

    def add_flower(self,pos,zindex):
        flower = Flower(pos,zindex)
        self.flowers.append(flower)

    def add_plant(self,pos,zindex,id):
        plant = Plant(pos,zindex,id)
        self.plants.append(plant)

    def add_wood(self,pos,zindex):
        wood = Wood(pos,zindex)
        self.woods.append(wood)

    def add_tree(self,pos,zindex):
        tree = Tree(pos,zindex)
        self.trees.append(tree)

    def add_rock(self,pos,zindex):
        rock = Rock(pos,zindex)
        self.rocks.append(rock)

class Door(Entity):
    def __init__(self,key):
        centerx = key[0]
        centery = key[1]
        super().__init__(centery) 

        centerx*=TILE_SIZE
        centery*=TILE_SIZE4

        self.tiles = []
        self.tiles_for_collision = []

        for i in range(0,11,1):
            tile_bis = Tile((-TILE_SIZE+centerx,-TILE_SIZE4*i+centery),i-1+centery,specific_id = "061")
            self.tiles.append(tile_bis)
            if i <= 1 :
                self.tiles_for_collision.append(tile_bis)
        for i in range(0,11,1):
            tile_bis = Tile((TILE_SIZE+centerx,-TILE_SIZE4*i+centery),i-1+centery,specific_id = "061")
            self.tiles.append(tile_bis)
            if i <= 1 :
                self.tiles_for_collision.append(tile_bis)
            
        tile_bis = Tile((centerx,-TILE_SIZE4*9+centery),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

        tile_bis = Tile((centerx+TILE_SIZE2,-TILE_SIZE4*9+centery+TILE_SIZE4),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

        tile_bis = Tile((centerx-TILE_SIZE2,-TILE_SIZE4*9+centery+TILE_SIZE4),8+centery,specific_id = "061")
        self.tiles.append(tile_bis)

    def display(self,surf,camera):
        for tile in self.tiles:
            tile.display(surf,camera)