import pygame
import numpy as np
from PIL import Image as PILImage
from scipy import ndimage
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


def rhombize(img: PILImage, h_angle: float = 0, v_angle: float = 0,):
    tans = np.tan(np.radians((v_angle, h_angle)))

    # Transform the old image size to the new image size
    size_transform = np.eye(2)
    size_transform[
        (0, 1),
        (1, 0),
    ] = np.abs(tans)
    new_size = img.size @ size_transform

    '''
    [ a b c ][ x ]   [ x']
    [ d e f ][ y ] = [ y']
    [ 0 0 1 ][ 1 ]   [ 1 ]
    '''
    shear = np.eye(2, 3)

    # Shift the x position based on the y position and vice versa
    shear[
        (1, 0),
        (0, 1),
    ] = tans

    # Shift the x and y positions everywhere; 
    # we need to be piecewise via clip() because in half of the cases
    # our origin needs to shift
    shear[(1, 0), 2] = np.clip(-tans * img.size, a_max=0, a_min=None)

    rhombised = img.transform(
        size=tuple(new_size.astype(int)),
        method=PILImage.AFFINE,
        data=shear.flatten(),
        # resample omitted - we don't really care about quality
    )

    return rhombised


# print(rhombize(PILImage.new('RGB', (TILE_SIZE, TILE_SIZE), (255,255,255)), 0, 30))
# rhombize(PILImage.new('RGB', (TILE_SIZE, TILE_SIZE), (0,0,0)), 0, 0.5).save('test/img_shear.png')


def create_iso_cube(size, color):
    faces = [PILImage.new('RGB', size, color) for i in range(3)]
    shear_val = [
                    [[1, 0, 0],
                    [0.5, 1, 0],
                    [0, 0, 1]],

                    [[1, 0.5, 0],
                    [0, 1, 0],
                    [0, 0, 1]],

                    [[1, 0, 0],
                    [0.5, 1, 0],
                    [0, 0, 1]]
    ]

    for index, image in enumerate(faces):
        array = np.array(image)

        height, width, colors = array.shape

        transform = [[1, 0, 0],
                    [0.5, 1, 0],
                    [0, 0, 1]]
        sheared_array = ndimage.affine_transform(array,
                                                shear_val[index],
                                                offset=(0, -height//2, 0),
                                                output_shape=(height, width+height//2, colors))

        img_out = PILImage.fromarray(sheared_array)
        img_out.save(f'test/shear-{index}.jpg')
        # image = image.resize((size[0], int(size[1] * 0.85)))
        # image.show()
        # image = rhombize(PILImage.fromarray(np.asarray(image)), 0, shear_val[index])
        # image.save(f'test/{index}_img_shear.png')


create_iso_cube((TILE_SIZE, TILE_SIZE), (255,0,0))