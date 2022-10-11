from random import randint

from entitie import Entitie


class Loup(Entitie):
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
        color : tuple
    """
    def __init__(self, pos, monde) -> None:
        super().__init__(pos, monde)

        self.type = 'loup'
        self.reproduction_energie = 250
        self.max_energie = 300
        self.lose_energie = (2, 8)
        self.start_energie = randint(80, 130)
        self.color = (100, 100, 100, 1)

    def action(self) -> None:
        """ Action : food, movement, reproduction """
        pass

    def getAroundMouton(self) -> tuple:
        """ Return the direction to go to the nearest sheep """
        return

