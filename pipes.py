import pygame
import random
from settings import *


class Pipes:
    def __init__(self, screen_width, screen_height):
        # Load and scale the pipe image
        self.image = pygame.image.load("./flappy-bird-assets/sprites/pipe-green.png")
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.position = pygame.Vector2(1000, screen_height / 2)
        self.velocity = pygame.Vector2(PIPE_VELOCITY, 0)

        # Set a random position for the upper pipe within a range
        self.position.y = random.randint(-300, 0)  # Random y position for upper pipe

        self.upper_pipe_y = self.position.y
        self.lower_pipe_y = self.position.y + self.image.get_height() + GAP

        # Create rectangles for collision detection
        self.upper_pipe_rect = pygame.Rect(self.position.x, self.upper_pipe_y, PIPE_WIDTH, self.image.get_height())  # Upper pipe rectangle
        self.lower_pipe_rect = pygame.Rect(self.position.x, self.lower_pipe_y, PIPE_WIDTH, self.image.get_height())  # Lower pipe rectangle


    def update(self, dt):
        # Update pipe position
        self.position.x += self.velocity.x * dt

        # Update the pipe rectangles based on the new position
        self.upper_pipe_rect.x = self.position.x
        self.lower_pipe_rect.x = self.position.x

    def draw(self, screen):
        # Draw upper pipe (rotated 180 degrees)
        screen.blit(pygame.transform.rotate(self.image, 180), (self.position))
        screen.blit(self.image, (self.position.x, self.lower_pipe_y))

    def check_collision(self, player_rect):
        # Check if the player's rectangle collides with either of the pipes' rectangles
        if player_rect.colliderect(self.upper_pipe_rect) or player_rect.colliderect(self.lower_pipe_rect) or player_rect.bottom >= SCREEN_HEIGHT or player_rect.top < 0:
            return True
        return False

