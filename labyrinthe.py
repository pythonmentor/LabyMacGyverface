
#! /usr/bin/env python3
# coding: utf-8

import random

def main():
    print("Hello")

    character = Macgyver(Labyrinth.START_SQUARE_ID)
    Labyrinth.initializeSquares()

    while Labyrinth.RUNNING:
        user_input = input('Move with zqsd')
        print(user_input)
        if user_input in ('z', 'q', 's', 'd'):
            character.move(user_input)

    print("Game Over")

class Macgyver:
    def __init__(self, startPos):
        self.position = startPos
        self.items=[]

    @property
    def currentSquare(self):
        return Labyrinth.SQUARE_ARRAY[self.position]


    ### SQUARE INTERACTION ###

    def touchSquare(self):
        newSquare = self.currentSquare #call property only once and store into local var
        if newSquare.content == 1:
            if len(self.items) == 3:
                print("Victory !")
                Labyrinth.RUNNING = False
            else:
                print("Defeat !")
                Labyrinth.RUNNING = False
        elif newSquare.content in (2, 3, 4):
            self.addItem(newSquare.content)

    def addItem(self, contentId):
        switcher = {
        2: "needle",
        3: "pipe",
        4: "ether"
        }
        self.items.append(switcher.get(contentId, "invalid contentId"))
        print("Inventory contains : " + ", ".join(self.items))


    ### MOVEMENT ###

    def move(self, key):
        switcher = {
            'q': "move_Left",
            's': "move_Down",
            'd': "move_Right",
            'z': "move_Up"
        }
        func = switcher.get(key, "invalid input")
        method = getattr(self, func, lambda: "Invalid move")
        method()
        self.touchSquare()
    
    def move_Right(self):    
        if self.currentSquare.xPos < 14:
            self.position +=1
            print("Successfully arrived at position id " + str(self.position) + " with coordinates " + str(self.currentSquare.xPos) + " , " + str(self.currentSquare.yPos))
        else:
            print("Grid border reached")

    def move_Up(self):
        if self.currentSquare.yPos > 0:
            self.position -=15
            print("Successfully arrived at position id " + str(self.position) + " with coordinates " + str(self.currentSquare.xPos) + " , " + str(self.currentSquare.yPos))
        else:
            print("Grid border reached")

    def move_Left(self):
        if self.currentSquare.xPos > 0:
            self.position -=1
            print("Successfully arrived at position id " + str(self.position) + " with coordinates " + str(self.currentSquare.xPos) + " , " + str(self.currentSquare.yPos))
        else:
            print("Grid border reached")

    def move_Down(self):
        if self.currentSquare.yPos < 14:
            self.position +=15
            print("Successfully arrived at position id " + str(self.position) + " with coordinates " + str(self.currentSquare.xPos) + " , " + str(self.currentSquare.yPos))
        else:
            print("Grid border reached")


class Square:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.content = 0

    def getContent(self):
        return self.content

    

class Labyrinth:


    START_SQUARE_ID = 224
    END_SQUARE_ID = 0
    SQUARE_ARRAY = []
    RUNNING = False

    #Generates fresh empty grid, then add items on it using the method below, then finally enables gameplay loop
    @classmethod
    def initializeSquares(cls):
        cls.SQUARE_ARRAY = []
        for i in range (0, 15):
            for j in range (0, 15):
                square = Square(j, i)
                cls.SQUARE_ARRAY.append(square)
        cls.populateSquares()
        cls.RUNNING = True


    #Creates items on squares. Nature of item is defined by an int stored in the content attribute of the square :  1 is warden, 2 to 4 are pick-ups
    @classmethod
    def populateSquares(cls):
        cls.SQUARE_ARRAY[cls.END_SQUARE_ID].content = 1
        for i in range (2, 5):
            random_id = random.randrange((cls.END_SQUARE_ID+1), cls.START_SQUARE_ID)

            while cls.SQUARE_ARRAY[random_id].content != 0:
                random_id = random.randrange((cls.END_SQUARE_ID+1), cls.START_SQUARE_ID) #select new random square if current one already has content

            cls.SQUARE_ARRAY[random_id].content = i



if __name__ == "__main__":
    main()
