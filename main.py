import pygame
import sys
import json

from world import World
from debug import debug


TILE_SIZE = 32
WORLD_WIDTH = 30
WORLD_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * WORLD_WIDTH
SCREEN_HEIGHT = TILE_SIZE * WORLD_HEIGHT

# Methods
def get_font(font_size):
    return pygame.font.SysFont('Calibri', font_size) 


def show_bar(current, max_amount, bg_rect, color):
    """ Display bar """
    display_surface = pygame.display.get_surface()

    # display bg_rect
    pygame.draw.rect(display_surface, (color[0]/2, color[1]/2, color[2]/2), bg_rect)
    
    # convert current value to pixel
    ratio = current / max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width

    # draw the bar
    pygame.draw.rect(display_surface, color, current_rect)


class EntitySprite(pygame.sprite.Sprite):
    """ Entity for Interface 
    ---
    
    Attributes
        entity : Entity
        groups : list - list of pygame sprite Group object
        display_surface : Surface - main pygame surface
        image : Surface
        rect : Rect
    """
    def __init__(self, entity, groups) -> None:
        super().__init__(groups)
        self.entity = entity

        self.display_surface = pygame.display.get_surface()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(self.entity.getColor())

        self.rect = self.image.get_rect(topleft=(self.entity.pos[0]*TILE_SIZE, self.entity.pos[1]*TILE_SIZE))

        if self.entity.type != 'grass':
            self.energie_rect = pygame.Rect(self.rect.left, self.rect.top, TILE_SIZE, 5)

        if self.entity.type == 'grass':
            self.amount_text_surf = get_font(10).render(str(self.entity.food_amount), True, (255,255,255))
            self.amount_text_rect = self.amount_text_surf.get_rect(topleft=self.rect.center)

    def update(self):
        if self.entity.type == 'grass': 
            self.display_surface.blit(self.amount_text_surf, self.amount_text_rect)
        if self.entity.type != 'grass': 
            self.energie_rect = pygame.Rect(self.rect.left, self.rect.top, TILE_SIZE, 5)
            show_bar(self.entity.energie, self.entity.max_energie, self.energie_rect, (250, 220, 45))
    

class Interface:
    def __init__(self) -> None:
        pygame.init()

        # Setup interface
        pygame.display.set_caption('Simulation')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()
        self.keys_time = pygame.time.get_ticks()
        self.pause = False

        # Entities data
        self.entities_data = json.load(open('data/entities.json'))

        # Setup world
        self.world = World((WORLD_WIDTH, WORLD_HEIGHT))

        for category_name, category_data in self.entities_data.items():
            print(category_name)
            for entity_type in category_data:
                print("--", entity_type)
                self.world.generate(category_name, self.entities_data[category_name][entity_type])

        # Create all sprites
        self.entities = pygame.sprite.Group()
        for entities_list in self.world.entities_dict.values():
            for entity in entities_list:
                entity_sprite = EntitySprite(entity, [self.entities])
                self.entities.add(entity_sprite) 
 
        # Create grid 
        self.grid_rects = [] 
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.grid_rects.append(rect)
        self.selected_rect = self.grid_rects[0]

    def input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - self.keys_time >= 300:
            if keys[pygame.K_SPACE]:
                self.pause = not self.pause
 
    def grid(self): 
        """ Display grid """
        for rect in self.grid_rects:
            if rect.collidepoint(self.mouse_pos):
                self.selected_rect = rect
                pygame.draw.rect(self.screen, (100,100,100), rect, 1)
            else:
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)
 
    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_time >= 1000:
            self.last_time = current_time
            
            self.world.iteration()

            # Reset and create all sprites
            self.entities = pygame.sprite.Group()
            for entities_list in self.world.entities_dict.values():
                for entity in entities_list:
                    entity_sprite = EntitySprite(entity, [self.entities])
                    self.entities.add(entity_sprite)
     
    def run(self): 
        while 1: 
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 
            self.screen.fill((10, 10, 10))
 
            # Method
            self.input()
            if not self.pause:
                self.update()   
            self.grid() 

            # Display and update entities
            self.entities.draw(self.screen)
            self.entities.update()

            for sheep in self.world.entities_dict['sheep']:
                pygame.draw.line(self.screen, (0, 255, 255), (sheep.pos[0]*TILE_SIZE+TILE_SIZE//2, sheep.pos[1]*TILE_SIZE+TILE_SIZE//2), (sheep.getAroundFood()[0]*TILE_SIZE+TILE_SIZE//2, sheep.getAroundFood()[1]*TILE_SIZE+TILE_SIZE//2), 4)

            # Debug
            debug((self.selected_rect.x / TILE_SIZE, self.selected_rect.y / TILE_SIZE))
            debug(f"{len(self.entities.sprites())} / {WORLD_WIDTH*WORLD_HEIGHT}", 30)
            debug(f"pause {self.pause}", 50)

            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    interface = Interface()
    interface.run()

