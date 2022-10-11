import pygame
import sys

from monde import Monde

TILE_SIZE = 32
WORLD_WIDTH = 30
WORLD_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * WORLD_WIDTH
SCREEN_HEIGHT = TILE_SIZE * WORLD_HEIGHT


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
 
        # Grid 
        self.grid_rects = [] 
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.grid_rects.append(rect)
 
    def grid(self): 
        for rect in self.grid_rects:
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
 
            self.screen.fill((10, 10, 10))
 
            for mouton in self.world.liste_mouton:
                print(mouton.getAroundHerbe())
                print(len(self.world.liste_mouton))
                pygame.draw.line(self.screen, mouton.getColor(), mouton.pos, mouton.getAroundHerbe())
                print("--------------")

            # Method 
            self.grid() 

            # Display entities
            for entity in self.entities:
                pygame.draw.rect(self.screen, entity[0], entity[1])

            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    interface = Interface()
    interface.run()

