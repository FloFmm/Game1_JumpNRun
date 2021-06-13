from GroundBlock import *
from otherFunctions import Collision, probability

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
        self.blockRepeat = 0

    # fills the ground array with blocks
    def initGroundArray(self, world):
        for i in range(self.blockAmount+world.blockBuffer):
             self.groundArray.append(StdBlock(world, self.width*i, self.width, randint(self.groundMin, self.groundMax)))

    # generates new groundBlock
    def genGroundBlock(self, world, i):
        # lava
        maxLavaHeight = 0.8  # 80% of the previous solid Block
        lavaProb = 60
        maxLavaB = 3



        # raises groundMin if the last Block is liquid (lava)
        if self.groundArray[i-1].blockType == "lava":
            groundMin = int(1/maxLavaHeight * self.groundArray[i-1].rawHeight)
        else:
            groundMin = self.groundMin


        # blockRepeat
        if self.groundArray[i-1].blockType == self.groundArray[i - 2].blockType:
            self.groundArray[i-1].blockRepeat = self.groundArray[i - 2].blockRepeat + 1
        else:
            self.groundArray[i-1].blockRepeat = 1


        # gen Lava Block
        if self.groundArray[i-1].blockType == "lava":
            if probability(lavaProb) and self.groundArray[i-1].blockRepeat < maxLavaB:
                self.groundArray[i] = LavaBlock(world, self.groundArray[i].XC, self.width,
                                                self.groundArray[i - 1].rawHeight)
                return
        elif probability(lavaProb):
            groundMax = int(maxLavaHeight * self.groundArray[i - 1].rawHeight)
            if groundMin > groundMax:
                self.groundArray[i] = LavaBlock(world, self.groundArray[i].XC, self.width, groundMax)
            else:
                self.groundArray[i] = LavaBlock(world, self.groundArray[i].XC, self.width,
                                                randint(groundMin,
                                                        int(maxLavaHeight * self.groundArray[i - 1].rawHeight)))
            return


        # gen Std Block
        self.groundArray[i] = StdBlock(world, self.groundArray[i].XC, self.width, randint(groundMin, self.groundMax))






    # shifts ground considering the current world.window size
    def updateGround(self, world):
        # managing float integer value of current MS in one pixel steps
        self.restGS = rest(self.restGS)
        self.restGS += rest(world.gameMS)
        world.gameMS += float(int(self.restGS))

        self.distanceMoved = (self.distanceMoved + int(world.gameMS)) % (world.windowWidth + world.blockBuffer * self.groundArray[0].width)
        if world.windowWidth != world.windowWidthOld:
            self.distanceMoved = int(self.distanceMoved * world.windowWidth/world.windowWidthOld)

        self.width = int(world.windowWidth / self.blockAmount)
        for j in range(self.blockAmount + world.blockBuffer):

            # horizontal update
            self.groundArray[j].width = self.width
            self.groundArray[j].XC = world.windowWidth - ((world.windowWidth - j * self.width + self.distanceMoved)
                                                    % (world.windowWidth + world.blockBuffer * self.width))

            # update height of block if it went out of bound and got relocated
            if self.groundArray[j].XC < -self.width:
                self.genGroundBlock(world, j)

            # vertical update
            self.groundArray[j].height = int(self.groundArray[j].rawHeight * world.windowHeight / 1000)
            self.groundArray[j].YC = world.windowHeight - self.groundArray[j].height  # +1 removed! #####################

            # update blockRect
            self.groundArray[j].blockRect = pygame.Rect((self.groundArray[j].XC,
                                                         self.groundArray[j].YC,
                                                         self.width,
                                                         self.groundArray[j].height))

        # add missing pixels to last block (due to int cast after division)
        self.groundArray[self.blockAmount+world.blockBuffer-1].width += world.windowWidth - self.blockAmount * self.groundArray[self.blockAmount].width


    # returns array of all blocks the player has been collided with
    def groundCollision(self, world, player1):
        arr = []
        for i in range(self.blockAmount + world.blockBuffer):
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
