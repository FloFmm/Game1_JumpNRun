# checks wether or not player and groundBlock are colliding
def Collision(i, world, ground, player1):

    return player1.YC + player1.height > world.windowHeight - ground.groundArray[i].height\
        and player1.YC < world.windowHeight\
        and player1.XC + player1.width > ground.groundArray[i].XC\
        and player1.XC < ground.groundArray[i].XC + ground.groundArray[i].width


# determines if two rects are overlapped
def overlappedRect(x1, y1, width1, height1, x2, y2, width2, height2):
    return x1 + width1 > x2 and x1 < x2 + width2 and y1 + height1 > y2 and y1 < y2 + height2


# returns the unsigned of an int
def toUnsigned(x):
    if x < 0:
        return -x
    return x


def rest(x):
    if x > 0:
        return x % 1
    elif x < 0:
        return -((-x) % 1)
    return 0


def posOrNeg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
