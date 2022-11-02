import pygame
import json

from settings import *

def get_font(font_size) -> pygame.font.SysFont:
    """ Return pygame Font object """
    return pygame.font.SysFont('Calibri', font_size) 


def show_bar(current, max_amount, bg_rect, color):
    """ Display bar depending on current value """
    display_surface = pygame.display.get_surface()

    # display bg_rect
    pygame.draw.rect(display_surface, (color[0]/2, color[1]/2, color[2]/2), bg_rect)
    
    # convert current value to pixel
    ratio = current / max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width

    # draw the bar
    pygame.draw.rect(display_surface, color, current_rect)


def write_json_file(path, data):
    json_object = json.dumps(data, indent=4)
    with open(path, 'w') as f:
        f.write(json_object)
    return data
