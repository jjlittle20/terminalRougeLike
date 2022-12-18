import math
import random


class DungeonWrapper:
    def __init__(self):
        self.maxWidth = 80
        self.maxHeight = 30
        self.minWidth = 0
        self.minHeight = 0
        self.initialMapState = [
            [" " for x in range(self.maxWidth)] for x in range(self.maxHeight)
        ]
        self.currentMapState = self.initialMapState
        self.maxRooms = self.getMaxRooms()
        self.currentRooms = self.generateRooms()

    def getMaxRooms(self):
        if self.maxWidth == self.maxHeight:
            return round(math.sqrt(self.maxWidth))
        elif self.maxWidth > self.maxHeight:
            return round(math.sqrt(self.maxWidth))
        else:
            return round(math.sqrt(self.maxHeight))

    def generateRooms(self):
        rooms = []

        for index in range(self.maxRooms):
            row = random.randint(0, self.maxHeight)
            col = random.randint(0, self.maxWidth)
            room = self.plotRoom([row, col], index)

            if hasattr(room, "tiles"):
                for tile in room.tiles:
                    row = tile.row
                    col = tile.col
                    self.currentMapState[row][col] = tile
                rooms.append(room)
        return rooms

    def checkOverlappedRoom(self, room):

        for tile in room.tiles:
            row = tile.row
            col = tile.col

            if isinstance(self.currentMapState[row][col], Tile):
                return True
        return False

    def plotRoom(self, origin, index):

        row = origin[0]
        col = origin[1]
        room = Room(origin)
        for i in range(room.width):
            for j in range(room.height):

                if row + i >= self.maxHeight or col + j >= self.maxWidth:
                    pass

                else:

                    room.tiles.append(Tile(row + i, col + j, str(index)))
        if self.checkOverlappedRoom(room):
            self.plotRoom(
                [
                    random.randint(0, self.maxHeight),
                    random.randint(0, self.maxWidth),
                ],
                index,
            )
        else:

            return room


class Tile:
    def __init__(self, row, col, symbol):
        self.symbol = symbol
        self.row = row
        self.col = col


class Room:
    def __init__(self, origin):
        self.origin = origin
        self.width = random.randint(2, 15)
        self.height = random.randint(2, 15)
        self.tiles = []


class SquareRoom(Room):
    def __init__(self, origin):
        super().__init__(origin)


def drawMap():
    for yIndex, y in enumerate(currentMap.currentMapState):

        row = ""
        for xIndex, x in enumerate(y):

            # t = "[" + str(yIndex) + "," + str(xIndex) + "]"
            # row = row + str(t)
            if type(x) == str:
                row = row + x
            else:
                row = row + x.symbol
        print(row)


def main():
    global currentMap
    currentMap = DungeonWrapper()
    drawMap()
    pass


main()
