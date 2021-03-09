import pygame


class World:

    def __init__(self):
        self.blockAmount = 14
        self.windowWidth = 1200
        self.windowHeight = 600
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.gravity = int((self.windowHeight / 600 * 2 + 1) / 2)  # 1
        self.gameMS = int((self.windowWidth / 600 * 2 + 1) / 2)
        self.playerSize = 10
        self.spaceHold = False
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE)

    def updateWorld(self):
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.windowWidth, self.windowHeight = pygame.display.get_surface().get_size()
        self.gameMS = int((self.windowWidth / 600 * 2 + 1) / 2)
