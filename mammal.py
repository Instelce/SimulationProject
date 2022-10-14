from random import randint, choice

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
        food_taken : int - food that the mammal takes per mouthful

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
        super().__init__(type, pos, world, color)
        self.category = 'mammals'
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

    def action(self):
        """ Actions : food, movement, escape, reproduction """
        self.target_food_pos = self.pos
        finished = False

        # Food
        if self.energie < self.max_energie:
            if self.world.getEntityAt(self.pos, self.food_type) != None:
                entity = self.world.getEntityAt(self.pos, self.food_type)
                if entity.food_amount > 0:
                    self.energie += self.energie_per_food_taken
                    entity.food_amount -= self.food_taken

                    finished = True
                elif entity.food_amount <= 0:
                    entity.kill()

        # Movement
        if self.energie > 0:
            if self.target_food_pos == self.pos:
                self.target_food_pos = self.getAroundFood()
            
            if self.target_food_pos != self.pos:
                x_move = self.pos[0] - self.target_food_pos[0]
                y_move = self.pos[1] - self.target_food_pos[1]

                if x_move > 0:
                    x = -1
                    y = 0
                elif x_move < 0:
                    x = 1
                    y = 0
                else:
                    x = 0
                    y = 0
            
                if y_move > 0 and x == 0 and x_move == 0:
                    x = 0
                    y = -1
                elif y_move < 0 and x == 0 and x_move == 0:
                    x = 0
                    y = 1

                self.pos = (self.pos[0] + x, self.pos[1] + y)
                print("MOVE", x_move, y_move, '---', x, y)
                self.loseEnergie()
                finished = True
            # else:
            #     self.pos = (self.pos[0] + randint(-1, 1), self.pos[1])
            #     self.pos = (self.pos[0], self.pos[1] + randint(-1, 1))

            #     self.loseEnergie()
            #     finished = True
        else:
            self.kill()

    def getAroundFood(self) -> tuple:
        """ Return the direction to go to the nearest food """
        # left, right, top, down
        all_pos = [self.pos, self.pos, self.pos, self.pos]
        all_food_amount = [0,0,0,0]
        print(self.category, self.type, self.pos)

        # Left
        for x in reversed(range(self.pos[0] - self.vision_range, self.pos[0])):
            pos = (x, self.pos[1])
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| left')
                all_pos[0] = pos
                all_food_amount[0] = entity.food_amount
                break
        
        # Right
        for x in range(self.pos[0], self.pos[0] + self.vision_range + 1):
            pos = (x, self.pos[1])
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| right')
                all_pos[1] = pos
                all_food_amount[1] = entity.food_amount
                break

        # Top
        for y in reversed(range(self.pos[1] - self.vision_range, self.pos[1])):
            pos = (self.pos[0], y)
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| top')
                all_pos[2] = pos
                all_food_amount[2] = entity.food_amount
                break
        
        # Down
        for y in range(self.pos[1], self.pos[1] + self.vision_range + 1):
            pos = (self.pos[0], y)
            if self.world.getEntityAt(pos, self.food_type) != None:
                entity = self.world.getEntityAt(pos, self.food_type)
                print(">>>", self.pos, '--', entity.pos, '--', entity.type, '| down')
                all_pos[3] = pos
                all_food_amount[3] = entity.food_amount
                break
            
        max_food_amount = max(all_food_amount)
        max_pos = all_pos[all_food_amount.index(max_food_amount)]

        return max_pos
    
    def loseEnergie(self) -> None:
        """ Dicrease energie """
        self.energie -= choice(self.lose_energie)

    
