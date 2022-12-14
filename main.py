import sys

from settings import *
from components import *
from support import *
from interface import SimulationInterface
from window import *


class WindowManager:
    """ WindowManager
    ---

    Attributes
        status : str
        windows : dict
    """
    def __init__(self) -> None:
        pygame.init()

        # Setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.active_window = 'main_menu'
        self.windows = {
            'main_menu': MainMenu(self),
            'simulation_interface': SimulationInterface(self),
            'create_entity_form': CreateEntityForm(self),
            'manage_entities': ManageEntities(self),
            'help': Help(self),
        }
        self.windows[self.active_window].__init__(self)

    def change_window(self, window):
        self.active_window = window
        self.windows[self.active_window].__init__(self)
    
    def quit_simulation(self):
        pygame.quit()
        sys.exit()

    def launch_main_menu(self):
        self.change_window('main_menu')

    def launch_simulation_interface(self):
        self.change_window('simulation_interface')

    def launch_create_entity_form(self):
        self.change_window('create_entity_form')

    def launch_manage_entities(self):
        self.change_window('manage_entities')
    
    def launch_help(self):
        self.change_window('help')

    def run(self):
        while 1:
            for event in pygame.event.get():
                self.windows[self.active_window].event_management(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((30, 25, 25))

            self.windows[self.active_window].display()

            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    window_manager = WindowManager()
    window_manager.run()

