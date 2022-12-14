import keyboard
import time
import os
import random
import curses


class Window:
    def __init__(self, name, rows, cols, rowsOffset, colsOffset, hasBorder):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.rowsOffset = rowsOffset
        self.colsOffset = colsOffset
        self.hasBorder = hasBorder

    def setupWindow(self):
        globals()[self.name] = curses.newwin(
            self.rows, self.cols, self.rowsOffset, self.colsOffset
        )
        window = globals()[self.name]
        if self.hasBorder:
            window.border()
        window.refresh()


class Map:
    def __init__(self, rows, cols):
        self.mapDefault = [["-" for x in range(cols)] for x in range(rows)]
        self.currentMapState = self.mapDefault
        self.xLength = len(self.mapDefault) - 1
        self.yLength = len(self.mapDefault[0]) - 1
        self.entities = []


class Player:
    def __init__(self, name):
        self.health = 2
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


class EnemyClass:
    def __init__(
        self,
        health,
        strength,
        defence,
        dexterity,
        symbol,
        facingDir,
        initialState,
        homePos,
        aggroRange,
        maxPursueRng,
    ):
        self.health = health
        self.maxHealth = health
        self.strength = strength
        self.defence = defence
        self.dexterity = dexterity
        self.symbol = symbol
        self.currentlyFacing = facingDir
        self.currentState = initialState
        self.homePosition = homePos
        self.currentPosition = self.homePosition
        self.previousPosition = self.currentPosition
        self.aggroRange = aggroRange
        self.maxPursueRange = maxPursueRng
        self.currentPursueRange = 0
        self.returnPosition = self.homePosition

    def checkState(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        playerX = player.currentPosition[0]
        playerY = player.currentPosition[1]
        if self.currentState == "return":
            return

        elif (
            (playerX == x + 1 and playerY == y)
            or (playerX == x - 1 and playerY == y)
            or (playerY == y + 1 and playerX == x)
            or (playerY == y - 1 and playerX == x)
            or (playerX == x and playerY == y)
        ):
            self.currentState = "attacking"
            arr = [-1, 1]
            randAmount = random.randint(0, 1)
            randDir = random.randint(0, 1)

            self.currentPosition[randDir] = (
                self.currentPosition[randDir] + arr[randAmount]
            )
        elif (
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
        elif self.currentState == "attacking":
            self.attack()

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

    def pursue(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]
        playX = player.currentPosition[0]
        playY = player.currentPosition[1]
        newPos = [x, y]
        # if x == playX and y == playY:
        #     self.currentState = "attacking"
        #     arr = [-1, 1]
        #     randAmount = random.randint(0, 1)
        #     randDir = random.randint(0, 1)

        #     self.currentPosition[randDir] = (
        #         self.currentPosition[randDir] + arr[randAmount]
        #     )

        if x == playX:
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


class EnemyWarrior(EnemyClass):
    def __init__(self):
        super().__init__(10, 10, 10, 10, "W", "down", "patrol", [8, 8], 5, 4)


class DebugWindow:
    def __init__(self):
        self.startPos = [20, 20]


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
    mapWindow.move(1, 1)
    for yIndex, y in enumerate(currentMap.currentMapState):
        for xIndex, x in enumerate(y):
            mapWindow.addch(str(x))
        mapWindow.move(1 + yIndex + 1, 1)

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
    if player.health <= 0:
        handleEndGame()
    xPos = player.currentPosition[1]
    yPos = player.currentPosition[0]
    prevXPos = player.previousPosition[1]
    prevYPos = player.previousPosition[0]
    currentMap.currentMapState[prevYPos][prevXPos] = "-"
    currentMap.currentMapState[yPos][xPos] = player.symbol


def handleEndGame():

    mainScreen.clear()
    mainScreen.addstr("Game Over!")
    mainScreen.refresh()
    mainScreen.getch()
    pass


def mainloop():
    updatePlayer()
    updateNPCs()
    handleDrawCurrentMap()
    keyboardListener()


def initTerminal():
    keyboard.press("f11")
    global mainScreen
    mainScreen = curses.initscr()
    curses.curs_set(0)
    mainScreen.refresh()
    debug = True
    windowList = []
    windowList.append(Window("mapWindow", 25, 65, 1, 1, True))
    if debug:
        windowList.append(Window("debugWindow", 25, 45, 1, 68, True))
    for window in windowList:
        window.setupWindow()


def initGame():
    initTerminal()
    global player
    player = Player("Test")
    global currentMap
    currentMap = Map(20, 60)
    currentMap.entities.append(EnemyWarrior())


initGame()
mainloop()
