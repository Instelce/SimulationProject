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
    def __init__(self, type, pos, world, color, food_amount, energie_per_food_taken, food_taken, food_type, enemy_type, reproduction_energie, max_energie, lose_energie, energie, vision_range, vision_type) -> None:
        self.type = type
        self.pos = pos
        self.world = world
        self.color = color
        self.food_amount = food_amount
        self.food_taken = food_taken
        self.energie_per_food_taken = energie_per_food_taken

        self.food_type = food_type
        self.enemy_type = enemy_type

        self.reproduction_energie = reproduction_energie 
        self.max_energie = max_energie
        self.lose_energie = lose_energie
        self.energie = energie

        self.vision_range = vision_range
        self.vision_type = vision_type

    def __repr__(self) -> str:
        return str(self.__dict__)

    def action(self):
        """ Actions : food, movement, escape, reproduction """
        finished = False

        # Food
        if self.energie < self.max_energie:
            if self.world.getEntityAt(self.pos, self.food_type) != []:
                entity = self.world.getEntityAt(self.pos, self.food_type)
                if entity.food_amount > 0:
                    self.energie += (entity.food_amount * self.energie_per_food_taken) / self.food_taken
                    entity.food_amount -= self.food_taken

                    finished = True
                elif entity.food_amount <= 0:
                    entity.kill()

        # Movement
        self.getAroundFood()
        print("---------", self.max_side, self.type, self.food_type, self.pos, '->')
        for side in self.sides:
            print(self.sides[side]['pos'], '-', self.sides[side]['food_amount'])
        if self.energie > 0:
            if self.getAroundFood() != self.pos and not finished:
                if 'right' in self.max_side:
                    self.pos = (self.pos[0]+1, self.pos[1])
                if 'left' in self.max_side:
                    self.pos = (self.pos[0]-1, self.pos[1])
                if 'top' in self.max_side:
                    self.pos = (self.pos[0], self.pos[1]+1)
                if 'down' in self.max_side:
                    self.pos = (self.pos[0], self.pos[1]-1)
                
                self.loseEnergie()
                finished = True
            else:
                if not finished:
                    self.pos = (self.pos[0] + randint(-1, 1), self.pos[1])
                    self.pos = (self.pos[0], self.pos[1] + randint(-1, 1))

                    self.loseEnergie()
                    finished = True
        else:
            self.kill()

    def getAroundFood(self) -> tuple:
        """ Return the direction to go to the nearest food """
        self.sides = {
            'left': {'pos': self.pos, 'food_amount': 0},
            'right': {'pos': self.pos, 'food_amount': 0},
            'top': {'pos': self.pos, 'food_amount': 0},
            'down': {'pos': self.pos, 'food_amount': 0}
        }

        for x in reversed(range(self.pos[0], self.pos[0]+self.vision_range)):
            pos = (x, self.pos[1])
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                self.sides['left']['pos'] = pos
                self.sides['left']['food_amount'] = entity.food_amount
                break

        for x in range(self.pos[0], self.pos[0]+self.vision_range):
            pos = (x, self.pos[1])
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                self.sides['right']['pos'] = pos
                self.sides['right']['food_amount'] = entity.food_amount
                break

        for y in reversed(range(self.pos[1], self.pos[1]+self.vision_range)):
            pos = (self.pos[0], y)
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                self.sides['top']['pos'] = pos
                self.sides['top']['food_amount'] = entity.food_amount
                break
        
        for y in range(self.pos[0], self.pos[0]+self.vision_range):
            pos = (self.pos[0], y)
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                self.sides['down']['pos'] = pos
                self.sides['down']['food_amount'] = entity.food_amount
                break

        max_food_amount = max([self.sides[s]['food_amount'] for s in self.sides])

        for side in self.sides:
            if self.sides[side]['food_amount'] == max_food_amount:
                max_side_pos = self.sides[side]['pos']
        self.max_side = 'left'
        return self.sides[self.max_side]['pos']

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


