import pygame

class Button:

    def __init__(self,buttonID, positionX, positionY, sizeX, sizeY, text = "", color = [120, 120, 120], borderC = [255, 255, 255],
                 borderWidth = 5, fontSize = 20):
        self.ID = buttonID
        self.XC = positionX
        self.YC = positionY
        self.width = sizeX
        self.height = sizeY
        self.color = color
        self.borderC = borderC
        self.borderWidth = borderWidth
        self.outerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.innerRect = pygame.Rect((self.XC + borderWidth, self.YC + borderWidth, self.width - 2*borderWidth,
                                      self.height - 2*borderWidth))
        self.font = pygame.font.SysFont('Arial', fontSize)
        self.fontSize = fontSize
        self.text = text
        self.keydown = False

    def setColor(self, color):

        for i in range(len(color)):
            if color[i] > 255:
                color[i] = 255
                continue
            if color[i] < 0:
                color[i] = 0

        self.color = color

    def setBorderC(self, color):

        for i in range(len(color)):
            if color[i] > 255:
                color[i] = 255
                continue
            if color[i] < 0:
                color[i] = 0

        self.borderC = color

    def draw(self, world):
        self.outerRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, self.borderC, self.outerRect)
        self.innerRect = pygame.Rect((self.XC + self.borderWidth, self.YC + self.borderWidth, self.width - 2*self.borderWidth,
                                      self.height - 2*self.borderWidth))
        pygame.draw.rect(world.window, self.color, self.innerRect)
        ##world.window.blit(self.font.render(self.text, True, (255, 0, 0)), (self.XC + self.borderWidth + 7,
          #                                                                self.YC + self.height/2 + self.fontSize/2))

        img = self.font.render(self.text, True, (0,0,0))
        world.window.blit(img, (self.XC + self.borderWidth + 7, self.YC + self.height/2 - self.fontSize/2))

    def hovered(self):
        mouseC = pygame.mouse.get_pos()
        if (mouseC[0] >= self.XC) and (mouseC[0] <= self.XC + self.width) and (mouseC[1] >= self.YC) and (mouseC[1] <= self.YC + self.width):
            print("hovered")
        return (mouseC[0] >= self.XC) and (mouseC[0] <= self.XC + self.width) and (mouseC[1] >= self.YC) and (mouseC[1] <= self.YC + self.height)

    def clicked(self):
        if not self.hovered():
            self.keydown = False
            return False
        if self.keydown:
            if not pygame.mouse.get_pressed()[0]:
                    self.keydown = False
                    return True
            return False
        else:
            if pygame.mouse.get_pressed()[0]:
                self.keydown = True
        return False

