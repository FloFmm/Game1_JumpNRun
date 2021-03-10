import pygame
from otherFunctions import *


class Player:

    def __init__(self, playerXC, playerYC, playerMS, jumpSpeed):
        self.height = 60
        self.width = 30
        self.XC = playerXC
        self.YC = playerYC
        self.MS = playerMS
        self.jumpSpeed = jumpSpeed
        self.curSpeedX = 0
        self.curSpeedY = 0
        self.maxJumps = 2
        self.jumpMark = self.maxJumps
        self.playerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.restXS = 0
        self.restYS = 0

    def updateScale(self, world):

        # update XC if windowWidth has changed (hold relative position on the screen)
        if world.windowWidth != world.windowWidthOld:
            self.XC = int(self.XC * world.windowWidth / world.windowWidthOld)

        # update YC if windowHeight has changed (hold relative position on the Screen)
        if world.windowHeight != world.windowHeightOld:
            self.YC = int(self.YC * world.windowHeight / world.windowHeightOld)

        self.height = int(world.windowHeight / world.playerSize)
        self.width = int(world.windowWidth / (world.playerSize * 4))
        self.jumpSpeed = int(world.windowHeight / 45)
        self.MS = world.windowWidth / 240

    def display(self, world):
        self.playerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, (255, 0, 0), self.playerRect)

    def move(self, world, ground):

        # shifting player with world
        self.XC -= int(world.gameMS)

        xStep = 0
        yStep = 0

        # setting x and y step according to direction of movement
        if self.curSpeedX > 0:
            xStep = 1
        elif self.curSpeedX < 0:
            xStep = -1

        if self.curSpeedY > 0:
            yStep = 1
        elif self.curSpeedY < 0:
            yStep = -1



        # managing float integer value of current MS in one pixel steps
        self.restXS = rest(self.restXS)
        self.restXS += rest(self.curSpeedX)
        self.curSpeedX += float(int(self.restXS))

        self.restYS = rest(self.restYS)
        self.restYS += rest(self.curSpeedY)
        self.curSpeedY += float(int(self.restYS))

        leave = False
        for i in range(int(toUnsigned(self.curSpeedX))):
            self.XC += xStep
            collidedBlocks = ground.groundCollision(world, self)
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(self, collidedBlocks[j] - 1) < ground.overlappedY(self, collidedBlocks[j] - 1):
                    self.XC -= xStep * ground.overlappedX(self, collidedBlocks[j] - 1)
                    self.curSpeedX = 0
                    leave = True
            if leave:
                break


        leave = False
        for i in range(int(toUnsigned(self.curSpeedY))):
            self.YC += yStep
            collidedBlocks = ground.groundCollision(world, self)
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(self, collidedBlocks[j] - 1) > ground.overlappedY(self, collidedBlocks[j] - 1):
                    self.YC -= yStep * ground.overlappedY(self, collidedBlocks[j] - 1)
                    self.curSpeedY = 0
                    self.jumpMark = self.maxJumps
                    leave = True
            if leave:
                break

    # execution of player jump
    def jump(self):

        if self.jumpMark > 0:  # jump if jumpmarks available
            self.jumpMark -= 1  # decrement jumpmarks
            self.curSpeedY = -self.jumpSpeed  # set Y-Speed to jumpSpeed

    # checks if player out of screen X DIRECTION
    def outOfScreenX(self, world):
        if self.XC < 0 or self.XC + self.width >= world.windowWidth:
            return True
        return False

    # checks if player out of screen y DIRECTION
    def outOfScreenY(self, world):
        if self.YC < 0 or self.YC + self.height >= world.windowHeight:
            return True
        return False

    # executes gravity on the player
    def gravity(self, world):
        self.curSpeedY += world.gravity
