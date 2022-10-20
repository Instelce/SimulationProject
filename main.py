import pygame
import sys
import json

from settings import *
from menu import *
from world import World
from debug import debug


# Methods
def get_font(font_size) -> pygame.font.SysFont:
    """ Return pygame Font object """
    return pygame.font.SysFont('Calibri', font_size) 


def show_bar(current, max_amount, bg_rect, color):
    """ Display bar depending on current value """
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
        entity_index : int
        groups : list - list of pygame sprite Group object

        display_surface : Surface - main pygame surface
        image : Surface
        rect : Rect
    """
    def __init__(self, entity, entity_index, groups) -> None:
        super().__init__(groups)
        self.entity = entity
        self.entity_index = entity_index

        self.display_surface = pygame.display.get_surface()

        if self.entity.category == 'mammals':
            self.image = pygame.Surface((TILE_SIZE-10, TILE_SIZE-10))
            self.image.fill(self.entity.getColor())

            self.rect = self.image.get_rect(topleft=(self.entity.pos[0]*TILE_SIZE + 5, self.entity.pos[1]*TILE_SIZE + 5))
        elif self.entity.category == 'plants':
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(self.entity.getColor())

            self.rect = self.image.get_rect(topleft=(self.entity.pos[0]*TILE_SIZE, self.entity.pos[1]*TILE_SIZE))

    def update(self):
        if self.entity.category == 'mammals':
            if self.entity.can_reproduction:
                pygame.draw.rect(self.display_surface, (255, 40, 40), self.rect.copy(), 2)

            # Energie bar
            energie_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 2)
            show_bar(self.entity.energie, self.entity.max_energie, energie_rect, (250, 140, 45))

            # Health bar
            health_rect = pygame.Rect(self.rect.left, self.rect.top + 2, self.rect.width, 2)
            show_bar(self.entity.food_amount, self.entity.max_food_amount, health_rect, (255, 60, 50))
            
            # Genre lettre
            genre_text_surf = get_font(8).render(self.entity.genre[0].upper(), True, (255,255,225))
            genre_text_rect = genre_text_surf.get_rect(bottomleft=(self.rect.bottomleft[0] + 4, self.rect.bottomleft[1] - 4))
            self.display_surface.blit(genre_text_surf, genre_text_rect)
            
            # Line for food
            pygame.draw.circle(self.display_surface, self.entity.color, (self.entity.getAroundFood()[0]*TILE_SIZE+TILE_SIZE//2, self.entity.getAroundFood()[1]*TILE_SIZE+TILE_SIZE//2), 4)
            pygame.draw.line(self.display_surface, self.entity.color, (self.entity.pos[0]*TILE_SIZE+TILE_SIZE//2, self.entity.pos[1]*TILE_SIZE+TILE_SIZE//2), (self.entity.getAroundFood()[0]*TILE_SIZE+TILE_SIZE//2, self.entity.getAroundFood()[1]*TILE_SIZE+TILE_SIZE//2), 1)

            # Line for nearest partner
            if len(self.entity.world.entities_dict[self.entity.type]) >= 2 and self.entity.getAroundPartner() != None:
                pygame.draw.circle(self.display_surface, self.entity.color, (self.entity.getAroundPartner().pos[0]*TILE_SIZE+TILE_SIZE//2, self.entity.getAroundPartner().pos[1]*TILE_SIZE+TILE_SIZE//2), 4)
                pygame.draw.line(self.display_surface, self.entity.color, (self.entity.pos[0]*TILE_SIZE+TILE_SIZE//2, self.entity.pos[1]*TILE_SIZE+TILE_SIZE//2), (self.entity.getAroundPartner().pos[0]*TILE_SIZE+TILE_SIZE//2, self.entity.getAroundPartner().pos[1]*TILE_SIZE+TILE_SIZE//2), 2)

        if self.entity.category == 'plants':
            # Food amount text
            amount_text_surf = get_font(10).render(str(self.entity.food_amount), True, (255,255,255))
            amount_text_rect = amount_text_surf.get_rect(bottomright=(self.rect.bottomright[0] - 4, self.rect.bottomright[1] - 4))
            self.display_surface.blit(amount_text_surf, amount_text_rect)


class Interface:
    def __init__(self) -> None:
        pygame.init()

        # Setup interface
        pygame.display.set_caption('Simulation')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()
        self.pause = False

        # Components
        self.show_components = True
        self.components = ComponentsGroup()

        # Entities data
        self.entities_data = json.load(open('data/entities.json'))

        # Setup world
        self.world = World((WORLD_WIDTH, WORLD_HEIGHT))
        for category_data in self.entities_data.values():
            for entity_type in category_data:
                self.world.entities_dict[entity_type] = []

        # Entities buttons
        self.bestiary_panel_groups = ComponentsGroup()
        self.entities_buttons = {}
        for index_category, category in enumerate(self.entities_data):
            category_data = self.entities_data[category]
            self.entities_buttons[category] = []
            for index_entity, entity_type in enumerate(category_data):
                size = 20
                gap = 10
                surface = pygame.Surface((size, size))
                surface.fill(category_data[entity_type]['color'])
                pos = (20+(gap+size)*index_entity, SCREEN_HEIGHT-20-((gap+size)*len(self.entities_data))+((gap+size)*index_category))
                self.entities_buttons[category].append(ImageButton(pos, [self.components], surface))
                surface = pygame.Surface((size, size))
                surface.fill(self.entities_data['mammals']['sheep']['color'])
                self.selected_entity = {'type': 'sheep', 'category': 'mammals', 'surface': surface}
        self.selected_entity_preview = [Image((SCREEN_WIDTH-64-20, SCREEN_HEIGHT-64-20), [self.components], self.selected_entity['surface'], (64, 64)), Text((SCREEN_WIDTH-64-10, SCREEN_HEIGHT-64-10), [self.components], self.selected_entity['type'], 14)]
        
        # Sprites
        self.entities = pygame.sprite.Group()
 
        # Create grid 
        self.grid_rects = [] 
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.grid_rects.append(rect)
        self.selected_rect = self.grid_rects[0]

    def grid(self):
        """ Display grid """
        for rect in self.grid_rects:
            if rect.collidepoint(self.mouse_pos):
                self.selected_rect = rect
                pygame.draw.rect(self.screen, (100,100,100), rect, 1)
            else:
                pygame.draw.rect(self.screen, (30, 25, 25), rect, 1)

    def get_click(self):
        can_click = True
        for component in self.components.components:
            if component.rect.collidepoint(self.mouse_pos):
                can_click = False

        if can_click:
            if self.mouse_input[0]:
                self.world.createEntity(self.mouse_pos_world, self.selected_entity['category'], self.entities_data[self.selected_entity['category']][self.selected_entity['type']])
            if self.mouse_input[2]:
                if self.world.getEntitiesAt(self.mouse_pos_world) != []:
                    entities = self.world.getEntitiesAt(self.mouse_pos_world)
                    
                    for entity in entities:
                        entity.kill()

    def generateWorld(self):
        self.world.entities_dict = {}

        for category_name, category_data in self.entities_data.items():
            print(category_name)
            for entity_type in category_data:
                print("--", entity_type)
                self.world.generate(category_name, self.entities_data[category_name][entity_type])
        
    def resetWorld(self):
        self.world.entities_dict = {}
        for category_data in self.entities_data.values():
            for entity_type in category_data:
                self.world.entities_dict[entity_type] = []
        self.entities = pygame.sprite.Group()
    
    def update(self):
        current_time = pygame.time.get_ticks()

        # Cooldown of 1000ms
        if current_time - self.last_time >= 1000 and self.world.entities_dict != {}:
            self.last_time = current_time
            
            self.world.iteration()

            # Reset and create all sprites
            self.entities = pygame.sprite.Group()
            for entities_list in self.world.entities_dict.values():
                for entity in entities_list:
                    EntitySprite(entity, entities_list.index(entity), [self.entities])

    def update_tileset_panel_view(self):
        """ Reset selected_entity_preview """
        for component in self.selected_entity_preview:
            component.delete()
        self.selected_entity_preview = [Image((SCREEN_WIDTH-64-20, SCREEN_HEIGHT-64-20), [self.components], self.selected_entity['surface'], (64, 64)), Text((SCREEN_WIDTH-64-10, SCREEN_HEIGHT-64-10), [self.components], self.selected_entity['type'], 14)]
    
    def entities_panel_management(self):
        for category in self.entities_buttons:
            for index, button in enumerate(self.entities_buttons[category]):
                if button.is_clicked:
                    # Update selected tile
                    for index_entity, entity in enumerate(self.entities_data[category]):
                        if index_entity == index:
                            entity_type = entity
                            break
                    self.selected_entity['type'] = entity_type
                    self.selected_entity['category'] = category
                    surface = pygame.Surface((10,10))
                    surface.fill(self.entities_data[category][entity_type]['color'])
                    self.selected_entity['surface'] = surface

                    self.update_tileset_panel_view()
     
    def run(self): 
        while 1: 
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_input = pygame.mouse.get_pressed()
            self.mouse_pos_world = (self.selected_rect.x // TILE_SIZE, self.selected_rect.y // TILE_SIZE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Pause
                        self.pause = not self.pause
                    if event.key == pygame.K_g: # Generate
                        self.generateWorld()
                    if event.key == pygame.K_r: # Reset
                        self.resetWorld()
                    if event.key == pygame.K_m: # Show components
                        self.show_components = not self.show_components
 
            self.screen.fill((30, 25, 25))
 
            # Method
            if not self.pause:
                self.update()   
            self.grid()
            self.get_click()

            # Display entities
            self.entities.draw(self.screen)

            # Display components
            if self.show_components:
                self.entities.update()
                
                self.components.display()
                self.entities_panel_management()

            # Debug
            if self.show_components:
                entity_in_mouse = self.world.getEntityAt(self.mouse_pos_world, "sheep")
                debug((self.selected_rect.x / TILE_SIZE, self.selected_rect.y / TILE_SIZE))
                debug(f"{len(self.entities.sprites())} / {WORLD_WIDTH*WORLD_HEIGHT}", 30)
                debug(f"{[e.type for e in self.world.getEntitiesAt(self.mouse_pos_world)]}", 50)
                debug(f"pause {self.pause}", 70)
                debug(f"{self.world.time[0]} h {self.world.time[1]} min", 90)
                debug(f"{[e.type for e in self.world.getEntitiesAt(self.mouse_pos_world, '', 'plants')]}", 110)
                if entity_in_mouse is not None: debug(f"Index {self.world.entities_dict[entity_in_mouse.type].index(entity_in_mouse)}", 130)

            # for index, list_type in enumerate(self.world.entities_dict):
            #     debug(f"{list_type} : {len(self.world.entities_dict[list_type])}", 130+(20*index))

            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    interface = Interface()
    interface.run()

