import pygame
import string

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class ComponentsGroup:
    """ Group for components
    
    args:
        components : list
    """
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def remove(self, component):
        self.components.remove(component)
    
    def remove_all(self):
        for component in self.components:
            self.remove(component)
        
    def delete_all(self):
        for component in self.components:
            component.delete()

    def inline(self, start_pos, gap, component_index=0):
        """ Repositioning components inline """
        component = self.components[component_index]
        component.pos = (start_pos[0], start_pos[1])
        component.update()

        if not component_index == len(self.components)-1:
            return self.inline((start_pos[0] + component.size[0] + gap, start_pos[1]), gap, component_index+1)

    def display(self):
        for component in self.components:
            component.display()


class Component:
    """ Component object for menu
    
    args:
        pos : tuple
        font : Object
        groups : list
    """
    def __init__(self, pos, groups):
        self.pos = pos
        self.groups = groups
        self.display_surface = pygame.display.get_surface()

        if self.groups is not []:
            for group in self.groups:
                group.add(self)

        self.font = pygame.font.SysFont('calibri', 18)
    
    def delete(self):
        for group in self.groups:
            group.remove(self)
        del(self)

    def display(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_input = pygame.mouse.get_pressed()


class Container(Component):
    """ Container
    ---

    Display component inline or in column
    
    args:
        pos : tuple
        groups : list
        components : list
        gap : int
        display_method : string
            'inline' or 'in_block'
    """
    def __init__(self, pos, groups, components, gap, display):
        super().__init__(pos, groups)
        self.components = components
        self.gap = gap
        self.display_method = display

        # Get size
        self.size = [0,0]
        max_component_size = 0
        for component in self.components:
            if self.display_method == 'inline':
                # Get the biggest component size
                if component.size[1] > max_component_size:
                    max_component_size = component.size[1]

                self.size[0] += (component.size[0] + self.gap)
                self.size[1] = max_component_size
            if self.display_method == 'in_column':
                # Get the biggest component size
                if component.size[0] > max_component_size:
                    max_component_size = component.size[0]

                self.size[0] = max_component_size
                self.size[1] += (component.size[1] + self.gap)
            print(component.size, self.gap, component.size[0] + self.gap)
            print(self.size)

        self.is_centered = False
        if self.pos == 'centered':
            self.pos = (SCREEN_WIDTH/2-self.size[0]/2, SCREEN_HEIGHT/2-self.size[1]/2)
            self.is_centered = True

        # Call display method
        if self.display_method == 'in_column':
            self.in_column(self.pos, self.gap)
        else:
            self.inline(self.pos, self.gap)
    
    def add(self, component):
        self.components.append(component)

    def remove(self, component):
        self.components.remove(component)

    def in_column(self, start_pos, gap, component_index=0):
        """ Repositioning components in column """
        component = self.components[component_index]

        if self.is_centered:
            gap_component = (self.size[0] - component.size[0])/2
        else:
            gap_component = 0

        component.pos = (start_pos[0] + gap_component, start_pos[1])
        component.update()

        if not component_index == len(self.components)-1:
            return self.in_column((start_pos[0], start_pos[1] + component.size[1] + gap), gap, component_index+1)

    def inline(self, start_pos, gap, component_index=0):
        """ Repositioning components inline """
        component = self.components[component_index]
        component.pos = start_pos
        component.update()

        if not component_index == len(self.components)-1:
            return self.inline((start_pos[0] + component.size[0] + gap, start_pos[1]), gap, component_index+1)
    
    def update(self):
        pass

    def display(self):
        super().display()

        # Call display method
        if self.display_method == 'in_column':
            self.in_column(self.pos, self.gap)
        else:
            self.inline(self.pos, self.gap)

        for component in self.components:
            component.display()

        # pygame.draw.rect(self.display_surface, "red", pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]), 1)


# ------------------------------------------
# Button components
# ------------------------------------------

class Button(Component):
    """ Button 
    
    args:
        text : string
        callback : function
        padding : tuple
        color : tuple
    """
    def __init__(self, pos, groups, text, callback=None, padding=None, color=None):
        super().__init__(pos, groups)
        self.type = "button"
        self.text = text
        self.callback = callback
        self.padding = padding if padding is not None else (40,10)
        self.color = color if color is not None else (255,255,255)

        # Create text
        self.text_surf = self.font.render(self.text, False, self.color)

        text_rect_temp = self.text_surf.get_rect(center=(0,0))
        self.size = (text_rect_temp.width+(self.padding[0]*2), text_rect_temp.height+(self.padding[1]*2))
        self.border = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.fill = pygame.Rect(self.pos[0], self.pos[1], self.border.width, 0)
        self.fill_height = 0

        self.text_rect = self.text_surf.get_rect(center=(self.border.center))

        # Interactions
        self.is_clicked = False
        self.is_overflown = False

    def check_interactions(self):
        """ Hover, click """

        # Hover
        if self.border.collidepoint(self.mouse_pos):
            self.is_overflown = True 

            # Click
            if self.mouse_input[0]:
                self.is_clicked = True

                if self.callback is not None:
                    self.callback()
            else:
                self.is_clicked = False
        else:
            self.is_overflown = False

    def update(self):
        """ Update every arguments """
        self.border = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.fill = pygame.Rect(self.pos[0], self.pos[1], self.border.width, 0)
        self.text_surf = self.font.render(self.text, False, self.color)
        self.text_rect = self.text_surf.get_rect(center=(self.border.center))
        self.size = (self.text_rect.width+(self.padding[0]*2), self.text_rect.height+(self.padding[1]*2))
    
    def display(self):
        super().display()
        self.check_interactions()

        # Animation on hover
        if self.is_overflown:
            self.text_surf = self.font.render(self.text, False, (0,0,0))

            if self.fill_height <= self.border.height:
                self.fill_height += 5
        else:
            self.text_surf = self.font.render(self.text, False, self.color)

            if self.fill_height > 0:
                self.fill_height -= 5

        # Display border
        if self.is_clicked:
            pygame.draw.rect(self.display_surface, self.color, self.border, 2)
        else:
            pygame.draw.rect(self.display_surface, self.color, self.border, 1)

        # Display fill
        if self.is_overflown:
            self.fill = pygame.Rect(self.pos[0], self.pos[1], self.border.width, self.fill_height) # Update fill
        else:
            self.fill = pygame.Rect(self.pos[0], self.pos[1]-self.fill_height+self.border.height, self.border.width, self.fill_height) # Update fill
            
        pygame.draw.rect(self.display_surface, self.color, self.fill)

        # Display text
        self.display_surface.blit(self.text_surf, self.text_rect)


# ------------------------------------------
# Image components
# ------------------------------------------

class Image(Component):
    """ Image
    
    args:
        surface : Surface
        scale : tuple
            default surface size
    """
    def __init__(self, pos, groups, surface, scale=None):
        super().__init__(pos, groups)
        self.type = "image"
        self.scale = scale if scale is not None else surface.get_size()
        self.surface = surface
        self.surface_scaled = pygame.transform.scale(surface, self.scale)
        
        self.size = self.surface.get_size()
        self.rect = self.surface.get_rect(topleft=self.pos)

    def alpha(self, alpha):
        self.surface.set_alpha(alpha)

    def update(self):
        self.surface_scaled = pygame.transform.scale(self.surface, self.scale)
        self.size = self.surface_scaled.get_size()
        self.rect = self.surface_scaled.get_rect(topleft=self.pos)

    def display(self):
        super().display()
        self.display_surface.blit(self.surface_scaled, self.rect)


class ImageButton(Component):
    """ Image Button 
    
    args:
        image : Surface
        callback : function
        color : tuple
    """
    def __init__(self, pos, groups, image, callback=None, color=None):
        super().__init__(pos, groups)
        self.type = "image_button"
        self.image = image
        self.callback = callback
        self.color = color if color is not None else (255,255,255)

        self.border = pygame.Rect(self.pos[0], self.pos[1], self.image.get_size()[0]+5, self.image.get_size()[1]+5)
        self.size = (self.border.width, self.border.height)

        # Interactions
        self.is_clicked = False
        self.is_overflown = False

    def check_interactions(self):
        """ Hover, click """

        # Hover
        if self.border.collidepoint(self.mouse_pos):
            self.is_overflown = True 

            # Click
            if self.mouse_input[0]:
                self.is_clicked = True

                if self.callback is not None:
                    self.callback()
            else:
                self.is_clicked = False
        else:
            self.is_overflown = False

    def update(self):
        self.border = pygame.Rect(self.pos[0], self.pos[1], self.image.get_size()[0]+5, self.image.get_size()[1]+5)
        self.size = (self.border.width, self.border.height)
    
    def display(self):
        super().display()
        self.check_interactions()

        # Display border
        if self.is_overflown:
            pygame.draw.rect(self.display_surface, self.color, self.border, 2)
        else:
            pygame.draw.rect(self.display_surface, self.color, self.border, 1)

        # Display image
        self.display_surface.blit(self.image, (self.border.centerx-self.image.get_size()[0]/2+1, self.border.centery-self.image.get_size()[1]/2+1))


# ------------------------------------------
# Text components
# ------------------------------------------

class Text(Component):
    """ Text

    args:
        text : string or int
        color : tuple
            default (255,255,255)
        text_size : int
            default 18
    """
    def __init__(self, pos, groups, text, size=None, color=None):
        super().__init__(pos, groups)
        self.type = "text"
        self.text = text
        self.text_size = size if size is not None else 18
        self.color = color if color is not None else (255,255,255)

        self.font = pygame.font.SysFont('calibri', self.text_size)
        self.surf = self.font.render(str(text), False, self.color)
        self.rect = self.surf.get_rect(topleft=self.pos)
        self.size = (self.rect.width, self.rect.height)

    def update(self):
        self.surf = self.font.render(str(self.text), False, self.color)
        self.rect = self.surf.get_rect(topleft=self.pos)
        self.size = (self.rect.width, self.rect.height)

    def display(self):
        super().display()
        self.display_surface.blit(self.surf, self.rect)


class TextInput(Component):
    """ Text input

    args:
        value : string
        placeholder : string
        color : tuple

        focus : bool
        size : tuple
    """
    def __init__(self, pos, groups, value=None, placeholder=None, padding=None, color=None):
        super().__init__(pos, groups)
        self.type = "text_input"
        self.value = value if value is not None else ""
        self.placeholder = placeholder if placeholder is not None else ""
        self.padding = padding if padding is not None else (10,5)
        self.color = color if color is not None else (0,0,0)
        
        self.focus = False

        # Text
        if len(self.value) > 0:
            self.value_surf = self.font.render(self.value, True, (255,255,255))
        else:
            self.value_surf = self.font.render(self.placeholder, True, (255,255,255))

        temp_value_rect = self.value_surf.get_rect()
        self.size = (temp_value_rect.width+(self.padding[0]*2), temp_value_rect.height+(self.padding[1]*2))
        self.border = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.cursor = pygame.Rect(self.pos[0]+len(self.value)*5, self.pos[1], 1, self.font.get_height())

        self.keypress_cooldown = 150
        self.keypress_time = pygame.time.get_ticks()

        self.get_caracters()
        
    def get_caracters(self):
        """ Gets all caracters and their keycode """
        self.letters = list(string.printable)
        self.special_caracters = "&é\"'(-è_çà"
        self.number_caracters = "1234567890"

        self.keys_keycode = {}

        for letter in self.letters:
            self.keys_keycode[letter] = pygame.key.key_code(letter)

    def check_focus(self):
        """ Update focus """
        if self.border.collidepoint(self.mouse_pos):
            if self.mouse_input[0]:
                self.focus = True
                self.color = (255,255,255)
            if not self.focus:
                self.color = (60,60,60)
        else:
            if self.mouse_input[0]:
                self.focus = False
                self.color = (20,20,20)
            if not self.focus:
                self.color = (20,20,20)

    def get_keypressed(self):
        """ Append keypress on value """
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.focus:
            for keycode in self.keys_keycode:
                if keys[self.keys_keycode[keycode]] and current_time - self.keypress_time >= self.keypress_cooldown:
                    self.keypress_time = current_time
                    if 49 <= self.keys_keycode[keycode] <= 61:
                        if keys[pygame.K_LSHIFT]: # Numbers
                            self.value += pygame.key.name(self.keys_keycode[keycode])
                        else: # Special caracters
                            index = abs(61-(int(keycode)+61))-1
                            self.value += self.special_caracters[index]
                    elif keys[pygame.K_LSHIFT]: # Capitalize
                        self.value += pygame.key.name(self.keys_keycode[keycode]).upper()
                    else: # Normal
                        self.value += pygame.key.name(self.keys_keycode[keycode])

                if keys[pygame.K_BACKSPACE] and current_time - self.keypress_time >= self.keypress_cooldown: # Remove caracters
                    self.keypress_time = current_time
                    self.value = self.value[:-1]
                if keys[pygame.K_SPACE] and current_time - self.keypress_time >= self.keypress_cooldown: # Space
                    self.keypress_time = current_time
                    self.value += ' '
                if keys[pygame.K_RETURN] and current_time - self.keypress_time >= self.keypress_cooldown:
                    self.keypress_time = current_time
                    self.value += ''
                    self.focus = False

    def update(self):
        self.text_size = ((len(self.value)*5)+20, self.font.get_height()+10) 
        self.border = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.value_rect = self.value_surf.get_rect(center=self.border.center)
        self.size = (self.value_rect.width+(self.padding[0]*2), self.value_rect.height+(self.padding[1]*2))

        if len(self.value) > 0:
            self.value_surf = self.font.render(self.value, True, (255,255,255))
        else:
            self.value_surf = self.font.render(self.placeholder, True, (255,255,255))

    def display(self):
        super().display()
        self.check_focus()
        self.get_keypressed()
        self.update()

        text_size = self.value_surf.get_size()
        self.value_rect = self.value_surf.get_rect(center=self.border.center)
        cursor_pos = (self.value_rect.topright[0] + 1, self.value_rect.topright[1]) 

        # Display input
        pygame.draw.rect(self.display_surface, self.color, self.border, 1)
        self.display_surface.blit(self.value_surf, self.value_rect)

        # Update and display cursor
        if self.focus and len(self.value) > 0:
            self.cursor = pygame.Rect(cursor_pos[0], cursor_pos[1], 1, self.font.get_height())
            pygame.draw.rect(self.display_surface, self.color, self.cursor, 2)


        


