from Animal import *

class Stag(Animal):
    def __init__(self,pos):
        super().__init__("stag/critter_stag",24,pos)  
        self.mask = pygame.mask.from_surface(pygame.image.load("assets/animals/stag/stag_mask.png").convert_alpha())