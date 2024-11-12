import pygame

class Background:
    def __init__(self, screee_width, screee_height):
        self.image = pygame.image.load("./flappy-bird-assets/sprites/background-day.png")
        self.image = pygame.transform.scale(self.image, (screee_width, screee_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))