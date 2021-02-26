import pygame
from random import randint

pygame.init()
blockAmount = 12
windowWidth = 1200
windowHeight = 600
gravity = 1


window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Jump n Run")
clock = pygame.time.Clock()



class Player:


    def __init__ (self, playerHeight, playerWidth, playerXC, playerYC, playerMS, jumpSpeed):
        self.playerHeight = playerHeight
        self.playerWidth = playerWidth
        self.playerXC = playerXC
        self.playerYC = playerYC
        self.playerMS = playerMS
        self.jumpSpeed = jumpSpeed
        self.curSpeedX = 0
        self.curSpeedY = 0
        # self.inJump = False
        self.displayPlayer()

    def displayPlayer(self):
        self.playerRect = pygame.Rect((self.playerXC, self.playerYC, self.playerWidth, self.playerHeight))
        pygame.draw.rect(window, (255, 255, 255), self.playerRect)

    def move(self):

        oldYpos = self.playerYC
        oldXpos = self.playerXC

        if self.curSpeedX > 0:
            xStep = 1
        elif self.curSpeedX < 0:
            xStep = -1

        if self.curSpeedY > 0:
            yStep = 1
        elif self.curSpeedY < 0:
            yStep = -1

        for i in range(toUnsigned(self.curSpeedX)):
            if (ground.groundCollisionX() == 0):
                self.playerXC += xStep
            else:
                self.playerXC -= xStep
                break

        for i in range(toUnsigned(self.curSpeedY)):
            if (ground.groundCollisionY() == 0):
                self.playerYC += yStep
            else:
                self.playerYC -= 1
                break

        if toUnsigned(oldXpos - self.playerXC) == 1: self.playerXC = oldXpos
        if toUnsigned(oldYpos - self.playerYC) == 1: self.playerYC = oldYpos


    def gravity(self):
        self.curSpeedY += gravity

    # def jump(self):
      #  self.playerYC -= self.jumpSpeed
      #  self.jumpSpeed -= Acceleration


class GroundBlock:

    def __init__(self, blockWidth, blockHeight, blockX):
        self.blockWidth = blockWidth
        self.blockHeight = blockHeight
        self.blockX = blockX
        self.blockRect = pygame.Rect((self.blockX, windowHeight-self.blockHeight, self.blockWidth, self.blockHeight))


    def drawBlock(self):
        pygame.draw.rect(window, (255, 255, 255), self.blockRect)


class Ground:

    def __init__(self, blockAmount):
        self.blockWidth = windowWidth / blockAmount
        self.groundArray = []
        self.blockHeight = 20
        self.blockAmount = blockAmount
        self.initGroundArray()

    def initGroundArray(self):
        for i in range(self.blockAmount+1):
            self.groundArray.append(GroundBlock(self.blockWidth, randint(5,200), self.blockWidth*i))

    def groundCollisionY(self):
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("y", i):
                    Player1.curSpeedY = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    return 1
        return 0

    def groundCollisionX(self):
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("x", i):
                    Player1.curSpeedX = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    return 1
        return 0


def Collision(mode, i):
    if mode == "b" or mode == "B":
        return Player1.playerYC + Player1.playerHeight > windowHeight - ground.groundArray[i].blockHeight and Player1.playerYC < windowHeight and Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth
    if mode == "x" or mode == "X":
        return Player1.playerYC + Player1.playerHeight > windowHeight - ground.groundArray[i].blockHeight and Player1.playerYC < windowHeight
    if mode == "y" or mode == "Y":
        return Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth




def toUnsigned(x):
    if(x<0):
        return -x
    return x

ground = Ground(blockAmount)

Player1 = Player(80, 40, 200, 200, 5, 15)
# Player2 = Player(40, 80, 400, 400, 5)



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    Player1.displayPlayer()

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_RIGHT]:
        Player1.curSpeedX = Player1.playerMS
    elif keysPressed[pygame.K_LEFT]:
        Player1.curSpeedX = -Player1.playerMS
    else:
        Player1.curSpeedX = 0
    if keysPressed[pygame.K_SPACE]:
        Player1.curSpeedY = -Player1.jumpSpeed
        Player1.playerYC -= 5

    Player1.gravity()

    Player1.move()


    for i in range(blockAmount+1):
        ground.groundArray[i].drawBlock()




    pygame.display.flip()
    window.fill((0, 0, 0))
    clock.tick(60)
