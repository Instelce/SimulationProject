from random import randint, choice

from plants import Plant
from mammal import Mammal


class World:
    """ World
    ---

    Attributes
        dimentions : tuple
        entities_dict : dict
        time : list
    """
    def __init__(self, dimensions):
        self.dimensions = dimensions

        self.entities_dict = {} # contains all entity lists
        self.time = [0, 0] # Hours, minutes

    def iteration(self) -> None: 
        """ Iteration of world""" 
        for entity_list in self.entities_dict.values():
            for entity in entity_list:
                entity.action()
        
        self.time[1] += 1
        if self.time[1] == 60:
            self.time[0] += 1
            self.time[1] = 0
        
    def getEntityAt(self, position, entity_type):
        """ Return Entity with specific type of None"""
        for entity in self.entities_dict.get(entity_type):
            if entity.pos == position and entity_type == entity.type:
                return entity
        return None

    def getEntitiesAt(self, position, ban_type="", ban_category="") -> list:
        """ Returns list of entities at position 
        
        if ban_type is not "" ban all entities with the type of ban_type
        """
        entities_in_pos = []
        for entities_list in self.entities_dict.values():
            if ban_category == "":
                if ban_type == "":
                    for entity in entities_list:
                        if entity.pos == position:
                            entities_in_pos.append(entity)
                else:
                    for entity in entities_list:
                        if entity.pos == position and entity.type != ban_type:
                            entities_in_pos.append(entity)
            else:
                if ban_type == "":
                    for entity in entities_list:
                        if entity.pos == position and entity.category != ban_category:
                            entities_in_pos.append(entity)
                else:
                    for entity in entities_list:
                        if entity.pos == position and entity.type != ban_type and entity.category != ban_category:
                            entities_in_pos.append(entity)

        return entities_in_pos

    def createEntity(self, pos, category, entity_data):
        """ Create Entity"""
        entity_type = entity_data['type']
        print(entity_type)

        if self.getEntitiesAt(pos) == []:        
            if category == 'plants':
                self.entities_dict[entity_type].append(Plant(
                        entity_type,
                        pos, 
                        self, 
                        entity_data['color'],
                        choice(range(entity_data['food_amount'][0], entity_data['food_amount'][1]+1, 25)), 
                        entity_data['growth_speed'],
                        entity_data['max_regrowth']
                    ))
            if category == 'mammals':
                self.entities_dict[entity_type].append(Mammal(
                        entity_type, 
                        pos, 
                        self, 
                        entity_data['color'], 
                        entity_data['food_amount'], 
                        entity_data['energie_per_food_taken'],
                        entity_data['food_taken'],
                        entity_data['food_type'], 
                        entity_data['enemy_type'], 
                        entity_data['reproduction_energie'], 
                        entity_data['max_energie'], 
                        tuple(entity_data['lose_energie']),
                        randint(entity_data['start_energie'][0], entity_data['start_energie'][1]),
                        entity_data['vision_range'],
                        entity_data['vision_type'],
                        choice(['male', 'female'])
                    ))

    def generate(self, category, entity_data) -> None:
        """ Randomly generates entities from entity_data dict """
        entity_type = entity_data['type']
        self.entities_dict[entity_type] = []

        # Loop dimentions
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if randint(0, 1000) <= int(entity_data['generate_percentage']*10): # Can generate
                    if category == 'plants':
                        self.entities_dict[entity_type].append(Plant(
                                entity_type,
                                (x,y), 
                                self, 
                                entity_data['color'],
                                choice(range(entity_data['food_amount'][0], entity_data['food_amount'][1]+1, 25)), 
                                entity_data['growth_speed'],
                                entity_data['max_regrowth']
                            ))
                    if category == 'mammals':
                        self.entities_dict[entity_type].append(Mammal(
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
                                entity_data['vision_type'],
                                choice(['male', 'female'])
                            ))
                        

