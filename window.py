from html import entities
import pygame
import json
import sys

from settings import *
from components import *
from support import write_json_file


class Window:
    """ Window
    --- 
    
    Artributes
        window_manager : WindowManager
        display_surface : pygame.Surface
        components : ComponentsGroup
    """
    def __init__(self, window_manager) -> None:
        pygame.init()

        # Setup
        self.window_manager = window_manager
        self.display_surface = self.window_manager.screen

        # Components
        self.components = ComponentsGroup()

    def event_management(self, event):
        pass

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_input = pygame.mouse.get_pressed()


class MainMenu(Window):
    def __init__(self, window_manager) -> None:
        super().__init__(window_manager)
        pygame.display.set_caption('Simulation - Main Menu')

        self.create_components()

    def create_components(self):
        ButtonBlockContainer(('centered', 'centered'), [self.components], [
            Text((0,0), [self.components], "Simulation", 40),
            Button((0,0), [self.components], "Launch Simulation", self.window_manager.launch_simulation_interface),
            Button((0,0), [self.components], "Create Entity", self.window_manager.launch_create_entity_form),
            Button((0,0), [self.components], "Manage Entity", self.window_manager.launch_manage_entities),
            Button((0,0), [self.components], "Quit", self.window_manager.quit_simulation)
        ], 20, 'in_column')

    def display(self):
        self.components.display()


class CreateEntityForm(Window):
    def __init__(self, window_manager) -> None:
        super().__init__(window_manager)
        pygame.display.set_caption('Simulation - New Entity')

        # Get entities data
        self.entities_data = json.load(open('data/entities.json'))

        # Get entity attributes type data and their info
        self.entity_attributes_type = json.load(open('data/menu/entity_attr_type.json'))
        self.attributes_type_info = json.load(open('data/menu/attr_type_info.json'))

        # Components
        self.specific_components = ComponentsGroup()
        self.input_components = {}
        self.entity_type = ""
        self.old_entity_type = ""

        self.create_components()

    def create_components(self):
        type_gap = 20
        component_gap = 10

        if self.entity_type == "":
            self.title_text = Text(('centered',20), [self.components], "New Entity", 30) # Title
            temp_back_text = Text((0,0), [], "Back") 
            temp_create_text = Text((0,0), [], "Create")
            temp_reset_text = Text((0,0), [], "Reset")
            self.back_button = Button((0,0), [self.components], "Back", self.window_manager.launch_main_menu, (SCREEN_WIDTH//6-40-temp_back_text.size[0]//2+10, 10)) # Back button
            self.create_button = Button((0,0), [self.components], "Create", self.create_entity, (SCREEN_WIDTH//6-40-temp_create_text.size[0]//2+10, 10), (0,255,150)) # Create button
            self.reset_button = Button((0,0), [self.components], "Reset", self.reset_form, (SCREEN_WIDTH//6-40-temp_reset_text.size[0]//2+10, 10)) # Reset button

            Container((40, SCREEN_HEIGHT-60), [self.components], [
                self.back_button,
                self.create_button,
                self.reset_button
            ], 40, 'inline') # Button container

            # Create all COMONS components for COMONS types of attributes
            pos = (40, 80)
            for attribute_name, attribute_type in self.entity_attributes_type.items():
                if type(attribute_type) != dict:
                    # Choice inputs
                    if attribute_name == 'category':
                        self.input_components[attribute_name] = ChoiceInput(pos, [self.components], ['mammals', 'plants'])
                    # Color inputs
                    elif attribute_type == 'color':
                        self.input_components[attribute_name] = ColorInput(pos, [self.components])
                    # Text and number inputs
                    else:
                        self.input_components[attribute_name] = Input(pos, [self.components], None, attribute_type.capitalize())

                    container = Container(pos, [self.components], [
                        Container(pos, [self.components], [
                            Text(pos, [self.components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                            InfoBox(pos, [self.components], self.attributes_type_info[attribute_name], (180,180,180))
                        ], 20, 'inline'),
                        self.input_components[attribute_name]
                    ], component_gap, 'in_column')

                    # Change pos
                    pos = (pos[0], pos[1] + container.size[1] + type_gap) 
        if self.entity_type == self.input_components['category'].value:
            # Delete old specific component 
            if self.old_entity_type != "":
                for entity_type, entity_attributes in self.entity_attributes_type.items():
                    if type(entity_attributes) == dict and self.old_entity_type == entity_type:
                        for attribute_name, attribute_type in entity_attributes.items():
                            if attribute_name in self.input_components:
                                print(attribute_name)
                                self.input_components.pop(attribute_name)
            self.specific_components = ComponentsGroup()

            # Create all SPECIFIC components for SPECIFIC types of attributes
            pos = (40*2+(SCREEN_WIDTH-160)//3, 80)
            for entity_type, entity_attributes in self.entity_attributes_type.items():
                if type(entity_attributes) == dict and self.entity_type == entity_type:
                    for attribute_name, attribute_type in entity_attributes.items():
                        # New column
                        if pos[1] > SCREEN_HEIGHT - 100:
                            pos = (pos[0]+40+(SCREEN_WIDTH-160)//3, 80)

                        # Choice inputs
                        if attribute_name == 'food_regime':
                            self.input_components[attribute_name] = ChoiceInput(pos, [self.specific_components], ['herbivore', 'carnivore'])
                        elif attribute_name == 'food_type':
                            self.input_components[attribute_name] = ChoiceInput(pos, [self.specific_components], [])
                        elif attribute_name == 'vision_type':
                            self.input_components[attribute_name] = ChoiceInput(pos, [self.specific_components], ['large', 'restricted'])
                        elif attribute_name == 'enemy_type':
                            self.input_components[attribute_name] = ChoiceInput(pos, [self.specific_components], [entity for entity in self.entities_data['mammals']])
                        # List inputs
                        elif type(attribute_type) == list:
                            self.input_components[attribute_name] = ListInput(pos, [self.specific_components], [Input(pos, [], None, input_type.capitalize()) for input_type in attribute_type])
                        # Text and number inputs
                        else:
                            self.input_components[attribute_name] = Input(pos, [self.specific_components], None, attribute_type.capitalize())
                        
                        container = Container(pos, [self.specific_components], [
                            Container(pos, [self.specific_components], [
                                Text(pos, [self.specific_components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                                InfoBox(pos, [self.specific_components], self.attributes_type_info[attribute_name], (180,180,180))
                            ], 20, 'inline'),
                            self.input_components[attribute_name]
                        ], component_gap, 'in_column')

                        # Change pos
                        pos = (pos[0], pos[1] + container.size[1] + type_gap)

    def create_entity(self):
        if self.entity_type != "" and self.input_components['type'] != "":

            # Collect all input values and converts
            entity_data = {}
            for attribute_name, attribute_type in self.entity_attributes_type.items():
                if attribute_name != 'category':
                    # Specific attributes
                    if type(attribute_type) == dict and self.entity_type == attribute_name:
                        for specific_attribute_name, specific_attribute_type in self.entity_attributes_type[attribute_name].items():
                            if specific_attribute_name != 'category':
                                input_component = self.input_components[specific_attribute_name]

                                # Convertion of all types of attributes
                                if type(specific_attribute_type) == list:
                                    entity_data[specific_attribute_name] = input_component.value
                                    for index, value_type in enumerate(specific_attribute_type):
                                        val = entity_data[specific_attribute_name][index]
                                        entity_data[specific_attribute_name][index] = int(val) if value_type == 'number' else val
                                elif type(specific_attribute_type) == str:
                                    if specific_attribute_type == 'number':
                                        entity_data[specific_attribute_name] = int(input_component.value)
                                    else:
                                        entity_data[specific_attribute_name] = input_component.value

                    # Comon attributes
                    if type(attribute_type) != dict:
                        input_component = self.input_components[attribute_name]

                        # Convertion of all types of attributes
                        if attribute_type == 'color':
                            print("COLOR", input_component.value, attribute_name, [int(v) for v in input_component.value])
                            entity_data[attribute_name] = [int(v) for v in input_component.value]
                        elif type(attribute_type) == list:
                            entity_data[attribute_name] = input_component.value
                            for index, value_type in enumerate(attribute_type):
                                val = entity_data[attribute_name][index]
                                entity_data[attribute_name][index] = int(val) if value_type == 'number' else val
                        elif type(attribute_type) == str:
                            if attribute_type == 'number':
                                entity_data[attribute_name] = int(input_component.value)
                            else:
                                entity_data[attribute_name] = input_component.value

            # Append new data into entities.json file
            entities_data = json.load(open('data/entities.json'))
            entities_data[self.input_components['category'].value][entity_data['type']] = entity_data
            write_json_file('data/entities.json', entities_data)

            self.reset_form()

    def reset_form(self):
        self.input_components = {}
        self.entity_type = ""
        self.components = ComponentsGroup()
        self.specific_components = ComponentsGroup()
        self.create_components()
            
    def display(self):
        super().update()

        # Update title text
        self.title_text.text = f"Create {self.input_components['type'].value.capitalize()} Entity" if self.input_components['type'].value != "" else "New Entity"
        self.title_text.update()

        # Update input component for get the new input value
        for attribute_name, input_component in self.input_components.items():
            if input_component.groups[0] == self.components:
                self.input_components[attribute_name] = self.components.components[self.components.components.index(input_component)]
            else:
                self.specific_components.components[self.specific_components.components.index(input_component)]

        # Change entity type
        if self.entity_type != self.input_components['category'].value:
            self.old_entity_type = self.entity_type
            self.entity_type = self.input_components['category'].value
            self.create_components()
        
        if self.entity_type == "mammals" and self.input_components['food_type'].choices == []:
            if self.input_components['food_regime'].value == 'herbivore':
                print([entity for entity in self.entities_data['plants']])
                self.input_components['food_type'].choices = [entity for entity in self.entities_data['plants']]
                self.input_components['food_type'].recreate_buttons()
            elif self.input_components['food_regime'].value == 'carnivore':
                print([entity for entity in self.entities_data['mammals']])
                self.input_components['food_type'].choices = [entity for entity in self.entities_data['mammals']]
                self.input_components['food_type'].recreate_buttons()
        self.specific_components.display()
        self.components.display()


class ManageEntities(Window):
    def __init__(self, window_manager) -> None:
        super().__init__(window_manager)

        # Get entities data
        self.entities_data = json.load(open('data/entities.json'))

        self.active_category = 'mammals'
        self.disabled_entities = json.load(open('data/disabled_entities.json'))['disabled']

        self.click_time = pygame.time.get_ticks()

        self.create_components()

    def create_components(self):
        self.components = ComponentsGroup()
        self.disable_buttons = ComponentsGroup()

        self.active_category_text = Text((0,0), [self.components], self.active_category.capitalize())
        
        # Main container
        Container(('centered', 20), [self.components], [
            Text([0,0], [self.components], "Manage Entities", 30),
            Button((0,0), [self.components], "Change Category", self.change_active_category, (20, 5)),
            self.active_category_text,
            ButtonBlockContainer((0,0), [self.components], [
                Box((0,0), [self.components], [
                    Text((0,0), [self.components], 
                    entity_name.capitalize(), 
                    None, 
                    (100,100,100) if entity_name in self.disabled_entities else entity_data['color']
                    ),
                    Button((0,0), [self.components, self.disable_buttons], 
                    "Enable" if entity_name in self.disabled_entities else "Disable", 
                    None, 
                    (10,5), 
                    (100,100,100) if entity_name in self.disabled_entities else entity_data['color'])
                ], 20, 'inline', (40, 10), (100,100,100) if entity_name in self.disabled_entities else entity_data['color']) for entity_name, entity_data in self.entities_data[self.active_category].items()
            ], 10, 'in_column')
        ], 20, 'in_column')

        # Bottom buttons
        temp_back_text = Text((0,0), [], "Back")
        self.back_button = Button((0,0), [self.components], "Back", self.window_manager.launch_main_menu, (SCREEN_WIDTH//6-40-temp_back_text.size[0]//2+10, 10)) # Back button
        temp_apply_text = Text((0,0), [], "Apply")
        self.apply_button = Button((0,0), [self.components], "Apply", self.apply_choice, (SCREEN_WIDTH//6-40-temp_apply_text.size[0]//2+10, 10)) # Apply button

        # Button container
        Container((40, SCREEN_HEIGHT-60), [self.components], [
            self.back_button,
            self.apply_button,
        ], 40, 'inline')

    def manage_button(self):
        current_time = pygame.time.get_ticks()
        for button in self.disable_buttons.components:
            if button.is_clicked and current_time - self.click_time >= 300:
                self.click_time = current_time
                entity_name = button.parent.components[0].text.lower() # get entity name from the text attributes of text Component

                # Update components
                if entity_name in self.disabled_entities:
                    self.disabled_entities.remove(entity_name)                    
                    self.create_components()
                else:
                    self.disabled_entities.append(entity_name)
                    self.create_components()

    def change_active_category(self):
        self.active_category = 'mammals' if self.active_category == 'plants' else 'plants'
        self.create_components()

    def apply_choice(self):
        write_json_file('data\disabled_entities.json', {'disabled': self.disabled_entities})
        self.window_manager.launch_main_menu()

    def display(self):
        self.manage_button()

        self.active_category_text.text = self.active_category.capitalize()
        self.active_category_text.update()

        self.components.display()
