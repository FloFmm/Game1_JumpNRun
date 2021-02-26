import pygame
from random import randint

pygame.init()
blockAmount = 12
windowWidth = 1200
windowHeight = 600
Acceleration = 1


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
        self.inJump = False
        self.displayPlayer()

    def displayPlayer(self):
        self.playerRect = pygame.Rect((self.playerXC, self.playerYC, self.playerWidth, self.playerHeight))
        pygame.draw.rect(window, (255, 255, 255), self.playerRect)

    def move(self, direction):
        if direction > 0:
            self.playerXC += self.playerMS
        else:
            self.playerXC -= self.playerMS

    def jump(self):
        self.playerYC -= self.jumpSpeed
        self.jumpSpeed -= Acceleration


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

    def groundCollision(self):
        for i in range(self.blockAmount+1):
            if(Player1.playerRect.colliderect(self.groundArray[i].blockRect)):
                Player1.inJump = False
                Player1.playerYC = windowHeight-self.groundArray[i].blockHeight-Player1.playerHeight
                return True


def toUnsigned(x):
    if(x<0):
        return -x
    return x

ground = Ground(blockAmount)

Player1 = Player(80, 40, 200, 200, 5, 15)
# Player2 = Player(40, 80, 400, 400, 5)



while True:
    if ground.groundCollision():
        Player1.jumpSpeed = 15



    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    Player1.displayPlayer()
    # displayPlayer()

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_RIGHT]:
        Player1.move(1)
    if keysPressed[pygame.K_LEFT]:
        Player1.move(-1)
    if keysPressed[pygame.K_SPACE]:
        Player1.inJump = True

    if Player1.inJump:
       Player1.jump()
     #   for i in range(toUnsigned(Player1.jumpSpeed)):
      #      if (ground.groundCollision()):
       #         Player1.jumpSpeed = 15
        ##        break
           # if Player1.jumpSpeed > 0:
          #      Player1.playerYC -= 1
            #elif Player1.jumpSpeed < 0:
            #    Player1.playerYC += 1

    for i in range(blockAmount+1):
        ground.groundArray[i].drawBlock()




    pygame.display.flip()
    window.fill((0, 0, 0))
    clock.tick(60)
