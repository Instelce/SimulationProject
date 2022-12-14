from random import randint

from entity import Entity


class Plant(Entity):
    """ Plant
    ---

    Attributes
        category : str
        type : str
        pos : tuple
        world : World
        growth_speed : int
        max_regrowth : int
        food_amount : int
        color_base : int
        full_since : int
    """
    def __init__(self, type, pos, world, color, food_amount, growth_speed, max_regrowth, full_since_max) -> None:
        super().__init__(type, pos, world, color)
        self.category = 'plants'
        self.color_base = color
        self.growth_speed = growth_speed
        self.max_regrowth = max_regrowth
        self.food_amount = food_amount
        self.color = (self.color_base[0], self.color_base[1]-self.food_amount, self.color_base[2])
        self.full_since = 0
        self.full_since_max = full_since_max

    def action(self) -> None:
        """ Actions of plants : grow, spread """
        # Grow
        if self.food_amount < self.max_regrowth:
            self.food_amount += self.growth_speed
            self.color = [self.color_base[0], self.color_base[1]-self.food_amount/2, self.color_base[2]]
            
            for index, val in enumerate(self.color):
                if val >= 255:
                    self.color[index] = 255
                elif val <= 0:
                    self.color[index] = 0

        # Kill
        if self.food_amount <= 0:
            self.kill()

        # Increse full_since if grass food_amount is full
        if self.food_amount >= self.max_regrowth:
            self.full_since += 1
        else:
            self.full_since = 0
        
        # Add another grass : 25% chance 
        if self.full_since >= 5 and randint(0, 4) <= 1:
            all_grass_pos = [(self.pos[0]-1, self.pos[1]), (self.pos[0]+1, self.pos[1]), (self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1]-1)]
            new_grass_pos = None
            for pos in all_grass_pos:
                if self.world.getEntityAt(pos, self.type) == None:
                    new_grass_pos = pos
                else:
                    all_grass_pos.remove(pos)
            
            if len(all_grass_pos) > 0 and new_grass_pos != None:
                self.world.entities_dict[self.type].append(Plant(self.type, new_grass_pos, self.world, self.color_base, 5, self.growth_speed, self.max_regrowth, self.full_since_max))
        
        if self.full_since > self.full_since_max:
            self.kill()

