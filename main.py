import keyboard
import time
import os
import numpy
import random

import curses
from curses import wrapper


class Map:
    def __init__(self, xLen, yLen):
        self.mapDefault = [["-" for x in range(xLen)] for x in range(yLen)]
        self.currentMapState = self.mapDefault
        self.yLength = len(self.mapDefault) - 1
        self.xLength = len(self.mapDefault[0]) - 1
        self.entities = []


class Player:
    def __init__(self, name):
        self.health = 10
        self.maxHealth = 10
        self.symbol = "P"
        self.name = name
        self.currentPosition = [0, 0]
        self.previousPosition = [0, 0]
        self.currentlyFacing = "right"

    def movePosition(self, pos):
        self.previousPosition = self.currentPosition
        self.currentPosition = pos

    def checkState():
        pass

    def handleState():
        pass


class EnemyWarrior:
    def __init__(self):
        self.health = 10
        self.maxHealth = 10
        self.symbol = "W"
        self.currentlyFacing = "down"
        self.currentState = "patrol"
        self.homePosition = [8, 8]
        self.currentPosition = self.homePosition
        self.previousPosition = self.currentPosition
        self.aggroRange = 3
        self.maxPursueRange = 4
        self.currentPursueRange = 0
        self.returnPosition = self.homePosition

    def checkState(self):
        if self.currentState == "return":
            return
        if (
            abs(self.currentPosition[0] - player.currentPosition[0]) <= self.aggroRange
            and abs(self.currentPosition[1] - player.currentPosition[1])
            <= self.aggroRange
        ):
            self.currentState = "pursue"
        else:
            self.currentState = "patrol"

    def handleState(self):
        self.checkState()
        if self.currentState == "patrol":
            self.patrol()
        elif self.currentState == "pursue":
            self.pursue()
        elif self.currentState == "return":
            self.returnToPosition()

    def patrol(self):
        dirs = ["up", "down", "left", "right"]
        directions = {"up": [-1, 0], "down": [0, -1], "left": [1, 0], "right": [0, 1]}
        direction = directions[self.currentlyFacing]
        isBlocked = self.handleMove(direction)
        if isBlocked:
            newDirection = random.choice(dirs)
            self.currentlyFacing = newDirection
        else:
            if random.randint(0, 100) < 36:
                newDir = random.choice(dirs)
                self.currentlyFacing = newDir

    def updateMapPosition(self):
        x = self.currentPosition[1]
        y = self.currentPosition[0]
        prevX = self.previousPosition[1]
        prevY = self.previousPosition[0]
        currentMap.currentMapState[prevY][prevX] = "-"
        currentMap.currentMapState[y][x] = self.symbol

    def handleMove(self, direction):
        newX = self.currentPosition[0] + direction[0]
        newY = self.currentPosition[1] + direction[1]
        if (
            newY < 0
            or newY > currentMap.yLength
            or newX < 0
            or newX > currentMap.xLength
        ):
            return True
        else:
            self.movePosition([newX, newY])
            return False

    def attack(self):
        player.health = player.health - 1
        pass

    def pursue(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        playX = player.currentPosition[0]
        playY = player.currentPosition[1]
        newPos = [x, y]
        if x == playX and y == playY:
            self.attack()
            arr = [-1, 1]
            randAmount = random.randint(0, 1)
            randDir = random.randint(0, 1)

            self.currentPosition[randDir] = (
                self.currentPosition[randDir] + arr[randAmount]
            )
        elif x == playX:
            if y < playY:
                newPos[1] = newPos[1] + 1
            else:
                newPos[1] = newPos[1] - 1
        elif y == playY:
            if x < playX:
                newPos[0] = newPos[0] + 1
            else:
                newPos[0] = newPos[0] - 1
        else:
            rand = random.randint(0, 1)
            if self.currentPosition[rand] > player.currentPosition[rand]:
                newPos[rand] = newPos[rand] - 1
            else:
                newPos[rand] = newPos[rand] + 1
        self.currentPursueRange = self.currentPursueRange + 1
        if self.currentPursueRange >= self.maxPursueRange:
            self.currentPursueRange = 0
            self.currentState = "return"
        self.movePosition(newPos)

    def returnToPosition(self):
        homeX = self.returnPosition[0]
        homeY = self.returnPosition[1]
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        if x == homeX and y == homeY:
            self.currentState = "patrol"

        newPos = [x, y]
        if x == homeX:
            if y < homeY:
                newPos[1] = newPos[1] + 1
            else:
                newPos[1] = newPos[1] - 1
        elif y == homeY:
            if x < homeX:
                newPos[0] = newPos[0] + 1
            else:
                newPos[0] = newPos[0] - 1
        else:
            rand = random.randint(0, 1)
            if self.currentPosition[rand] > self.returnPosition[rand]:
                newPos[rand] = newPos[rand] - 1
            else:
                newPos[rand] = newPos[rand] + 1
        self.movePosition(newPos)

    def movePosition(self, pos):
        self.previousPosition = self.currentPosition
        self.currentPosition = pos


controls = {
    "w": ["playerMove", [-1, 0]],
    "a": ["playerMove", [0, -1]],
    "s": ["playerMove", [1, 0]],
    "d": ["playerMove", [0, 1]],
}


def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")


def handlePlayerMove(cord):
    newX = player.currentPosition[0] + cord[0]
    newY = player.currentPosition[1] + cord[1]
    if newY < 0 or newY > currentMap.yLength or newX < 0 or newX > currentMap.xLength:
        return
    else:
        player.movePosition([newX, newY])
        return


def handleDrawCurrentMap():
    mapWindow.move(0, 0)
    for xIndex, x in enumerate(currentMap.currentMapState):
        for yIndex, y in enumerate(x):
            mapWindow.addch(str(y))
        mapWindow.move(xIndex + 1, 0)

    mapWindow.addstr(str(player.health))

    mapWindow.refresh()


def keyboardListener():
    notValidKey = True
    time.sleep(0.1)
    while notValidKey:

        key = keyboard.read_key()
        control = controls.get(key)
        if control != None:
            notValidKey = False
            if control[0] == "playerMove":
                handlePlayerMove(control[1])
                mainloop()
                break


def updateNPCs():
    for entity in currentMap.entities:
        entity.checkState()
        entity.handleState()
        entity.updateMapPosition()


def updatePlayer():
    xPos = player.currentPosition[1]
    yPos = player.currentPosition[0]
    prevXPos = player.previousPosition[1]
    prevYPos = player.previousPosition[0]
    currentMap.currentMapState[prevYPos][prevXPos] = "-"
    currentMap.currentMapState[yPos][xPos] = player.symbol


def mainloop():
    updatePlayer()
    updateNPCs()
    handleDrawCurrentMap()
    keyboardListener()


def initGame():
    global mainScreen
    global mapWindow
    mainScreen = curses.initscr()
    mapWindow = curses.newwin(0, 0)
    global player
    player = Player("Test")
    global currentMap
    currentMap = Map(10, 10)
    currentMap.entities.append(EnemyWarrior())


initGame()
mainloop()
