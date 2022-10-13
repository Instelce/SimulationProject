from random import randint, choice

from entity import Entity
from grass import Grass
from sheep import Sheep
from wolf import Wolf


class World:
    """ World
    ---

    Attributes
        dimentions : tuple
        grass_list : list
        wolf_list : list
        sheep_list : list
    """
    def __init__(self, dimensions):
        self.dimensions = dimensions

        self.entities_dict = {} # contains all entity lists

    def iteration(self) -> None: 
        """ Iteration of world""" 
        for entity_list in self.entities_dict.values():
            for entity in entity_list:
                entity.action()

    def getGrassAt(self, position) -> Grass or None:
        """ Return None or Grass object """ 
        for grass in self.entities_dict['grass']: 
            if grass.pos == position:
                return grass
        return None

    def getEntityAt(self, position, entity_type):
        """ Returns list of entities type at position """
        entity = None
        for entity in self.entities_dict.get(entity_type):
            if entity.pos == position and entity_type == entity.type:
                entity = entity
        return entity

    def getEntitiesAt(self, position) -> list:
        """ Returns list of entities at position """
        entities_in_pos = []
        for entities_list in self.entities_dict.values():
            for entity in entities_list:
                if entity.pos == position:
                    entities_in_pos.append(entity)
        return entities_in_pos

    def generate(self, category, entity_data) -> None:
        """ Randomly generates entities from entity_data """
        entity_type = entity_data['type']
        self.entities_dict[entity_type] = []
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if randint(0, 1000) <= int(entity_data['generate_percentage']*10): # Can generate
                    if category == 'plants':
                        self.entities_dict[entity_type].append(Grass(
                                (x,y), 
                                self, 
                                choice(range(entity_data['food_amount'][0], entity_data['food_amount'][1]+1, 25)), 
                                entity_data['growth_speed'],
                                entity_data['color']
                            ))
                    if category == 'mammals':
                        self.entities_dict[entity_type].append(Entity(
                                entity_type, 
                                (x,y), 
                                self, 
                                entity_data['color'], 
                                entity_data['food_amount'], 
                                entity_data['food_taken'],
                                entity_data['energie_per_food_taken'],
                                entity_data['food_type'], 
                                entity_data['enemy_type'], 
                                entity_data['reproduction_energie'], 
                                entity_data['max_energie'], 
                                tuple(entity_data['lose_energie']),
                                randint(entity_data['start_energie'][0], entity_data['start_energie'][1]),
                                entity_data['vision_range'],
                                entity_data['vision_type']
                            ))
                        

