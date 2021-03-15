import pygame


class World:

    def __init__(self):
        self.blockAmount = 14
        self.windowWidth = 1200
        self.windowHeight = 600
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.gameMS = 0  # self.windowWidth / 600
        self.gravity = self.windowHeight / 600
        self.playerSize = 10
        self.spaceHold = False
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE)

    def updateWorld(self):
        self.windowWidthOld = self.windowWidth
        self.windowHeightOld = self.windowHeight
        self.windowWidth, self.windowHeight = pygame.display.get_surface().get_size()
        self.gameMS = 0  # self.windowWidth / 600
        self.gravity = self.windowHeight / 600
