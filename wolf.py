from random import randint

from entity import Entity


class Wolf(Entity):
    """ Wolf
    ---
    
    Attributes
        type : str
        world : World 
        pos : tuple
        reproduction_energie : int - 160
        max_energie : int - 200
        lose_energie : tuple - (10, 30)
        start_energie : int - random int between 80 and 130
        color : tuple
    """
    def __init__(self, pos, world) -> None:
        super().__init__(pos, world) 

        self.type = 'wolf'
        self.reproduction_energie = 250
        self.max_energie = 300
        self.lose_energie = (2, 8)
        self.start_energie = randint(80, 130)
        self.color = (0, 0, 0, 1)

    def action(self) -> None:
        """ Action : food, movement, reproduction """
        pass

    def getAroundSheep(self) -> tuple:
        """ Return the direction to go to the nearest sheep """
        return

