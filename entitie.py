from random import randint


class Entitie:
    """ Entities
    ---

    Attributes
        type : str
        monde : Monde
        pos : tuple
        reproduction_energie : int
        max_energie : int
        lose_energie : tuple 
        start_energie : int - random int between 80 and 130
        color : tuple
   """
    def __init__(self, pos, monde) -> None:
        self.type = None
        self.pos = pos
        self.monde = monde
        self.reproduction_energie = None
        self.max_energie = None
        self.lose_energie = None
        self.start_energie = randint(80, 130)
        self.color = None

    def getColor(self):
        """ Return color at rgba (int, int, int, int) """
        return self.color

    def dead(self):
        """ Destroy object """
        del self

    def loseEnergie(self) -> None:
        """ Dicrease energie """
        pass


