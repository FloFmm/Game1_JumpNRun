import pygame
import copy
class Background:
    def __init__(self, image_source = "images/backgrounds/background"):
        self.window_width_old = 0
        self.window_height_old = 0
        self.image = pygame.image.load(image_source)
        self.image.convert()

    def draw(self, world):
        if world.windowWidth != self.window_width_old or world.windowHeight != self.window_height_old:
            self.image_to_draw = copy.copy(self.image).convert()
            self.image_to_draw = pygame.transform.scale(self.image_to_draw, (world.windowWidth, world.windowHeight))
            print("not equal")
            self.window_width_old = world.windowWidth
            self.window_height_old = world.windowHeight
        world.window.blit(self.image_to_draw, (0, 0))