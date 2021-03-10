import pygame




class GroundBlock:

    def __init__(self, world, blockX, blockWidth, rawBlockHeight):
        self.width = blockWidth
        self.rawHeight = rawBlockHeight
        self.height = int(self.rawHeight * world.windowHeight / 1000)
        self.XC = blockX
        self.YC = world.windowHeight - self.height
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))

    # updates the rect and then draws it on the world.window
    def drawBlock(self, world, blockColor = (255, 255, 255)):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, blockColor, self.blockRect)

   # def collision(self):




class LavaBlock (GroundBlock):

    def __init__(self,world, blockX, blockWidth, rawBlockHeight):
        super().__init__(world, blockX, blockWidth, rawBlockHeight)
        self.dmg = 10
        self.slow = 50
        self.color = (200, 0, 0)

    def xCollision(self, collidedObj):
        collidedObj.curSpeedX = collidedObj.curSpeedX * self.slow / 100
        collidedObj.curSpeedY = collidedObj.curSpeedY * self.slow / 100
        collidedObj.health -= self.dmg












