
class Herbe:
    """ Herbe
    ---

    Attributes
        type : str
        pos : tuple
        max_repousse : int - 100
        amount : int
        color_base : int - (52, 140, 49)
        color_mod : (int, int, int) - rgb color
        plein_depuis : int
    """
    def __init__(self, pos, amount, color_mod, plein_depuis) -> None:
        self.type = 'herbe'
        self.pos = pos
        self.max_repousse = 100
        self.amount = amount
        self.color_base = (52, 140, 49)
        self.color_mod = color_mod
        self.plein_depuis = plein_depuis

    def action(self) -> None:
        pass

    def getColor(self):
        """ Return color (int, int, int)"""
        return self.color_base

    def dead(self) -> None:
        """ Destroy object """
