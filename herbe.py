
class Herbe:
    """ Herbe
    ---

    Attributes
        type : str
        pos : tuple
        max_repousse : int - 100
        quantitee : int
        color_base : int - (52, 140, 49)
        color_mod : (int, int, int)
        plein_depuis : int
    """
    def __init__(self, nom, pos, quantitee, color_mod, plein_depuis, max_repousse=100, color_base=(52, 140, 49)) -> None:
        self.type = 'herbe'
        self.pos = pos
        self.max_repousse = max_repousse
        self.quantitee = quantitee
        self.color_base = color_base
        self.color_mod = color_mod
        self.plein_depuis = plein_depuis

    def action(self) -> None:
        pass

    def get_color(self):
        """ Return color (int, int, int)"""
        return

    def dead(self) -> None:
        """ Destroy object """