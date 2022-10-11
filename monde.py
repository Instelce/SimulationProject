from random import randint

from herbe import Herbe
from mouton import Mouton


class Monde:
    """ Monde
    ---

    Attributes
        dimention : tuple
        liste_herbe : list
        liste_loup : list
        liste_mouton : list
    """
    def __init__(self, dimensions):
        self.dimensions = dimensions

        self.liste_herbe = []
        self.liste_loup = []
        self.liste_mouton = []

    def iteration(self) -> None:
        """ Itaration of world"""
        pass

    def getHerbeAt(self, position) -> Herbe or None:
        """ Return None or Herbe object """
        for herbe in self.liste_herbe:
            if herbe.pos == position:
                return herbe
        return None

    def getEntitiesAt(self, position) -> list:
        """ entitie at position """
        return []

    def generate(self, entitie, pourcentage) -> None:
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if randint(0, 100) <= pourcentage: # Can generate
                    if entitie == 'herbe':
                        self.liste_herbe.append(Herbe((x,y), randint(1,5), (52, 140, 49), 0))
                    if entitie == 'mouton':
                        self.liste_mouton.append(Mouton((x,y), self))
                        

