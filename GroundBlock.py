import pygame


class Block:

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        self.width = blockWidth
        self.rawHeight = rawBlockHeight
        self.height = int(self.rawHeight * world.windowHeight / 1000)
        self.XC = blockX
        self.YC = world.windowHeight - self.height
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))

    # updates the rect and then draws it on the world.window
    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, self.color, self.blockRect)


class GroundBlock(Block):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.color = (255, 255, 255)

    def xCollision(self, world, ground, collidedObj, xStep, collidedBlock):
        collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
        collidedObj.curSpeedX = 0

        return True

    def yCollision(self, world, ground, collidedObj, yStep, collidedBlock):
        collidedObj.YC -= yStep * ground.overlappedY(collidedObj, collidedBlock)
        collidedObj.curSpeedY = 0
        collidedObj.jumpMark = collidedObj.maxJumps

        return True


class LavaBlock (Block):

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.dmg = 50/60
        self.slow = 50
        self.color = (200, 0, 0)

    def xCollision(self, world, ground, collidedObj, xStep, collidedBlock):
        collidedObj.MS = world.windowWidth / 240 * self.slow / 100

        if collidedObj.curSpeedY >= 0:
            collidedObj.curSpeedY = world.windowHeight / 1000

        collidedObj.HP -= self.dmg

        return False

    def yCollision(self, world, ground, collidedObj, yStep, collidedBlock):
        return self.xCollision(world, ground, collidedObj, yStep, collidedBlock)










