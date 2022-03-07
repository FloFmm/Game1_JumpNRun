from World import *
from Player import *
from Ground import *
from InGame import *
from MainMenu import *
from Background import*

import pygame

pygame.init()
pygame.display.set_caption("Jump n Run")
clock = pygame.time.Clock()

world = World()
ground = Ground(world, 50, 350)
player1 = Player(world, 200, 200, 100)
# button1 = Button(200, 200, 100, 50, "button1")
mainMenu = MainMenu(world, clock)
inGame = InGame(world, clock, player1)


while True:

    if world.menuLocation == "start-menu":
        mainMenu.run(world, clock)
    else:
        exitReason = inGame.run(world, clock, player1, ground)
        if exitReason == "death":
            # reset
            ground = Ground(world, 50, 350)
            player1 = Player(world, 200, 200, 100)
            inGame = InGame(world, clock, player1)






