from World import *
from Player import *
from Ground import *

import pygame

pygame.init()
pygame.display.set_caption("Jump n Run")
clock = pygame.time.Clock()

world = World()
ground = Ground(world, 50, 350)
player1 = Player(world, 200, 200, 100)

while True:

    # exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # saving pressed keys
    keysPressed = pygame.key.get_pressed()

    # key action
    if keysPressed[pygame.K_RIGHT]:
        player1.curSpeedX = player1.MS
    elif keysPressed[pygame.K_LEFT]:
        player1.curSpeedX = -player1.MS
    else:
        player1.curSpeedX = 0
    if keysPressed[pygame.K_SPACE]:
        if not world.spaceHold:   # allowing jump only when key has previously been released
            player1.jump()  # -> only one jump mark is used when pressing the key once (and holding it)
            world.spaceHold = True
    else:
        world.spaceHold = False

    # updates all properties of the whole world
    world.updateWorld()

    # update all sizes
    player1.updateScale(world)
    ground.updateGround(world)

    # update all positions
    player1.gravity(world)
    player1.move(world, ground)

    # display content
    for i in range(world.blockAmount+1):
        ground.groundArray[i].drawBlock(world)
    player1.display(world)

    #ground.groundArray[5].xCollision(world, ground, player1, 1, ground.groundArray[5])

    # pygame stuff
    pygame.display.flip()
    world.window.fill((0, 0, 0))
    clock.tick(60)

