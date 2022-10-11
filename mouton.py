from random import randint

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
        x_right_grass = {'count': 0, 'pos': self.pos}
        x_left_grass = {'count': 0, 'pos': self.pos}
        y_top_grass = {'count': 0, 'pos': self.pos}
        y_down_grass = {'count': 0, 'pos': self.pos}

        x_range = (self.pos[0]-4, self.pos[0]+4)
        for herbe in self.monde.liste_herbe:
            if x_range[0] < herbe.pos[0] < x_range[1]:
                if herbe.pos[0] > self.pos[0]:
                    x_right_grass['count'] += 1

                    if x_right_grass['pos'][0] < herbe.pos[0]:
                        x_right_grass['pos'] = herbe.pos
                if herbe.pos[0] < self.pos[0]:
                    x_left_grass['count'] += 1

                    if x_left_grass['pos'][0] > herbe.pos[0]:
                        x_left_grass['pos'] = herbe.pos

        y_range = (self.pos[1]-4, self.pos[1]+4)
        for herbe in self.monde.liste_herbe:
            if y_range[0] < herbe.pos[1] < y_range[1]:
                if herbe.pos[1] < self.pos[1]:
                    y_top_grass['count'] += 1

                    if y_top_grass['pos'][1] > herbe.pos[1]:
                        y_top_grass['pos'] = herbe.pos
                if herbe.pos[1] > self.pos[1]:
                    y_down_grass['count'] += 1

                    if y_down_grass['pos'][1] < herbe.pos[1]:
                        y_down_grass['pos'] = herbe.pos

        print(x_left_grass, x_right_grass)
        print(y_top_grass, y_down_grass)
        
        if x_right_grass['count'] > x_left_grass['count']:
            return x_right_grass['pos']
        elif x_left_grass['count'] > x_right_grass['count']:
            return x_left_grass['pos']
        elif y_top_grass['count'] > y_down_grass['count']:
            return y_top_grass['pos']
        elif y_down_grass['count'] > y_top_grass['count']:
            return y_down_grass['pos']

        return self.pos

