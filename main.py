from GroundBlock import *

import pygame
from random import randint


pygame.init()

# world.window = pygame.display.set_mode((world.windowWidth, world.windowHeight), pygame.RESIZABLE)
pygame.display.set_caption("Jump n Run")
clock = pygame.time.Clock()

class World:
    
    def __init__(self):
        self.blockAmount = 14
        self.windowWidth = 1200
        self.windowHeight = 600
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.gravity = int((self.windowHeight/600*2+1)/2)  # 1
        self.gameMS = int((self.windowWidth/600*2+1)/2)
        self.scale = 10
        self.spaceHold = False
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE)
    
    def updateWorld(self):
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.windowWidth, self.windowHeight = pygame.display.get_surface().get_size()
        self.gameMS = int((self.windowWidth/600*2+1)/2)


class Player:

    def __init__(self, playerHeight, playerWidth, playerXC, playerYC, playerMS, jumpSpeed):
        self.height = playerHeight
        self.width = playerWidth
        self.XC = playerXC
        self.YC = playerYC
        self.MS = playerMS
        self.jumpSpeed = jumpSpeed
        self.curSpeedX = 0
        self.curSpeedY = 0
        self.maxJumps = 2
        self.jumpMark = self.maxJumps
        self.display()

    def updateScale(self):

        # update XC if
        if world.windowWidth != world.windowWidthOld:
            self.XC = int(self.XC * world.windowWidth/world.windowWidthOld)

        if world.windowHeight != world.windowHeightOld:
            self.YC = int(self.YC * world.windowHeight/world.windowHeightOld)

        self.height = int(world.windowHeight/world.scale)
        self.width = int(world.windowWidth/(world.scale*4))
        self.jumpSpeed = int(world.windowHeight/45)
        self.MS = int(world.windowWidth/240)

    def display(self):
        self.playerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, (255, 0, 0), self.playerRect)

    def move(self):

        # shifting player with world
        player1.XC -= world.gameMS

        xStep = 0
        yStep = 0

        if self.curSpeedX > 0:
            xStep = 1
        elif self.curSpeedX < 0:
            xStep = -1

        if self.curSpeedY > 0:
            yStep = 1
        elif self.curSpeedY < 0:
            yStep = -1

        leave = False
        for i in range(toUnsigned(self.curSpeedX)):
            self.XC += xStep
            collidedBlocks = ground.groundCollision()
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(collidedBlocks[j] - 1) < ground.overlappedY(collidedBlocks[j] - 1):
                    self.XC -= xStep * ground.overlappedX(collidedBlocks[j] - 1)
                    player1.curSpeedX = 0
                    leave = True
            if leave:
                break

        leave = False
        for i in range(toUnsigned(self.curSpeedY)):
            self.YC += yStep
            collidedBlocks = ground.groundCollision()
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(collidedBlocks[j] - 1) > ground.overlappedY(collidedBlocks[j] - 1):
                    self.YC -= yStep * ground.overlappedY(collidedBlocks[j] - 1)
                    player1.curSpeedY = 0
                    self.jumpMark = self.maxJumps
                    leave = True
            if leave:
                break

    # execution of player jump
    def jump(self):

        if self.jumpMark > 0:  # jump if jumpmarks available
            self.jumpMark -= 1  # decrement jumpmarks
            player1.curSpeedY = -player1.jumpSpeed  # set Y-Speed to jumpSpeed
    
    # checks if player out of screen X DIRECTION
    def outOfScreenX(self):
        if self.XC < 0 or self.XC + self.width >= world.windowWidth:
            return True
        return False

    # checks if player out of screen y DIRECTION
    def outOfScreenY(self):
        if self.YC < 0 or self.YC + self.height >= world.windowHeight:
            return True
        return False

    # executes gravity on the player
    def gravity(self):
        self.curSpeedY += world.gravity




class Ground:

    def __init__(self, blockAmount, groundMin, groundMax):
        self.groundMin = groundMin
        self.groundMax = groundMax
        self.width = int(world.windowWidth / blockAmount)
        self.groundArray = []
        self.height = 20
        self.blockAmount = blockAmount
        self.initGroundArray()
        self.distanceMoved = 0

    # fills the ground array with blocks
    def initGroundArray(self):
        for i in range(self.blockAmount+1):
            self.groundArray.append(GroundBlock(world, self.width*i, self.width, randint(self.groundMin, self.groundMax)))

    # shifts ground considering the current world.window size
    def updateGround(self):

        self.distanceMoved = (self.distanceMoved + world.gameMS) % (world.windowWidth + self.groundArray[0].width)
        if world.windowWidth != world.windowWidthOld:
            self.distanceMoved = int(self.distanceMoved * world.windowWidth/world.windowWidthOld)

        for j in range(self.blockAmount + 1):

            # horizontal update
            self.groundArray[j].width = int(world.windowWidth / self.blockAmount)
            self.groundArray[j].XC = world.windowWidth - ((world.windowWidth - j * self.groundArray[j].width + self.distanceMoved)
                                                    % (world.windowWidth + self.groundArray[j].width))

            # update height of block if it went out of bound and got relocated
            if self.groundArray[j].XC >= world.windowWidth:  # +1 removed ###############################################
                self.groundArray[j].rawHeight = randint(ground.groundMin, ground.groundMax)

            # vertical update
            self.groundArray[j].height = int(self.groundArray[j].rawHeight * world.windowHeight / 1000)
            self.groundArray[j].YC = world.windowHeight - self.groundArray[j].height  # +1 removed! #####################

            # update blockRect
            self.groundArray[j].blockRect = pygame.Rect((self.groundArray[j].XC,
                                                         self.groundArray[j].YC,
                                                         self.groundArray[j].width,
                                                         self.groundArray[j].height))

        # add missing pixels to last block (due to int cast after division)
        self.groundArray[self.blockAmount].width += world.windowWidth - self.blockAmount * self.groundArray[self.blockAmount].width

    # returns array of all blocks the player has been collided with
    def groundCollision(self):
        arr = []
        for i in range(self.blockAmount + 1):
            if Collision(i):
                arr.append(i + 1)
        return arr

    # returns the overlapping from player and block in X direction
    def overlappedX(self, block):
        rightFromPlayer = player1.XC + player1.width - self.groundArray[block].XC
        leftFromPlayer = self.groundArray[block].XC + self.groundArray[block].width - player1.XC
        if rightFromPlayer < leftFromPlayer:
            return rightFromPlayer
        else:
            return leftFromPlayer

    # returns the overlapping from player and block in Y direction
    def overlappedY(self, block):
        belowPlayer = player1.YC + player1.height - self.groundArray[block].YC
        abovePlayer = self.groundArray[block].YC + self.groundArray[block].height - player1.YC
        if belowPlayer < abovePlayer:
            return belowPlayer
        else:
            return abovePlayer


# checks wether or not player and groundBlock are colliding
def Collision(i):

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

world = World()

ground = Ground(world.blockAmount, 50, 350)

player1 = Player(80, 40, 200, 200, 5, 15)

while True:

    # exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # saving pressed keys
    keysPressed = pygame.key.get_pressed()

    # key action
    if keysPressed[pygame.K_RIGHT]:
        player1.curSpeedX = player1.MS
    elif keysPressed[pygame.K_LEFT]:
        player1.curSpeedX = -player1.MS
    else:
        player1.curSpeedX = 0
    if keysPressed[pygame.K_SPACE]:
        if not world.spaceHold:   # allowing jump only when key has previously been released
            player1.jump()  # -> only one jump mark is used when pressing the key once (and holding it)
            world.spaceHold = True
    else:
        world.spaceHold = False

    # updates all properties of the whole world
    world.updateWorld()

    # update all sizes
    player1.updateScale()
    ground.updateGround()

    # update all positions
    player1.gravity()
    player1.move()

    # display content
    for i in range(world.blockAmount+1):
        ground.groundArray[i].drawBlock(world)
    player1.display()

    # pygame stuff
    pygame.display.flip()
    world.window.fill((0, 0, 0))
    clock.tick(60)
