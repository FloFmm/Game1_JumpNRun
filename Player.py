from otherFunctions import *
from GroundBlock import *

import pygame


class Player:

    def __init__(self, world, playerXC, playerYC, health):
        self.height = 60
        self.width = 30
        self.XC = playerXC
        self.YC = playerYC
        self.maxHP = health
        self.HP = self.maxHP
        self.healthBar = HealthBar(world)
        self.MS = world.windowWidth / 240
        self.jumpSpeed = world.windowHeight / 45 * 1.5
        self.curSpeedX = 0
        self.curSpeedY = 0
        self.maxJumps = 2
        self.jumpMark = self.maxJumps
        self.playerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.restXS = 0
        self.restYS = 0
        self.dmgLava = False
        self.color = (255, 255, 255)

        self.player_image = pygame.image.load('images/characters/ghost.png')
        self.player_image = pygame.transform.scale(self.player_image, (self.width,  self.height))

    def updateScale(self, world):

        # updating health bar
        self.healthBar.updateHealthBar(world, self)

        # update XC if windowWidth has changed (hold relative position on the screen)
        if world.windowWidth != world.windowWidthOld:
            self.XC = int(self.XC * world.windowWidth / world.windowWidthOld)

        # update YC if windowHeight has changed (hold relative position on the Screen)
        if world.windowHeight != world.windowHeightOld:
            self.YC = int(self.YC * world.windowHeight / world.windowHeightOld)

        self.height = int(world.windowHeight / world.playerSize)
        self.width = int(world.windowWidth / (world.playerSize * 4))
        self.jumpSpeed = world.windowHeight / 45 * 1.5
        self.MS = world.windowWidth / 240

    def display(self, world):
        self.playerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        #pygame.draw.rect(world.window, self.color, self.playerRect)

        self.player_image = pygame.transform.scale(self.player_image, (self.width, self.height))
        world.window.blit(self.player_image, (self.XC, self.YC))

        self.healthBar.drawBlock(world)

    def move(self, world, ground):


        # resets all moving stats
        self.cleanse(world)

        # shifting player with world
        self.XC -= int(world.gameMS)

        # setting x and y step according to direction of movement
        xStep = posOrNeg(self.curSpeedX)
        yStep = posOrNeg(self.curSpeedY)

        # managing float integer value of current MS in one pixel steps
        self.restXS = rest(self.restXS)
        self.restXS += rest(self.curSpeedX)
        self.curSpeedX += float(int(self.restXS))

        leave = False
        for i in range(int(toUnsigned(self.curSpeedX))):
            self.XC += xStep
            collidedBlocks = ground.groundCollision(world, self)
            for j in range(len(collidedBlocks)):
                leave = leave or ground.groundArray[collidedBlocks[j]].Collision(world, ground, 'x', collidedBlocks[j], self)
            if leave:
                break



        # managing float integer value of current MS in one pixel steps
        self.restYS = rest(self.restYS)
        self.restYS += rest(self.curSpeedY)

        # warum hier eine if funktion steht wissen wir selber nicht
        # eigentlich sollte der rest einer negativen Zahl auch negativ sein
        if self.curSpeedY>0:
            self.curSpeedY += float(int(self.restYS))
        else:
            self.curSpeedY -= float(int(self.restYS))

        leave = False
        for i in range(int(toUnsigned(self.curSpeedY))):
            self.YC += yStep
            collidedBlocks = ground.groundCollision(world, self)
            #print(collidedBlocks)
            for j in range(len(collidedBlocks)):
                leave = leave or ground.groundArray[collidedBlocks[j]].Collision(world, ground, 'y', collidedBlocks[j], self)
            if leave:
                break





    def cleanse(self, world):
        self.MS = world.windowWidth / 240
        self.jumpSpeed = world.windowHeight / 45 * 1.5
        self.dmgLava = False


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
        #rint(self.curSpeedY)
        self.curSpeedY += world.gravity
        # print(self.curSpeedY)
        #print(int(-4.6))
