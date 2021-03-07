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
        self.jumpSpeed = int(windowHeight/45)

    def displayPlayer(self):
        self.playerRect = pygame.Rect((self.playerXC, self.playerYC, self.playerWidth, self.playerHeight))
        pygame.draw.rect(window, (255, 0, 0), self.playerRect)

    def move(self):
        xStep = 0
        yStep = 0
        if self.curSpeedX > 0:
            xStep = 1
        elif self.curSpeedX < 0:
            xStep = -1

        if self.curSpeedY > 0:
            yStep = 1
        elif self.curSpeedY < 0:
            yStep = -1

        leave = False
        for i in range(toUnsigned(self.curSpeedX)):
            self.playerXC += xStep
            collidedBlocks = ground.groundCollision()
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(collidedBlocks[j] - 1) < ground.overlappedY(collidedBlocks[j] - 1):
                    self.playerXC -= xStep * ground.overlappedX(collidedBlocks[j] - 1)
                    Player1.curSpeedX = 0
                    leave = True
            if leave:
                break


        leave = False
        for i in range(toUnsigned(self.curSpeedY)):
            self.playerYC += yStep
            collidedBlocks = ground.groundCollision()
            for j in range(len(collidedBlocks)):
                if ground.overlappedX(collidedBlocks[j] - 1) > ground.overlappedY(collidedBlocks[j] - 1):
                    self.playerYC -= yStep * (ground.overlappedY(collidedBlocks[j] - 1))
                    Player1.curSpeedY = 0
                    self.jumpMark = self.maxJumps
                    leave = True
            if leave:
                break

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
        arr =[]
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("y", i):
                    Player1.curSpeedY = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    arr.append(i+1)
        return arr

    def groundCollisionX(self):
        arr = []
        for i in range(self.blockAmount+1):
            if Collision("b", i):
                if Collision("x", i):
                    Player1.curSpeedX = 0
                    # Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                    arr.append(i+1)
        return arr

    def groundCollision(self):
        arr = []
        for i in range(self.blockAmount + 1):
            if Collision("b", i):
                arr.append(i + 1)
        return arr


    def overlappedX(self, block):
        rightFromPlayer = Player1.playerXC + Player1.playerWidth - self.groundArray[block].blockX
        leftFromPlayer = self.groundArray[block].blockX + self.groundArray[block].blockWidth - Player1.playerXC
        if rightFromPlayer < leftFromPlayer:
            return rightFromPlayer
        else:
            return leftFromPlayer

    def overlappedY(self, block):
        belowPlayer = Player1.playerYC + Player1.playerHeight - self.groundArray[block].blockY
        abovePlayer = self.groundArray[block].blockY + self.groundArray[block].blockHeight - Player1.playerYC
        if belowPlayer < abovePlayer:
            return belowPlayer
        else:
            return abovePlayer



def Collision(mode, i):
    if mode == "b" or mode == "B":
        return Player1.playerYC + Player1.playerHeight - 1 > windowHeight - ground.groundArray[i].blockHeight\
            and Player1.playerYC < windowHeight\
            and Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX\
            and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth
    if mode == "x" or mode == "X":
        return Player1.playerYC + Player1.playerHeight - 1 > windowHeight - ground.groundArray[i].blockHeight\
            and Player1.playerYC < windowHeight
    if mode == "y" or mode == "Y":
        return Player1.playerXC + Player1.playerWidth > ground.groundArray[i].blockX \
            and Player1.playerXC < ground.groundArray[i].blockX + ground.groundArray[i].blockWidth




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