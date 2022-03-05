import pygame
from otherFunctions import *

class InGame:

    def __init__(self, world, clock, player):

        self.world = world
        self.clock = clock
        self.player = player

    def draw(self, world):
        pass

    def processKeyPressings(self, player, world):
        # saving pressed keys
        keysPressed = pygame.key.get_pressed()

        # key action
        if keysPressed[pygame.K_RIGHT]:
            player.curSpeedX = player.MS
        elif keysPressed[pygame.K_LEFT]:
            player.curSpeedX = -player.MS
        else:
            player.curSpeedX = 0
        if keysPressed[pygame.K_SPACE]:
            if not world.spaceHold:  # allowing jump only when key has previously been released
                player.jump()  # -> only one jump mark is used when pressing the key once (and holding it)
                world.spaceHold = True
        else:
            world.spaceHold = False

    def update(self, world, player, ground):

        # updates all properties of the whole world
        world.updateWorld()

        # update all sizes
        player.updateScale(world)
        ground.updateGround(world)

        # update all positions
        player.gravity(world)
        player.move(world, ground)

    def run(self, world, clock, player, ground):
        # print(self.buttons[0].ID)
        while True:
            # exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.processKeyPressings(player, world)

            self.update(world, player, ground)

            # display content
            for i in range(world.blockAmount + world.blockBuffer):
                ground.groundArray[i].drawBlock(world)
            player.display(world)

            if self.player.HP <= 0 or self.player.YC > world.windowHeight + 100:
                world.menuLocation = "start-menu"
                exitReason = "death"
                return exitReason

            gameRender(world, clock)








