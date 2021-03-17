from GroundBlock import *
from otherFunctions import Collision

import pygame
from random import randint
from otherFunctions import rest


class Ground:

    def __init__(self, world, groundMin, groundMax):
        self.groundMin = groundMin
        self.groundMax = groundMax
        self.width = int(world.windowWidth / world.blockAmount)
        self.groundArray = []
        self.height = 20
        self.blockAmount = world.blockAmount
        self.initGroundArray(world)
        self.distanceMoved = 0
        self.restGS = 0

    # fills the ground array with blocks
    def initGroundArray(self, world):
        for i in range(self.blockAmount+1):
            if i != 2:
                self.groundArray.append(StdBlock(world, self.width*i, self.width, randint(self.groundMin, self.groundMax)))
            else:
                self.groundArray.append(LavaBlock(world, 0, self.width, 666))#randint(self.groundMin, self.groundMax)))


    # shifts ground considering the current world.window size
    def updateGround(self, world):
        # managing float integer value of current MS in one pixel steps
        self.restGS = rest(self.restGS)
        self.restGS += rest(world.gameMS)
        world.gameMS += float(int(self.restGS))

        self.distanceMoved = (self.distanceMoved + int(world.gameMS)) % (world.windowWidth + self.groundArray[0].width)
        if world.windowWidth != world.windowWidthOld:
            self.distanceMoved = int(self.distanceMoved * world.windowWidth/world.windowWidthOld)

        for j in range(self.blockAmount + 1):

            # horizontal update
            self.groundArray[j].width = int(world.windowWidth / self.blockAmount)
            self.groundArray[j].XC = world.windowWidth - ((world.windowWidth - j * self.groundArray[j].width + self.distanceMoved)
                                                    % (world.windowWidth + self.groundArray[j].width))

            # update height of block if it went out of bound and got relocated
            if self.groundArray[j].XC >= world.windowWidth - 1:
                self.groundArray[j] = StdBlock(world, self.groundArray[j].XC,
                                                  self.groundArray[j].width, randint(self.groundMin, self.groundMax))

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
    def groundCollision(self, world, player1):
        arr = []
        for i in range(self.blockAmount + 1):
            if Collision(i, world, self, player1):
                arr.append(i)
        return arr

    # returns the overlapping from player and block in X direction
    def overlappedX(self, player1, block):
        rightFromPlayer = player1.XC + player1.width - self.groundArray[block].XC
        leftFromPlayer = self.groundArray[block].XC + self.groundArray[block].width - player1.XC
        if rightFromPlayer < leftFromPlayer:
            return rightFromPlayer
        else:
            return leftFromPlayer

    # returns the overlapping from player and block in Y direction
    def overlappedY(self, player1, block):
        belowPlayer = player1.YC + player1.height - self.groundArray[block].YC
        abovePlayer = self.groundArray[block].YC + self.groundArray[block].height - player1.YC
        if belowPlayer < abovePlayer:
            return belowPlayer
        else:
            return abovePlayer
