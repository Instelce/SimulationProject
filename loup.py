from random import randint


class Loup:
    """ Loup
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
    def __init__(self, monde, pos) -> None:
        self.type = 'loup'
        self.monde = monde
        self.pos = pos
        self.reproduction_energie = 250
        self.max_energie = 300
        self.lose_energie = (2, 8)
        self.start_energie = randint(80, 130)
    
    def action(self) -> None:
        """ Action : food, movement, reproduction """
        pass

    def getColor(self):
        """ Return color (int, int, int, int) """
        return (100, 100, 100, 1)

    def getAroundMouton(self) -> tuple:
        """ Return the direction to go to the nearest sheep """
        return

    def dead(self):
        """ Destroy object """
        del self

    def loseEnergie(self) -> None:
        pass