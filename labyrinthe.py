#! /usr/bin/env python3
# coding: utf-8


'''This is the main module. It contains the main function
that enables gameplay loop. It also initializes display window.
'''


import json
import random
import pygame
from pygame.locals import *



pygame.init() #enables sprite initialization during Display class declaration
WINDOW = pygame.display.set_mode((750, 750))

class Macgyver:
    '''The MacGyver class represents the player-controlled character
    It handles movement, item pick-up, item storage, and game over
    '''

    def __init__(self, startPos):
        '''Constructor spawns the character at a given square on the grid'''
        self.position = startPos
        self.items = []
        self.current_square.content = 6

    @property
    def current_square(self):
        '''Syntactic sugar'''
        return GameController.SQUARE_ARRAY[self.position]


    ### SQUARE INTERACTION ###

    def touch_square(self):
        '''Triggers various events when the character enters an occupied square
        Items will be added to inventory
        Encounter with the warden results in either victory or defeat'''
        new_square = self.current_square
        if new_square.content == 1:
            GameController.RUNNING = False
            GameController.GAME_OVER = True

            if len(self.items) == 3:
                Display.STATE = "Victory"

            else:
                Display.STATE = "Defeat"
                
            pygame.display.flip()

        elif new_square.content in (2, 3, 4):
            self.add_item(new_square.content)

    def add_item(self, content_id):
        '''Reads entered square's content and add corresponding item to array'''
        switcher = {
            2: "needle",
            3: "pipe",
            4: "ether"
        }
        self.items.append(switcher.get(content_id, "invalid content_id"))


    ### MOVEMENT ###

    def move_right(self):
        '''Checks grid borders using square logic, then check walls
        Moves the character using square id logic if all clear'''
        if self.current_square.x_pos < 14:
            next_position = self.position + 1
            if GameController.SQUARE_ARRAY[next_position].content != 5:
                self.position = next_position

    def move_up(self):
        '''Same as above'''
        if self.current_square.y_pos > 0:
            next_position = self.position - 15
            if GameController.SQUARE_ARRAY[next_position].content != 5:
                self.position = next_position

    def move_left(self):
        '''Same as above'''
        if self.current_square.x_pos > 0:
            next_position = self.position - 1
            if GameController.SQUARE_ARRAY[next_position].content != 5:
                self.position = next_position

    def move_down(self):
        '''Same as above'''
        if self.current_square.y_pos < 14:
            next_position = self.position + 15
            if GameController.SQUARE_ARRAY[next_position].content != 5:
                self.position = next_position

class Square:
    '''Square object is used to store coordinates and id
    Attributes are called to locate items and agents on the grid'''
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.content = 0


class GameController:
    '''Handles the labyrinth grid creation using dedicated json file
    Created grid is stored as an array of squares used for navigation
    Also contains useful variable to check game state'''

    RUNNING = True
    GAME_OVER = False
    START_SQUARE_ID = 0
    SQUARE_ARRAY = []

    @classmethod
    def initialize_squares(cls):
        '''Generates fresh empty grid and add items on it using the method below'''
        cls.SQUARE_ARRAY = []

        for i in range(0, 15):
            for j in range(0, 15):

                square = Square(j, i)
                cls.SQUARE_ARRAY.append(square)

        cls.populate_squares()


    @classmethod
    def populate_squares(cls):
        '''Creates items on squares. Nature of item is defined by an int
        that is stored in the content attribute of the square :
        1 is warden, 2 to 4 are pick-ups, 5 is wall, 6 is character'''
        for counter, id_key in enumerate(
                json.load(open("ressources/wall-layout.json"))):

            if counter == 0:
                cls.SQUARE_ARRAY[id_key].content = 6
                START_SQUARE_ID = id_key
            elif counter == 1:
                cls.SQUARE_ARRAY[id_key].content = 1
            else:
                cls.SQUARE_ARRAY[id_key].content = 5

        for i in range(2, 5):
            random_id = random.randrange(0, 225)

            while cls.SQUARE_ARRAY[random_id].content != 0:
                random_id = random.randrange(0, 225)
                #select new random square if current one already has content

            cls.SQUARE_ARRAY[random_id].content = i


class Display:
    '''handles sprites loading from ressources folder
    also displays them in the window, based on their position on the grid'''

    SPRITE_WIDTH = 50

    TILE_SPRITE = pygame.image.load("ressources/tile.png")
    CHARACTER_SPRITE = pygame.image.load("ressources/character.png")
    WARDEN_SPRITE = pygame.image.load("ressources/warden.png").convert_alpha()
    NEEDLE_SPRITE = pygame.image.load("ressources/needle.png").convert_alpha()
    PIPE_SPRITE = pygame.image.load("ressources/pipe.png").convert_alpha()
    ETHER_SPRITE = pygame.image.load("ressources/ether.png").convert_alpha()
    WALL_SPRITE = pygame.image.load("ressources/wall.png")
    VICTORY_SCREEN = pygame.image.load("ressources/victory.jpg")
    DEFEAT_SCREEN = pygame.image.load("ressources/defeat.jpg")

    STATE = None

    @classmethod
    def refresh_display(cls):
        '''The method is called after each action (i.e when the character moves)
        Each square is refreshed, displaying eventual content atop standard tile'''

        if cls.STATE == "Victory":
            WINDOW.blit(Display.VICTORY_SCREEN, (0, 0))

        elif cls.STATE == "Defeat":
            WINDOW.blit(Display.DEFEAT_SCREEN, (0, 0))

        else:    

            for square in GameController.SQUARE_ARRAY:

                x_pix_pos = square.x_pos * cls.SPRITE_WIDTH
                y_pix_pos = square.y_pos * cls.SPRITE_WIDTH

                WINDOW.blit(cls.TILE_SPRITE, (x_pix_pos, y_pix_pos))

                #standard tile is blitted before adding eventual content

                if square.content == 1:
                    WINDOW.blit(cls.WARDEN_SPRITE, (x_pix_pos, y_pix_pos))

                elif square.content == 2:
                    WINDOW.blit(cls.NEEDLE_SPRITE, (x_pix_pos, y_pix_pos))

                elif square.content == 3:
                    WINDOW.blit(cls.PIPE_SPRITE, (x_pix_pos, y_pix_pos))

                elif square.content == 4:
                    WINDOW.blit(cls.ETHER_SPRITE, (x_pix_pos, y_pix_pos))

                elif square.content == 5:
                    WINDOW.blit(cls.WALL_SPRITE, (x_pix_pos, y_pix_pos))

                elif square.content == 6:
                    WINDOW.blit(cls.CHARACTER_SPRITE, (x_pix_pos, y_pix_pos))

        
        pygame.display.flip()


def main():
    '''Initializes the grid, player's agent, and handles gameplay loop'''

    GameController.initialize_squares()
    character = Macgyver(GameController.START_SQUARE_ID)
    Display.refresh_display()

    while GameController.RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                GameController.RUNNING = False

            if (event.type == KEYDOWN and
                    event.key in (K_LEFT, K_UP, K_RIGHT, K_DOWN)):

                character.current_square.content = 0

                if event.key == K_LEFT:
                    character.move_left()

                elif event.key == K_UP:
                    character.move_up()

                elif event.key == K_RIGHT:
                    character.move_right()

                elif event.key == K_DOWN:
                    character.move_down()

                character.touch_square()
                character.current_square.content = 6
                Display.refresh_display()

    while GameController.GAME_OVER:
        for event in pygame.event.get():
            if event.type == QUIT:
                GameController.GAME_OVER = False

if __name__ == "__main__":
    main()
