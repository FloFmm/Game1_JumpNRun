import pygame
from otherFunctions import posOrNeg


class Block:
    def __init__(self, world, blockWidth=0, rawBlockHeight = 0, blockX = 0, blockY = 0):
        self.width = blockWidth
        self.rawHeight = rawBlockHeight  # relative Height of the Block
        self.height = int(world.windowHeight * self.rawHeight / 1000)
        self.XC = blockX
        self.YC = blockY
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))

    # updates the rect and then draws it on the world.window
    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, self.color, self.blockRect)

class HealthBar(Block):

    def __init__ (self, world):
        super().__init__(world)
        self.color = (255, 0, 0)


    def updateHealthBar(self, world, creature):
        self.height = int(world.windowHeight / 20)
        self.XC = int(world.windowHeight / 20)
        self.YC = int(world.windowHeight / 20)
        self.width = (1/3) * world.windowWidth * creature.HP / creature.maxHP



class GroundBlock(Block):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockWidth, rawBlockHeight, blockX)
        self.YC = world.windowHeight - self.height
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.blockRepeat = 0


class StdBlock(GroundBlock):


    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.color = (40, 100, 0)
        self.blockType = "std"

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        if XorY == 'x':
            return self.xCollision(ground, collidedObj, collidedBlock)
        else:
            return self.yCollision(ground, collidedObj, collidedBlock)


    def xCollision(self, ground, collidedObj, collidedBlock):
        xStep = posOrNeg(collidedObj.curSpeedX)
        if ground.overlappedX(collidedObj, collidedBlock) < ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
            collidedObj.curSpeedX = 0
            return True
        return False

    def yCollision(self, ground, collidedObj, collidedBlock):
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
        self.blockType = "lava"

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        collidedObj.MS = world.windowWidth / 240 * self.slow / 100

        if collidedObj.curSpeedY >= 0:
            collidedObj.curSpeedY = world.windowHeight / 1000

        if not collidedObj.dmgLava:
            collidedObj.HP -= self.dmg
            collidedObj.dmgLava = True

        return False

class BounceBlock (GroundBlock):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.blockType = "bounce"

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        if XorY == 'x':
            return self.xCollision(ground, collidedObj, collidedBlock)
        else:
            return self.yCollision(ground, collidedObj, collidedBlock)

    def xCollision(self, ground, collidedObj, collidedBlock):
        xStep = posOrNeg(collidedObj.curSpeedX)
        if ground.overlappedX(collidedObj, collidedBlock) < ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
            collidedObj.curSpeedX = 0
            return True
        return False

    def yCollision(self, ground, collidedObj, collidedBlock):
        yStep = posOrNeg(collidedObj.curSpeedY)
        if ground.overlappedX(collidedObj, collidedBlock) > ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.YC -= yStep * ground.overlappedY(collidedObj, collidedBlock)
            collidedObj.curSpeedY = -collidedObj.curSpeedY
            collidedObj.jumpMark = collidedObj.maxJumps
            return True
        return False











