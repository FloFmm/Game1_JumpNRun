from Button import *
import pygame
from otherFunctions import *
class MainMenu:

    def __init__(self, world, clock):
        self.buttons = []
        self.buttons.append(
            Button("go-in-game", world.windowWidth/2 - 100, world.windowHeight/2 - 50, 200, 100, "Play")
        )
        self.world = world
        self.clock = clock

    def draw(self, world):
        for button in self.buttons:
            button.draw(world)

    def run(self, world, clock):
        # print(self.buttons[0].ID)
        while True:
            # exit button NEEEEDED111!!!111
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.draw(world)
            if self.buttons[0].clicked():
                world.menuLocation = "in-game"
                return
            gameRender(world, clock)




