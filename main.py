import pygame
import sys

from monde import Monde

TILE_SIZE = 32
WORLD_WIDTH = TILE_SIZE * 30
WORLD_HEIGHT = TILE_SIZE * 20

class Interface:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption('Simulation')
        self.screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
        self.clock = pygame.time.Clock()

        self.world = Monde((WORLD_WIDTH, WORLD_HEIGHT))

        # Grid
        self.grid_rects = []
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            for y in range(0, WORLD_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.grid_rects.append(rect)

    def grid(self):
        for rect in self.grid_rects:
            pygame.draw.rect(self.screen, (0,0,0), rect, 1)

    def display_world(self):
        pass

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((10, 10, 10))

            # Method
            self.grid()
            self.display_world()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    interface = Interface()
    interface.run()