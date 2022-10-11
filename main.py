import pygame
import sys

from monde import Monde
from debug import debug


TILE_SIZE = 32
WORLD_WIDTH = 30
WORLD_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * WORLD_WIDTH
SCREEN_HEIGHT = TILE_SIZE * WORLD_HEIGHT


class SpriteEntity(pygame.sprite.Sprite):
    """ Entity for Interface 
    ---
    
    Attributes
        pos : int
        groups : Group
        entity : Entity - sheep or wolf
    """
    def __init__(self, pos, groups, entity) -> None:
        super().__init__(groups)
        self.pos = pos
        self.entity = entity

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(self.entity.getColor())

        self.rect = self.imgage.get_rect(topleft=self.pos)
    

class Interface:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption('Simulation')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.entities = []

        # Setup world
        self.world = Monde((WORLD_WIDTH, WORLD_HEIGHT))
        self.world.generate('herbe', 10)
        self.world.generate('mouton', 1)
        self.update_world()

        for mouton in self.world.liste_mouton:
            print("Mouton", mouton.pos)
            print("Go to", mouton.getAroundHerbe())
            print("Max side", mouton.max_side)
            # print("Amount", self.world.getHerbeAt(mouton.getAroundHerbe()).amount)
            print("All side", mouton.sides)
            print('------------------')
 
        # Grid 
        self.grid_rects = [] 
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.grid_rects.append(rect)
        self.selected_rect = self.grid_rects[0]
 
    def grid(self): 
        for rect in self.grid_rects:
            if rect.collidepoint(self.mouse_pos):
                self.selected_rect = rect
                pygame.draw.rect(self.screen, (100,100,100), rect, 1)
            else:
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)
 
    def update_world(self): 
        # Grass 
        for herbe in self.world.liste_herbe:
            rect = pygame.Rect(herbe.pos[0] * TILE_SIZE, herbe.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.entities.append([herbe.getColor(), rect]) 
 
        # Entities 
        for mouton in self.world.liste_mouton:
            rect = pygame.Rect(mouton.pos[0] * TILE_SIZE, mouton.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.entities.append([mouton.getColor(), rect]) 
 
    def run(self): 
        while 1: 
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
 
            self.screen.fill((10, 10, 10))
 
            # Method 
            self.grid() 

            # Display entities
            for entity in self.entities:
                pygame.draw.rect(self.screen, entity[0], entity[1])

            for mouton in self.world.liste_mouton:
                pygame.draw.line(self.screen, (0, 255, 255), (mouton.pos[0]*TILE_SIZE, mouton.pos[1]*TILE_SIZE), (mouton.getAroundHerbe()[0]*TILE_SIZE, mouton.getAroundHerbe()[1]*TILE_SIZE), 4)

            # Debug
            debug((self.selected_rect.x / TILE_SIZE, self.selected_rect.y / TILE_SIZE))

            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    interface = Interface()
    interface.run()

