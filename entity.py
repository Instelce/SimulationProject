from random import randint, choice


class Entity:
    """ Entity
    ---

    Attributes
        type : str
        pos : tuple
        world : World
        color : tuple
        food_amount : int
        food_taken : int - food that the entity takes per mouthful

        food_type : str
        enemy_type : str

        reproduction_energie : int
        max_energie : int
        lose_energie : tuple 
        energie : int - random int between 80 and 130

        vision_range : int
        vision_type : str - 'large' or 'restricted'
   """
    def __init__(self, type, pos, world, color, food_amount, food_taken, food_type, enemy_type, reproduction_energie, max_energie, lose_energie, energie, vision_range, vision_type) -> None:
        self.type = type
        self.pos = pos
        self.world = world
        self.color = color
        self.food_amount = food_amount
        self.food_taken = food_taken

        self.food_type = food_type
        self.enemy_type = enemy_type

        self.reproduction_energie = reproduction_energie 
        self.max_energie = max_energie
        self.lose_energie = lose_energie
        self.energie = energie

        self.vision_range = vision_range
        self.vision_type = vision_type

    def action(self):
        """ Actions : food, movement, escape, reproduction """
        print("-----------------", self.getAroundFood())
        print("Data", self.sides)

    def getAroundFood(self) -> tuple:
        """ Return the direction to go to the nearest food """
        self.sides = {
                'x_left': {'energie_lost': 0, 'food_amount': 0, 'pos': self.pos, 'benefit': False},
                'x_right': {'energie_lost': 0, 'food_amount': 0, 'pos': self.pos, 'benefit': False},
                'y_top': {'energie_lost': 0, 'food_amount': 0, 'pos': self.pos, 'benefit': False},
                'y_down': {'energie_lost': 0, 'food_amount': 0, 'pos': self.pos, 'benefit': False},
        }
        energie_lost_average = (self.lose_energie[0]+self.lose_energie[1])/2

        # X left
        for index, x in enumerate(reversed(range(self.pos[0]-self.vision_range, self.pos[0]))):
            pos = (x, self.pos[1])
            if self.world.getEntitiesAt(pos) != []:
                entities = self.world.getEntitiesAt(pos)
                if self.food_type in [entity.type for entity in entities]:
                    for entity in entities:
                        if entity.type == self.food_type:
                            entity = entity
                    self.sides['x_left']['pos'] = pos
                    self.sides['x_left']['energie_lost'] = index * energie_lost_average
                    self.sides['x_left']['food_amount'] = entity.food_amount
                    break
                
        # X right
        for index, x in enumerate(range(self.pos[0], self.pos[0]+self.vision_range)):
            pos = (x, self.pos[1])
            if self.world.getEntitiesAt(pos) != []:
                entities = self.world.getEntitiesAt(pos)
                if self.food_type in [entity.type for entity in entities]:
                    for entity in entities:
                        if entity.type == self.food_type:
                            entity = entity
                    self.sides['x_right']['pos'] = pos
                    self.sides['x_right']['energie_lost'] = index * energie_lost_average
                    self.sides['x_right']['food_amount'] = entity.food_amount
                    break
        
        # Calculate benefit
        for side_name, side_data in self.sides.items():
            self.sides[side_name]['benefit'] = int((self.sides[side_name]['food_amount']/self.food_taken * 10) - self.sides[side_name]['energie_lost'])
            print(side_name, self.sides[side_name]['benefit'])

        x_data = [side for side_name, side in self.sides.items() if 'x' in side_name]
        y_data = [side for side_name, side in self.sides.items() if 'y' in side_name]
        
        if x_data[0]['benefit'] > x_data[1]['benefit']:
            max_x_side = 'x_left' 
        else:
            max_x_side = 'x_right'

        if x_data[0]['benefit'] == 0:
            max_x_side = 'x_right'
        if x_data[1]['benefit'] == 0:
            max_x_side = 'x_left'

        print("---------------")
        print("X data", x_data)
        print("Max x", max_x_side)
        print("Y data", y_data)
        print("---------------")

        max_side = 'x_left'
        return self.sides[max_side]['pos']

    def getColor(self):
        """ Return color at rgb (int, int, int) """
        return self.color

    def kill(self):
        """ Destroy object """
        print(f"{self.type} entity is dead ...")
        self.world.entities_dict[self.type].remove(self)
        del self

    def loseEnergie(self) -> None:
        """ Dicrease energie """
        self.energie -= choice(self.lose_energie)


