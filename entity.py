from random import randint, choice


class Entity:
    """ Entity 
    ---
    
    Attributes
        type : str
        pos : tuple
        world : World
        color : tuple
    """
    def __init__(self, type, pos, world, color) -> None:
        self.type = type
        self.pos = pos
        self.world = world
        self.color = color

    def __repr__(self) -> str:
        return str(self.__dict__)

    def getColor(self):
        """ Return color at rgb (int, int, int) """
        return self.color

    def kill(self):
        """ Destroy entity """
        print(f"{self.type} entity is dead ...")
        self.world.entities_dict[self.type].remove(self)
        del self



