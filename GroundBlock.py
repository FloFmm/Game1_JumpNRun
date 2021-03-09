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
    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, (255, 255, 255), self.blockRect)
