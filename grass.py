from random import randint, choice


class Grass:
    """ Grass
    ---

    Attributes
        type : str
        pos : tuple
        world : World
        growth_speed : int
        max_regrowth : int - 100
        food_amount : int - 25, 50, 75, 100
        color_base : int - (52, 140, 49)
        color_mod : (int, int, int) - rgb color
        full_since : int
    """
    def __init__(self, pos, world, food_amount, growth_speed, color_mod) -> None:
        self.type = 'grass' 
        self.pos = pos
        self.world = world
        self.growth_speed = growth_speed
        self.max_regrowth = 100
        self.food_amount = food_amount
        self.color_base = (50, 180-self.food_amount, 50)
        self.color_mod = color_mod
        self.full_since = 0

    def action(self) -> None:
        # Grow
        if self.food_amount < self.max_regrowth:
            self.food_amount += self.growth_speed 
            self.color_base = (50, 180-self.food_amount, 50)

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
                if self.world.getGrassAt(pos) == None:
                    new_grass_pos = pos
                else:
                    all_grass_pos.remove(pos)
            
            if len(all_grass_pos) > 0 and new_grass_pos != None:
                self.world.entities_dict['grass'].append(Grass(new_grass_pos, self.world, 5, self.growth_speed, self.color_mod))

    def getColor(self):
        """ Return color (int, int, int)"""
        return self.color_base

    def kill(self) -> None:
        """ Destroy object """
        self.world.entities_dict[self.type].remove(self)
        del self

