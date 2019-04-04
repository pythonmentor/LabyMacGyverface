
#! /usr/bin/env python3
# coding: utf-8

import json
import random
import pygame
from pygame.locals import *

pygame.init() #enables sprite initialization during Display class declaration
WINDOW = pygame.display.set_mode((750, 750))


class Macgyver:
    def __init__(self, startPos):
        self.position = startPos
        self.items = []
        self.currentSquare.content = 6

    @property
    def currentSquare(self):
        return GameController.SQUARE_ARRAY[self.position]


    ### SQUARE INTERACTION ###

    def touch_square(self):
        newSquare = self.currentSquare #call property only once and store into local var
        if newSquare.content == 1:
            if len(self.items) == 3:
                print("Victory !")
                GameController.RUNNING = False
            else:
                print("Defeat !")
                GameController.RUNNING = False
        elif newSquare.content in (2, 3, 4):
            self.add_item(newSquare.content)

    def add_item(self, contentId):
        switcher = {
        2: "needle",
        3: "pipe",
        4: "ether"
        }
        self.items.append(switcher.get(contentId, "invalid contentId"))
        print("Inventory contains : " + ", ".join(self.items))


    ### MOVEMENT ###
    
    def move_Right(self):    
        if self.currentSquare.xPos < 14:
            nextPosition = self.position +1
            if GameController.SQUARE_ARRAY[nextPosition].content != 5:
                self.position = nextPosition


    def move_Up(self):
        if self.currentSquare.yPos > 0:
            nextPosition = self.position - 15
            if GameController.SQUARE_ARRAY[nextPosition].content != 5:
                self.position = nextPosition

    def move_Left(self):
        if self.currentSquare.xPos > 0:
            nextPosition = self.position - 1
            if GameController.SQUARE_ARRAY[nextPosition].content != 5:
                self.position = nextPosition

    def move_Down(self):
        if self.currentSquare.yPos < 14:
            nextPosition = self.position + 15
            if GameController.SQUARE_ARRAY[nextPosition].content != 5:
                self.position = nextPosition


class Square:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.content = 0

    def getContent(self):
        return self.content


class GameController:

    RUNNING = True
    START_SQUARE_ID = 224
    END_SQUARE_ID = 0
    SQUARE_ARRAY = []

    #Generates fresh empty grid, then add items on it using the method below
    @classmethod
    def initializeSquares(cls):
        cls.SQUARE_ARRAY = []
        for i in range (0, 15):
            for j in range (0, 15):
                square = Square(j, i)
                cls.SQUARE_ARRAY.append(square)
        cls.populateSquares()


    #Creates items on squares. Nature of item is defined by an int 
    #int is stored in the content attribute of the square :  
    #1 is warden, 2 to 4 are pick-ups, 5 is wall
    @classmethod
    def populateSquares(cls):
        cls.SQUARE_ARRAY[cls.END_SQUARE_ID].content = 1
        for wall in json.load(open("ressources/wall-layout.json")):
            cls.SQUARE_ARRAY[wall].content = 5
        for i in range (2, 5):
            random_id = random.randrange((cls.END_SQUARE_ID+1), cls.START_SQUARE_ID)

            while cls.SQUARE_ARRAY[random_id].content != 0:
                random_id = random.randrange((cls.END_SQUARE_ID+1), cls.START_SQUARE_ID) 
                #select new random square if current one already has content

            cls.SQUARE_ARRAY[random_id].content = i


class Display:
    SPRITE_WIDTH = 50

    CHARACTER_SPRITE = pygame.image.load("ressources/character.png").convert_alpha()
    CHARACTER_SPRITE.set_colorkey((255,255,255))
    WARDEN_SPRITE = pygame.image.load("ressources/warden.png").convert_alpha()
    WARDEN_SPRITE.set_colorkey((255,255,255))
    NEEDLE_SPRITE = pygame.image.load("ressources/needle.png").convert_alpha()
    NEEDLE_SPRITE.set_colorkey((255,255,255))
    PIPE_SPRITE = pygame.image.load("ressources/pipe.png")
    PIPE_SPRITE.set_colorkey((255,255,255))
    ETHER_SPRITE = pygame.image.load("ressources/ether.png").convert_alpha()
    ETHER_SPRITE.set_colorkey((0,0,0)) 
    WALL_SPRITE = pygame.image.load("ressources/wall.png").convert_alpha()

    @classmethod
    def refresh_display(cls):
        for square in GameController.SQUARE_ARRAY:
            if square.content == 1:
                WINDOW.blit(cls.WARDEN_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))
            elif square.content == 2:
                WINDOW.blit(cls.NEEDLE_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))
            elif square.content == 3:
                WINDOW.blit(cls.PIPE_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))
            elif square.content == 4:
                WINDOW.blit(cls.ETHER_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))
            elif square.content == 5:
                WINDOW.blit(cls.WALL_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))
            elif square.content == 6:
                WINDOW.blit(cls.CHARACTER_SPRITE, (square.xPos * cls.SPRITE_WIDTH, square.yPos * cls.SPRITE_WIDTH))

        pygame.display.flip()

def main():
    
    GameController.initializeSquares()
    character = Macgyver(GameController.START_SQUARE_ID)
    Display.refresh_display()
    
    while GameController.RUNNING:
        for event in pygame.event.get(): 
            if event.type == QUIT:   
                GameController.RUNNING = False

            if event.type == KEYDOWN and event.key in (K_LEFT, K_UP, K_RIGHT, K_DOWN):

                character.currentSquare.content = 0

                if event.key == K_LEFT:
                    character.move_Left()

                elif event.key == K_UP:
                    character.move_Up()

                elif event.key == K_RIGHT:
                    character.move_Right()

                elif event.key == K_DOWN:
                    character.move_Down()

                character.touch_square()
                character.currentSquare.content = 6
                Display.refresh_display()

if __name__ == "__main__":
    main()
