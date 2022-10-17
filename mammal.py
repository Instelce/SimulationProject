from random import randint, choice, shuffle
from math import copysign

from entity import Entity


class Mammal(Entity):
    """ Mammal
    ---

    Attributes
        category : str
        type : str
        pos : tuple
        world : World
        color : tuple
        food_amount : int
        food_regime : str - "carnivore" or "herbivore"
        food_taken : int - food that the mammal takes per mouthful

        food_type : str
        enemy_type : str

        reproduction_energie : int
        max_energie : int
        lose_energie : tuple 
        energie : int - random int between 80 and 130

        vision_range : int
        vision_type : str - "large" or "restricted"
        speed : int

        genre : str - "female" or "male"
   """
    def __init__(self, type, pos, world, color, food_amount, food_taken, food_regime, energie_per_food_taken, food_type, enemy_type, reproduction_energie, max_energie, lose_energie, energie, start_energie, vision_range, vision_type, speed, genre) -> None:
        super().__init__(type, pos, world, color)
        self.category = 'mammals'
        self.food_amount = food_amount
        self.food_taken = food_taken
        self.food_regime = food_regime
        self.energie_per_food_taken = energie_per_food_taken

        self.food_type = food_type
        self.enemy_type = enemy_type

        self.reproduction_energie = reproduction_energie 
        self.max_energie = max_energie
        self.lose_energie = lose_energie
        self.energie = energie
        self.start_energie = start_energie

        self.vision_range = vision_range
        self.vision_type = vision_type
        self.speed = speed

        self.genre = genre
        self.can_reproduction = False

        self.is_hurt = False
        self.target_food_pos = None

    def action(self):
        """ Actions : food, movement, escape, reproduction """
        if self.target_food_pos == None:
            self.target_food_pos = self.getAroundFood()
        if self.food_regime == 'herbivore':
            self.target_food_pos = self.getAroundFood()
        
        self.can_reproduction = False
        finished = False
        all_pos_around = [
            (self.pos[0] - 1, self.pos[1]), # left
            (self.pos[0] + 1, self.pos[1]), # right
            (self.pos[0], self.pos[1] - 1), # top
            (self.pos[0], self.pos[1] + 1), # down
        ]

        # Food
        if self.energie + self.energie_per_food_taken < self.max_energie:
            if self.food_regime == 'carnivore':
                for pos in all_pos_around:
                    if self.world.getEntityAt(pos, self.food_type) != None:
                        entity = self.world.getEntityAt(pos, self.food_type)
                        entity.is_hurt = True
                        
                        if entity.food_amount > 0:
                            self.energie += (entity.food_amount * self.energie_per_food_taken) / self.food_taken if entity.food_amount < self.food_taken else self.energie_per_food_taken     
                            entity.food_amount -= self.food_taken

                            finished = True

            if self.food_regime == 'herbivore':
                if self.world.getEntityAt(self.pos, self.food_type) != None:
                    entity = self.world.getEntityAt(self.pos, self.food_type)
                    if entity.food_amount > 0:
                        self.energie += (entity.food_amount * self.energie_per_food_taken) / self.food_taken if entity.food_amount < self.food_taken else self.energie_per_food_taken
                        entity.food_amount -= self.food_taken

                        finished = True
        
        # Reproduction
        if self.reproduction_energie < self.energie and not finished:
            closer_partner = self.getAroundPartner()
            for pos in all_pos_around:
                if self.world.getEntityAt(pos, self.type) != None:
                    entity = self.world.getEntityAt(pos, self.type)
                    if entity.genre != self.genre:
                        self.can_reproduction = True
                        break

            # Move to partner
            if not self.can_reproduction and closer_partner != None:
                x_move = self.pos[0] - closer_partner.pos[0]
                y_move = self.pos[1] - closer_partner.pos[1]

                if x_move != 0:
                    direction = (int(copysign(1, -x_move)), 0)
                if y_move != 0:
                    direction = (0, int(copysign(1, -y_move)))

                self.pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                self.loseEnergie('movement')
                finished = True

            # Reproduction
            if not finished and self.can_reproduction and closer_partner != None:
                for pos in all_pos_around:
                    if self.world.getEntityAt(pos, self.type) == None and closer_partner.energie > closer_partner.reproduction_energie:
                        self.loseEnergie('reproduction')
                        if self.genre == 'female':
                            self.world.createEntity(pos, self.category, self.__dict__)
                        finished = True
                        break

        # Movement
        if 0 < self.energie and not self.is_hurt and not finished:
            if self.food_regime == 'herbivore':
                if self.target_food_pos == self.pos:
                    self.target_food_pos = self.getAroundFood()
            elif self.food_regime == 'carnivore':
                for pos in all_pos_around:
                    if self.target_food_pos == pos:
                        self.target_food_pos = self.getAroundFood()

            if self.food_regime == 'carnivore':
                print("CARNIVORE POS", self.pos)
                print(">>>", self.getAroundFood())
            
            if self.target_food_pos != self.pos:
                x_move = self.pos[0] - self.target_food_pos[0]
                y_move = self.pos[1] - self.target_food_pos[1]

                # Get direction
                if x_move != 0:
                    direction = (int(copysign(1, -x_move)), 0)
                if y_move != 0:
                    direction = (0, int(copysign(1, -y_move)))

                pos = (self.pos[0] + (direction[0]*self.speed), self.pos[1] + (direction[1]*self.speed))

                if self.food_regime == 'carnivore':
                    if self.world.getEntitiesAt(pos, self.food_type, "plants") == []:
                        self.pos = pos

                        print("MOVE TO", pos)
                        self.loseEnergie('movement')
                        finished = True
                elif self.food_regime == 'herbivore':
                    if self.world.getEntitiesAt(pos, self.food_type) == []:
                        self.pos = pos

                        print("MOVE TO", pos)
                        self.loseEnergie('movement')
                        finished = True
            
            if self.target_food_pos == self.pos and not finished:
                random_pos = choice([(self.pos[0] + (randint(-1, 1) * self.speed), self.pos[1]), (self.pos[0], self.pos[1] + (randint(-1, 1) * self.speed))])

                while self.world.getEntitiesAt(random_pos, self.food_type, "plants") != [] and 0 < random_pos[0] < self.world.dimensions[0]-1 and 0 < random_pos[1] < self.world.dimensions[1]-1:
                    random_pos = choice([(self.pos[0] + (randint(-1, 1) * self.speed), self.pos[1]), (self.pos[0], self.pos[1] + (randint(-1, 1) * self.speed))])
                    
                self.pos = random_pos

                print("RANDOM MOVE TO", random_pos, '---', self.world.getEntitiesAt(random_pos, self.food_type, "plants") != [])
                self.loseEnergie('movement')
                finished = True
        
        if self.energie <= 0 or self.food_amount <= 0 or 0 > self.pos[0] or self.pos[0] > self.world.dimensions[0]-1 or 0 > self.pos[1] or self.pos[1] > self.world.dimensions[1]-1:
            self.kill()

    def getAroundFood(self) -> tuple:
        """ Return the direction to go to the nearest food """
        # Large vision
        if self.vision_type == 'large':
            closer_entity = None
            closer_distance = 0

            for entity in self.world.entities_dict[self.food_type]:
                if entity.pos != self.pos and self.pos[0] - self.vision_range < entity.pos[0] < self.pos[0] + self.vision_range and self.pos[1] - self.vision_range < entity.pos[1] < self.pos[1] + self.vision_range:
                    # Calculate the distance
                    distance = abs(self.pos[0]-entity.pos[0]) + abs(self.pos[1]-entity.pos[1])
                    if closer_entity == None:
                        closer_entity = entity
                        closer_distance = distance
                    elif distance < closer_distance: # Get nearest food
                        closer_entity = entity
                        closer_distance = distance

            if closer_entity != None:
                pos = closer_entity.pos
            else:
                pos = self.pos

            return pos

        # Restricted vision
        if self.vision_type == 'restricted':
            # left, right, top, down
            all_pos = [self.pos, self.pos, self.pos, self.pos]
            all_food_amount = [0,0,0,0]
            # print(self.category, self.type, self.pos)

            # Left
            for x in reversed(range(self.pos[0] - self.vision_range, self.pos[0])):
                pos = (x, self.pos[1])
                if self.world.getEntityAt(pos, self.food_type) != None and x > 0:
                    entity = self.world.getEntityAt(pos, self.food_type)
                    # print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| left')
                    all_pos[0] = pos
                    all_food_amount[0] = entity.food_amount
                    break
            
            # Right
            for x in range(self.pos[0], self.pos[0] + self.vision_range + 1):
                pos = (x, self.pos[1])
                if self.world.getEntityAt(pos, self.food_type) != None and x < self.world.dimensions[0]:
                    entity = self.world.getEntityAt(pos, self.food_type)
                    # print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| right')
                    all_pos[1] = pos
                    all_food_amount[1] = entity.food_amount
                    break

            # Top
            for y in reversed(range(self.pos[1] - self.vision_range, self.pos[1])):
                pos = (self.pos[0], y)
                if self.world.getEntityAt(pos, self.food_type) != None and y > 0:
                    entity = self.world.getEntityAt(pos, self.food_type)
                    # print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| top')
                    all_pos[2] = pos
                    all_food_amount[2] = entity.food_amount
                    break
            
            # Down
            for y in range(self.pos[1], self.pos[1] + self.vision_range + 1):
                pos = (self.pos[0], y)
                if self.world.getEntityAt(pos, self.food_type) != None and y < self.world.dimensions[1]:
                    entity = self.world.getEntityAt(pos, self.food_type)
                    # print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| down')
                    all_pos[3] = pos
                    all_food_amount[3] = entity.food_amount
                    break
            
            # Get the max of all sides
            max_food_amount = max(all_food_amount)
            pos = all_pos[all_food_amount.index(max_food_amount)]

            return pos
    
    def getAroundPartner(self) -> Entity:
        closer_partner = None
        closer_distance = 0

        for entity in self.world.entities_dict[self.type]:
            if entity.genre != self.genre and entity.type == self.type:
                if entity.pos != self.pos:
                    # Calculate the distance
                    distance = abs(self.pos[0]-entity.pos[0]) + abs(self.pos[1]-entity.pos[1])

                    if closer_partner == None: # Start
                        closer_partner = entity
                        closer_distance = distance
                    elif distance < closer_distance: # Get the nearest partner
                        closer_partner = entity
                        closer_distance = distance

        return closer_partner 

    def loseEnergie(self, action) -> None:
        """ Dicrease energie """
        if action == 'movement':
            self.energie -= choice(self.lose_energie)
        elif action == 'reproduction':
            self.energie -= self.reproduction_energie

    
