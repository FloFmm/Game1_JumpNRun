import pygame
import copy
from otherFunctions import posOrNeg


class Block:
    def __init__(self, world, blockWidth=0, rawBlockHeight = 0, blockX = 0, blockY = 0, image_source = 'images/blocks/grass_block.png'):
        self.width = blockWidth
        self.rawHeight = rawBlockHeight  # relative Height of the Block
        self.height = int(world.windowHeight * self.rawHeight / 1000)
        self.old_width = 0
        self.old_height = 0
        self.XC = blockX
        self.YC = blockY
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.color = (0,0,0)

        self.block_image = pygame.image.load(image_source)
        self.block_image.convert()
        self.block_image_to_draw = copy.copy(self.block_image).convert()
        self.block_image_to_draw = pygame.transform.scale(self.block_image_to_draw, (int(self.width), (int(self.width*16))))
        #self.block_image = pygame.transform.scale(self.block_image, (self.width,  self.height))

    # updates the rect and then draws it on the world.window
    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        pygame.draw.rect(world.window, self.color, self.blockRect)
        self.block_image = pygame.transform.scale(self.block_image, (int(self.width), self.height))
        world.window.blit(self.block_image, (self.XC, self.YC))

class HealthBar(Block):

    def __init__ (self, world):
        super().__init__(world, int((1/3) * world.windowWidth), int(world.windowHeight / 20), int(world.windowHeight / 20),
                         int(world.windowHeight / 20))
        self.color = (255, 0, 0)


    def updateHealthBar(self, world, creature):
        self.height = int(world.windowHeight / 20)
        self.XC = int(world.windowHeight / 20)
        self.YC = int(world.windowHeight / 20)
        self.width = (1/3) * world.windowWidth * creature.HP / creature.maxHP




class GroundBlock(Block):
    width = 0

    def __init__(self, world, blockX, rawBlockHeight, image_source = 'images/blocks/grass_block.png'):
        super().__init__(world, 0, rawBlockHeight, blockX, 0, image_source)
        self.YC = world.windowHeight - self.height
        #self.blockRect = pygame.Rect((self.XC, self.YC, self.width, self.height))
        self.blockRepeat = 0
        self.blockType = "ground_block"

    def drawBlock(self, world):
        self.blockRect = pygame.Rect((self.XC, self.YC, GroundBlock.width, self.height))
        #pygame.draw.rect(world.window, self.color, self.blockRect)

        #print("height")
        #print(self.width)
        #print("oldheight")
        #print(self.old_width)
        #print(self.blockType)
        if not GroundBlock.width == self.width:
            self.block_image_to_draw = copy.copy(self.block_image)
            self.block_image_to_draw = pygame.transform.scale(self.block_image_to_draw, (int(GroundBlock.width), (int(GroundBlock.width * 16))))
            self.block_image_to_draw.convert()
            self.width = GroundBlock.width

        #if not self.height == self.old_height or not GroundBlock.width == GroundBlock.old_width:
        #    self.block_image_to_draw = copy.copy(self.block_image)
        #    self.block_image_to_draw = pygame.transform.scale(self.block_image_to_draw, (int(GroundBlock.width), (int(GroundBlock.width*16))))
        #    self.block_image_to_draw.convert()
        #    print("not equal")
        cropped_region = (0, 0, GroundBlock.width, self.height)
        world.window.blit(self.block_image_to_draw, (self.XC, self.YC),cropped_region)

class StdBlock(GroundBlock):


    def __init__(self, world, blockX, rawBlockHeight):
        super().__init__(world, blockX, rawBlockHeight, 'images/blocks/grass_block.png')
        self.color = (40, 100, 0)
        self.blockType = "std"

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        if XorY == 'x':
            return self.xCollision(ground, collidedObj, collidedBlock)
        else:
            return self.yCollision(ground, collidedObj, collidedBlock)


    def xCollision(self, ground, collidedObj, collidedBlock):
        xStep = posOrNeg(collidedObj.curSpeedX)
        if ground.overlappedX(collidedObj, collidedBlock) < ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
            collidedObj.curSpeedX = 0
            return True
        return False

    def yCollision(self, ground, collidedObj, collidedBlock):
        yStep = posOrNeg(collidedObj.curSpeedY)
        if ground.overlappedX(collidedObj, collidedBlock) > ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.YC -= yStep * ground.overlappedY(collidedObj, collidedBlock)
            collidedObj.curSpeedY = 0
            collidedObj.jumpMark = collidedObj.maxJumps
            return True
        return False


class LavaBlock (GroundBlock):

    def __init__(self, world, blockX, rawBlockHeight):
        super().__init__(world, blockX, rawBlockHeight, 'images/blocks/lava_block.png')
        self.dmg = 50/60
        self.slow = 50
        self.color = (200, 0, 0)
        self.blockType = "lava"

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        collidedObj.MS = world.windowWidth / 240 * self.slow / 100

        if collidedObj.curSpeedY >= 0:
            collidedObj.curSpeedY = world.windowHeight / 1000

        if not collidedObj.dmgLava:
            collidedObj.HP -= self.dmg
            collidedObj.dmgLava = True

        return False

class BounceBlock (GroundBlock):

    def __init__(self, world, blockX, rawBlockHeight):
        super().__init__(world, blockX, rawBlockHeight,'images/blocks/jump_block.png')
        self.blockType = "bounce"
        self.color = (20, 20, 60)

    def Collision(self, world, ground, XorY, collidedBlock, collidedObj):
        if XorY == 'x':
            return self.xCollision(ground, collidedObj, collidedBlock)
        else:
            return self.yCollision(ground, collidedObj, collidedBlock)

    def xCollision(self, ground, collidedObj, collidedBlock):
        xStep = posOrNeg(collidedObj.curSpeedX)
        if ground.overlappedX(collidedObj, collidedBlock) < ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.XC -= xStep * ground.overlappedX(collidedObj, collidedBlock)
            collidedObj.curSpeedX = 0
            return True
        return False

    def yCollision(self, ground, collidedObj, collidedBlock):
        yStep = posOrNeg(collidedObj.curSpeedY)
        if ground.overlappedX(collidedObj, collidedBlock) > ground.overlappedY(collidedObj, collidedBlock):
            collidedObj.YC -= yStep * ground.overlappedY(collidedObj, collidedBlock)
            #print(collidedObj.curSpeedY)
            collidedObj.curSpeedY = -collidedObj.curSpeedY
            #print(collidedObj.curSpeedY)
            collidedObj.jumpMark = collidedObj.maxJumps
            return True
        return False











