from PIL import ImageGrab, ImageOps
import pyautogui
import time

# print(pyautogui.displayMousePosition())

currentGrid = [
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
]

UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103

scoreGrid = [
    50, 30, 15, 5,
    30, -10, 0, 0,
    15, 0, 0, 0,
    5, 0, 0, 0,
]


class Cords:
    cord11 = (250, 280)
    cord12 = (370, 280)
    cord13 = (490, 280)
    cord14 = (610, 280)
    cord21 = (250, 400)
    cord22 = (370, 400)
    cord23 = (490, 400)
    cord24 = (610, 400)
    cord31 = (250, 520)
    cord32 = (370, 520)
    cord33 = (490, 520)
    cord34 = (610, 520)
    cord41 = (250, 640)
    cord42 = (370, 640)
    cord43 = (490, 640)
    cord44 = (610, 640)

    cordArray = [
        cord11, cord12, cord13, cord14,
        cord21, cord22, cord23, cord24,
        cord31, cord32, cord33, cord34,
        cord41, cord42, cord43, cord44,
    ]


class Values:
    empty = 193
    empty1 = 194
    empty2 = 195
    two = 229
    four = 225
    eight = 190
    sixteen = 172
    thirtyTwo = 157
    sixtyFour = 135
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    valueArray = [empty, empty1, empty2, two, four, eight, sixteen, thirtyTwo, sixtyFour,
                  oneTwentyEight, twoFiftySix, fiveOneTwo, oneZeroTwoFour, twoZeroFourEight]


def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)
    for index, cord in enumerate(Cords.cordArray):
        pixel = grayImage.getpixel(cord)
        pos = Values.valueArray.index(pixel)
        if pos == 0 or pos == 1 or pos == 2:
            currentGrid[index] = 0
        else:
            currentGrid[index] = pow(2, pos-2)


def printGrid(grid):
    for i in range(16):
        if i % 4 == 0:
            print("[ "+str(grid[i])+" "+str(grid[i+1]) +
                  " "+str(grid[i+2])+" "+str(grid[i+3])+" ]")


def swipeRow(row):
    prev = -1
    i = 0
    temp = [0, 0, 0, 0]
    for element in row:
        if element != 0:
            if prev == -1:
                prev = element
                temp[i] = element
                i += 1
            elif prev == element:
                temp[i-1] = 2*prev
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1
    return temp


def getNextGrid(grid, move):
    temp = [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
    ]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i+4*j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i+4*j] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4*i+j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4*i+j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i+4*(3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i+4*(3-j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4*i+(3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4*i+(3-j)] = val

    return temp


def getScore(grid):
    score = 0
    for i in range(4):
        for j in range(4):
            score += grid[4*i+j]*scoreGrid[4*i+j]
    return score


def isMoveValid(grid, move):
    if getNextGrid(grid, move) == grid:
        return False
    else:
        return True


def getBestMove(grid):
    scoreUp = getScore(getNextGrid(grid, UP))
    scoreDown = getScore(getNextGrid(grid, DOWN))
    scoreLeft = getScore(getNextGrid(grid, LEFT))
    scoreRight = getScore(getNextGrid(grid, RIGHT))

    if not isMoveValid(grid, UP):
        scoreUp = 0
    if not isMoveValid(grid, DOWN):
        scoreDown = 0
    if not isMoveValid(grid, LEFT):
        scoreLeft = 0
    if not isMoveValid(grid, RIGHT):
        scoreRight = 0

    maxScore = max(scoreUp, scoreDown, scoreLeft, scoreRight)

    if maxScore == scoreUp:
        return UP
    elif maxScore == scoreDown:
        return DOWN
    elif maxScore == scoreLeft:
        return LEFT
    else:
        return RIGHT

    if getNextGrid(grid, move) == grid:
        return False
    else:
        return True


def performMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        print("UP")
        time.sleep(0.05)
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        print("DOWN")
        time.sleep(0.05)
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        print("LEFT")
        time.sleep(0.05)
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        print("RIGHT")
        time.sleep(0.05)
        pyautogui.keyUp('right')


def main():
    print('Beginning in 5 seconds....')
    time.sleep(5)
    while True:
        getGrid()
        performMove(getBestMove(currentGrid))
        time.sleep(0.1)


if __name__ == "__main__":
    main()



# performMove(UP)

# getGrid()
# printGrid(currentGrid)
# print(getScore(currentGrid))
# printGrid(getNextGrid(currentGrid, UP))

# image = ImageGrab.grab()
# grayImage = ImageOps.grayscale(image)
# for cord in Cords.cordArray:
#     pixel = grayImage.getpixel(cord)
#     print(pixel)
