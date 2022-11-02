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

        # Get entity attributes type data
        self.entity_attributes_type = json.load(open('data/menu/entity_attr_type.json'))

        # Components
        self.input_components = {}
        self.entity_type = ""

        self.create_components()

    def create_components(self):
        type_gap = 20
        component_gap = 10

        if self.entity_type == "":
            self.title_text = Text(('centered',20), [self.components], f"New Entity", 30) # Title
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

            # Common attributes
            pos = (40, 80)
            for attribute_name, attribute_type in self.entity_attributes_type.items():
                if type(attribute_type) != dict:
                    if attribute_type == 'color':
                        self.input_components[attribute_name] = ColorInput(pos, [self.components])
                        container = Container(pos, [self.components], [
                            Text(pos, [self.components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                            self.input_components[attribute_name]
                        ], component_gap, 'in_column')
                        pos = (pos[0], pos[1] + container.size[1] + type_gap) # Change pos
                    else:
                        self.input_components[attribute_name] = Input(pos, [self.components], None, attribute_type.capitalize())
                        container = Container(pos, [self.components], [
                            Text(pos, [self.components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                            self.input_components[attribute_name]
                        ], component_gap, 'in_column')
                        pos = (pos[0], pos[1] + container.size[1] + type_gap) # Change pos
        else:
            # Specific attributes
            pos = (40*2+(SCREEN_WIDTH-160)//3, 80)
            for entity_type, entity_attributes in self.entity_attributes_type.items():
                if type(entity_attributes) == dict and self.entity_type == entity_type:
                    for attribute_name, attribute_type in entity_attributes.items():
                        if pos[1] > SCREEN_HEIGHT - 100:
                            pos = (pos[0]+40+(SCREEN_WIDTH-160)//3, 80)

                        if type(attribute_type) == list:
                            self.input_components[attribute_name] = ListInput(pos, [self.components], [Input(pos, [], None, input_type.capitalize()) for input_type in attribute_type])
                            container = Container(pos, [self.components], [
                                Text(pos, [self.components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                                self.input_components[attribute_name]
                            ], component_gap, 'in_column')
                            pos = (pos[0], pos[1] + container.size[1] + type_gap)
                        else:
                            self.input_components[attribute_name] = Input(pos, [self.components], None, attribute_type.capitalize())
                            container = Container(pos, [self.components], [
                                Text(pos, [self.components], attribute_name.replace('_', ' ').upper(), 12, (180,180,180)),
                                self.input_components[attribute_name]
                            ], component_gap, 'in_column')
                            pos = (pos[0], pos[1] + container.size[1] + type_gap)

    def create_entity(self):
        if self.entity_type != "" and self.input_components['type'] != "":

            # Collect all input value
            entity_data = {}
            for attribute_name, attribute_type in self.entity_attributes_type.items():
                if attribute_name != 'category':
                    if type(attribute_type) == dict and self.entity_type == attribute_name:
                        for specific_attribute_name, specific_attribute_type in self.entity_attributes_type[attribute_name].items():
                            print(specific_attribute_name, specific_attribute_type)
                            if specific_attribute_name != 'category':
                                input_component = self.input_components[specific_attribute_name]

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
                    if type(attribute_type) != dict:
                        input_component = self.input_components[attribute_name]
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
            print(entity_data)
            entities_data = json.load(open('data/entities.json'))
            entities_data[self.input_components['category'].value][entity_data['type']] = entity_data
            write_json_file('data/entities.json', entities_data)

            self.reset_form()

    def reset_form(self):
        self.input_components = {}
        self.entity_type = ""
        self.components = ComponentsGroup()
        self.create_components()
            
    def display(self):
        super().update()

        self.title_text.text = f"Create {self.input_components['type'].value.capitalize()} Entity" if self.input_components['type'].value != "" else "New Entity"
        self.title_text.update()

        # Update input component
        for attribute_name, input_component in self.input_components.items():
            self.input_components[attribute_name] = self.components.components[self.components.components.index(input_component)]

        # Check the category input value
        if self.entity_type == "":
            if self.input_components['category'].value == 'plants':
                self.entity_type = 'plants'
            elif self.input_components['category'].value == 'mammals':
                self.entity_type = 'mammals'

            if self.entity_type != "":
                self.create_components()

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

        self.entities_container = ButtonBlockContainer((0,0), [self.components], [
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
        
        Container(('centered', 20), [self.components], [
            Text([0,0], [self.components], "Manage Entities", 30),
            Button((0,0), [self.components], "Change Category", self.change_active_category, (20, 5)),
            self.active_category_text,
            self.entities_container
        ], 20, 'in_column')

        # Buttons
        temp_back_text = Text((0,0), [], "Back")
        self.back_button = Button((0,0), [self.components], "Back", self.window_manager.launch_main_menu, (SCREEN_WIDTH//6-40-temp_back_text.size[0]//2+10, 10)) # Back button
        temp_apply_text = Text((0,0), [], "Apply")
        self.apply_button = Button((0,0), [self.components], "Apply", self.apply_choice, (SCREEN_WIDTH//6-40-temp_apply_text.size[0]//2+10, 10)) # Apply button

        Container((40, SCREEN_HEIGHT-60), [self.components], [
            self.back_button,
            self.apply_button,
        ], 40, 'inline') # Button container

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