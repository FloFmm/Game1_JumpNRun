import pygame
from random import randint

pygame.init()
blockAmount = 14
windowWidth = 1200
windowHeight = 600
gravity = 1
gameMovementSpeed = 2
worldScale = 10


window = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
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
        self.maxJumps = 2
        self.jumpMark = self.maxJumps
        # self.inJump = False
        self.displayPlayer()

    def updateScale(self):
        self.playerHeight = int(windowHeight/worldScale)
        self.playerWidth = int(windowWidth/(worldScale*4))

    def displayPlayer(self):
        self.playerRect = pygame.Rect((self.playerXC, self.playerYC, self.playerWidth, self.playerHeight))
        pygame.draw.rect(window, (255, 0, 0), self.playerRect)

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
            #if self.outOfScreenX():
            #   self.playerXC -= xStep
            #   self.curSpeedX = 0
            #   break
            if ground.groundCollisionX() == 0:
                self.playerXC += xStep
            else:
                self.playerXC -= xStep
                break

        for i in range(toUnsigned(self.curSpeedY)):
            #if self.outOfScreenY():
            #    self.playerYC += 2
            #    self.curSpeedY = 0
            #    break
            if ground.groundCollisionY() == 0:
                self.playerYC += yStep
            else:
                self.jumpMark = self.maxJumps
                val = ground.groundCollisionY() - 1
                #print(f"{Player1.playerYC} + {Player1.playerHeight} - {ground.groundArray[ground.groundCollisionY()-1].blockY} = {Player1.playerHeight + Player1.playerYC - ground.groundArray[ground.groundCollisionY()-1].blockY}")
                self.playerYC -= 1
                print(
                    f"{Player1.playerYC} + {Player1.playerHeight} - {ground.groundArray[val].blockY} = {Player1.playerHeight + Player1.playerYC - ground.groundArray[val].blockY}")
                break

        if toUnsigned(oldXpos - self.playerXC) == 1: self.playerXC = oldXpos
        if oldYpos - self.playerYC == -1: self.playerYC = oldYpos # 1 Pixel upwards works, 1 Pixel downwards doesn´t

    def jump(self):

        if self.jumpMark > 0:
            self.jumpMark -= 1
            Player1.curSpeedY = -Player1.jumpSpeed


    def outOfScreenX(self):
        if self.playerXC < 0 or self.playerXC + self.playerWidth >= windowWidth:
            return True
        return False

    def outOfScreenY(self):
        if self.playerYC < 0 or self.playerYC + self.playerHeight >= windowHeight:
            return True
        return False


    def gravity(self):
        self.curSpeedY += gravity

    # def jump(self):
      #  self.playerYC -= self.jumpSpeed
      #  self.jumpSpeed -= Acceleration


class GroundBlock:

    def __init__(self, blockWidth, rawBlockHeight, blockX):
        self.blockWidth = blockWidth
        self.rawBlockHeight = rawBlockHeight
        self.blockHeight = int(rawBlockHeight * windowHeight / 1000)
        self.blockX = blockX
        self.blockY = windowHeight - self.blockHeight
        self.blockRect = pygame.Rect((self.blockX, self.blockY, self.blockWidth, self.blockHeight))


    def drawBlock(self):
        self.blockRect = pygame.Rect((self.blockX, self.blockY, self.blockWidth, self.blockHeight))
        pygame.draw.rect(window, (255, 255, 255), self.blockRect)




class Ground:

    def __init__(self, blockAmount, groundMin, groundMax):
        self.groundMin = groundMin
        self.groundMax = groundMax
        self.blockWidth = int(windowWidth / blockAmount)
        self.groundArray = []
        self.blockHeight = 20
        self.blockAmount = blockAmount
        self.initGroundArray()
        self.distanceMoved = 0

    def initGroundArray(self):
        for i in range(self.blockAmount+1):
            self.groundArray.append(GroundBlock(self.blockWidth, randint(self.groundMin, self.groundMax), self.blockWidth*i))

    def updateWorld(self):
        self.distanceMoved += gameMovementSpeed
        for j in range(self.blockAmount + 1):
            self.groundArray[j].blockWidth = int(windowWidth / blockAmount)
            self.groundArray[j].blockX = windowWidth - (
                        (windowWidth - j * self.groundArray[j].blockWidth + self.distanceMoved) % (
                        windowWidth + self.groundArray[j].blockWidth))
            self.distanceMoved = self.distanceMoved % ( windowWidth + self.groundArray[j].blockWidth)

            if self.groundArray[j].blockX >= windowWidth-1:
                self.groundArray[j].rawBlockHeight = randint(ground.groundMin, ground.groundMax)
            self.groundArray[j].blockHeight = int(self.groundArray[j].rawBlockHeight * windowHeight / 1000)
            self.groundArray[j].blockY = 1 + windowHeight - self.groundArray[j].blockHeight

            self.groundArray[j].blockRect = pygame.Rect((self.groundArray[j].blockX, self.groundArray[j].blockY,
                                                        self.groundArray[j].blockWidth,
                                                        self.groundArray[j].blockHeight))
        self.groundArray[blockAmount].blockWidth += windowWidth - blockAmount * self.groundArray[blockAmount].blockWidth
            #self.groundArray[j].rawBlockHeight = randint(ground.groundMin, ground.groundMax)

          #  self.groundArray[j].blockX = i * self.groundArray[j].blockWidth






    def groundCollisionY(self):
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("y", i):
                    Player1.curSpeedY = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    return i + 1
        return 0

    def groundCollisionX(self):
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("x", i):
                    Player1.curSpeedX = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    return i + 1
        return 0




def Collision(mode, i):
    if mode == "b" or mode == "B":
        return Player1.playerYC + Player1.playerHeight -1 > windowHeight - ground.groundArray[i].blockHeight and Player1.playerYC < windowHeight and Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth
    if mode == "x" or mode == "X":
        return Player1.playerYC + Player1.playerHeight -1 > windowHeight - ground.groundArray[i].blockHeight and Player1.playerYC < windowHeight
    if mode == "y" or mode == "Y":
        return Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth


def overlappedRect(x1, y1, width1, height1, x2, y2, width2, height2):
    return x1 + width1 > x2 and x1 < x2 + width2 and y1 + height1 > y2 and y1 < y2 + height2


def toUnsigned(x):
    if(x<0):
        return -x
    return x

ground = Ground(blockAmount, 50, 350)

Player1 = Player(80, 40, 200, 200, 5, 15)
# Player2 = Player(40, 80, 400, 400, 5)

pygame.key.set_repeat(50, 50)


while True:
    windowWidth, windowHeight = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()



    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_RIGHT]:
        Player1.curSpeedX = Player1.playerMS
    elif keysPressed[pygame.K_LEFT]:
        Player1.curSpeedX = -Player1.playerMS
    else:
        Player1.curSpeedX = 0
    if keysPressed[pygame.K_SPACE]:
        if spaceHold == 0:
            spaceHold = 1
            if Player1.jumpMark != 0:
                print(Player1.jumpMark)
            Player1.jump()
    else:
        spaceHold = 0

        #Player1.playerYC -= 1


    #print(ground.groundArray[5].blockHeight)


    #update all sizes
    Player1.updateScale()
    ground.updateWorld()

    #updating all positions
    Player1.gravity()
    Player1.playerXC -= gameMovementSpeed
    Player1.move()


    #displaying everything
    for i in range(blockAmount+1):
        ground.groundArray[i].drawBlock()

    Player1.displayPlayer()



    pygame.display.flip()
    window.fill((0, 0, 0))
    clock.tick(60)