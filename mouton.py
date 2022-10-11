from random import randint

from numpy import ma

from entitie import Entitie


class Mouton(Entitie):
    """ Mouton
    ---

    Attributes
        type : str
        monde : Monde
        pos : tuple
        reproduction_energie : int - 160
        max_energie : int - 200
        lose_energie : tuple - (10, 30)
        start_energie : int - random int between 80 and 130
        color : tuple
    """
    def __init__(self, pos, monde) -> None:
        super().__init__(pos, monde)

        self.type = 'mouton'
        self.reproduction_energie = 160
        self.max_energie = 200
        self.lose_energie = (10, 30)
        self.start_energie = randint(80, 130)
        self.color = (100, 100, 100, 1)

    def action(self) -> None:
        """ Action : food, movement, reproduction """
        pass

    def getAroundHerbe(self) -> tuple:
        """ Return the direction to go to the nearest herbs """
        self.sides = {
            'x_right': {'amount': 0, 'pos': self.pos},
            'x_left': {'amount': 0, 'pos': self.pos},
            'y_top': {'amount': 0, 'pos': self.pos},
            'y_down': {'amount': 0, 'pos': self.pos},
        }

        x_range = (self.pos[0]-4, self.pos[0]+4)
        for x in range(x_range[0], x_range[1]):
            if self.monde.getHerbeAt((x, self.pos[1])) != None:
                herbe = self.monde.getHerbeAt((x, self.pos[1]))
                if herbe.pos[0] > self.pos[0]:
                    self.sides['x_right']['amount'] = herbe.amount
                    if self.sides['x_right']['pos'][0] < herbe.pos[0]:
                        self.sides['x_right']['pos'] = herbe.pos
                if herbe.pos[0] < self.pos[0]:
                    self.sides['x_left']['amount'] = herbe.amount
                    if self.sides['x_left']['pos'][0] > herbe.pos[0]:
                        self.sides['x_left']['pos'] = herbe.pos

        y_range = (self.pos[1]-4, self.pos[1]+4)
        for y in range(y_range[0], y_range[1]):
            if self.monde.getHerbeAt((self.pos[0], y)) != None:
                herbe = self.monde.getHerbeAt((self.pos[0], y))
                if herbe.pos[1] > self.pos[1]:
                    self.sides['y_top']['amount'] = herbe.amount
                    if self.sides['y_top']['pos'][1] > herbe.pos[1]:
                        self.sides['y_top']['pos'] = herbe.pos
                if herbe.pos[1] < self.pos[1]:
                    self.sides['y_down']['amount'] = herbe.amount
                    if self.sides['y_down']['pos'][1] < herbe.pos[1]:
                        self.sides['y_down']['pos'] = herbe.pos

        # print(x_left_grass, x_right_grass)
        # print(y_top_grass, y_down_grass)
        
        all_side_amount = {self.sides['x_right']['amount']: 'x_right', self.sides['x_left']['amount']: 'x_left', self.sides['y_top']['amount']: 'y_top', self.sides['y_down']['amount']: 'y_down'}
        self.max_side = all_side_amount.get(max(all_side_amount))

        return self.sides[self.max_side]['pos']
