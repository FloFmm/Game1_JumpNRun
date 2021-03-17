import pygame
from otherFunctions import posOrNeg


class Block:
    def __init__(self, world, blockWidth, rawBlockHeight, blockX = 0, blockY = 0):
        self.width = blockWidth
        self.rawHeight = rawBlockHeight
        self.height = int(self.rawHeight * world.windowHeight / 1000)
        self.XC = blockX
        self.YC = blockY
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))

    # updates the rect and then draws it on the world.window
    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, self.color, self.blockRect)


class GroundBlock(Block):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockWidth, rawBlockHeight, blockX)
        self.YC = world.windowHeight - self.height
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))


class StdBlock(GroundBlock):


    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.color = (255, 255, 255)

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        if XorY == 'x':
            return self.xCollision(world, ground, collidedObj, collidedBlock)
        else:
            return self.yCollision(world, ground, collidedObj, collidedBlock)


    def xCollision(self, world, ground, collidedObj, collidedBlock):
        xStep = posOrNeg(collidedObj.curSpeedX)
        if ground.overlappedX(collidedObj, collidedBlock) < ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
            collidedObj.curSpeedX = 0
            return True
        return False

    def yCollision(self, world, ground, collidedObj, collidedBlock):
        yStep = posOrNeg(collidedObj.curSpeedY)
        if ground.overlappedX(collidedObj, collidedBlock) > ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.YC -= yStep * ground.overlappedY(collidedObj, collidedBlock)
            collidedObj.curSpeedY = 0
            collidedObj.jumpMark = collidedObj.maxJumps
            return True
        return False


class LavaBlock (GroundBlock):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.dmg = 50/60
        self.slow = 50
        self.color = (200, 0, 0)

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        collidedObj.MS = world.windowWidth / 240 * self.slow / 100

        # print(f"Restspeed: {collidedObj.restYS}")
        # print(f"speed: {collidedObj.curSpeedY}")

        if collidedObj.curSpeedY >= 0:
            collidedObj.curSpeedY = 0.8  # world.windowHeight / 1000

        collidedObj.HP -= self.dmg

        return False










