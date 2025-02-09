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

        self.water_group = pygame.sprite.Group()

        self.w_ = 854
        self.h_ = 480
        self.display_surf = pygame.Surface((self.w_, self.h_))

        self.world = World(self)

        self.player = Player(self)

        self.camera_aim = vec(0,0)
        self.camera = vec(0,0)
    
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

            self.world.expand()
            
            self.updateCamera()

            self.display()

            self.screen.blit(pygame.transform.scale(self.display_surf,
                                                    (self.screen.get_width(),self.screen.get_height())),
                                                    (0,0))

            show_fps = Text(str(int(self.clock.get_fps())),(255,255,255),20,(20,15))
            show_fps.display(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def displayOnlyScreen(self,list):
        for elem in list :
            if elem.rect.x >= self.camera.x-32 and elem.rect.x <= self.camera.x+self.w_ :
                if elem.rect.y >= self.camera.y-32 and elem.rect.y <= self.camera.y+self.h_ :
                    elem.display(self.display_surf,self.camera)

    def display(self):
        self.displayOnlyScreen(self.world.tiles)
        self.displayOnlyScreen(self.world.objects)
        self.displayOnlyScreen(self.world.animals)

        self.player.display(self.display_surf,self.camera)

    def updateCamera(self):
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

game = Game().run()