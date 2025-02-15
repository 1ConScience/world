from World import *
from Player import *
from Util import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME, vsync=1)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("WORLD")
        self.clock = pygame.time.Clock()
        self.running = True

        self.w_ = 640
        self.h_ = 360
        self.display_surf = pygame.Surface((self.w_, self.h_))

        loading_txt = Text("LOADING",(255,255,255),40,(self.screen.get_width()/2, self.screen.get_height()/2))
        loading_txt.display(self.screen)
        pygame.display.flip()

        self.world = World(self)

        self.player = Player(self)
        self.player_group = pygame.sprite.Group()
        self.player.add(self.player_group)

        self.elements_to_display = []

        self.camera_aim = vec(self.player.pos.x - self.w_/2,self.player.pos.y - self.h_/2)
        self.camera = vec(self.player.pos.x - self.w_/2,self.player.pos.y - self.h_/2)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.display_surf.fill("black")
            self.screen.fill("black")
            
            self.player.move()

            gnocchis = self.player.testNewSubworldkey()
            if gnocchis != None :
                self.world.updateActualSubworlds(gnocchis)

            self.moveAnimals()
            
            self.updateCameraCenterSmooth()

            self.display()

            self.screen.blit(pygame.transform.scale(self.display_surf,
                                                    (self.screen.get_width(),self.screen.get_height())),
                                                    (0,0))

            show_fps = Text(str(int(self.clock.get_fps())),(255,255,255),20,(20,15))
            show_fps.display(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def moveAnimals(self):
        for inoffensiveanimal in self.world.actualinoffensiveanimal_group:
            if inoffensiveanimal.rect.x >= self.camera.x-TILE_SIZE and inoffensiveanimal.rect.x <= self.camera.x+self.w_ :
                if inoffensiveanimal.rect.y >= self.camera.y-TILE_SIZE and inoffensiveanimal.rect.y <= self.camera.y+self.h_ :
                    inoffensiveanimal.move()

    def fillElements_to_display(self,list):
        for elem in list :
            if elem.rect.x >= self.camera.x-TILE_SIZE and elem.rect.x <= self.camera.x+self.w_ :
                if elem.rect.y >= self.camera.y-TILE_SIZE and elem.rect.y <= self.camera.y+self.h_ :
                    self.elements_to_display.append(elem)

    def display(self):
        self.elements_to_display.clear()


        self.fillElements_to_display(self.world.actualtiles)

        for cle, subworld in self.world.actualsubworlds.items():
            self.fillElements_to_display(subworld.flowers)
            self.fillElements_to_display(subworld.plants)
            self.fillElements_to_display(subworld.woods)
            self.fillElements_to_display(subworld.rocks)
            self.fillElements_to_display(subworld.inoffensiveanimals)

            self.elements_to_display.append(subworld.door)

        self.elements_to_display.append(self.player)


        self.elements_to_display.sort(key=lambda x: x.zindex, reverse=False)

        for elem in self.elements_to_display :
            elem.display(self.display_surf,self.camera)

    def updateCameraCenterSmooth(self):
            self.camera_aim = vec(self.player.pos.x - self.w_/2,self.player.pos.y - self.h_/2)

            self.camera_aim.x = round(self.camera_aim.x)
            self.camera_aim.y = round(self.camera_aim.y)

            if self.camera_aim.x > self.camera.x :
                self.camera.x += 1
            if self.camera_aim.x < self.camera.x :
                self.camera.x -= 1
            if self.camera_aim.y > self.camera.y :
                self.camera.y += 1
            if self.camera_aim.y < self.camera.y :
                self.camera.y -= 1

    def updateCameraCenter(self):
            self.camera_aim = vec(self.player.pos.x - self.w_/2,self.player.pos.y - self.h_/2)

            self.camera.x = round(self.camera_aim.x)
            self.camera.y = round(self.camera_aim.y)

game = Game().run()