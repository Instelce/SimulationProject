from herbe import Herbe


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

    def getHerbeAt(self, position) -> Herbe:
        """ Return None or Herbe object """
        for herbe in self.liste_herbe:
            if herbe.pos == position:
                return herbe
        return None

    def getEntitiesAt(self, position) -> list:
        """ Create entitie at position """
        return []

    def generate(self, entitie, pourcentage) -> None:
        pass