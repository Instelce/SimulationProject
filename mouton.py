from random import randint


class Mouton:
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
    """
    def __init__(self, pos, monde) -> None:
        self.type = 'mouton'
        self.pos = pos
        self.monde = monde
        self.reproduction_energie = 160
        self.max_energie = 200
        self.lose_energie = (10, 30)
        self.start_energie = randint(80, 130)

    def action(self) -> None:
        """ Action of mouton """
        pass

    def getColor(self):
        """ Return color (int, int, int, int) """
        return (0, 200, 200, 1)

    def getAroundHerbe(self) -> tuple:
        """ Return the direction to go to the nearest herbs """
        return 

    def dead(self):
        """ Destroy object """
        del self

    def loseEnergie(self) -> None:
        """ Dicrease energie """
        pass