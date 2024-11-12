import pygame
from settings import *

class Player:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("flappy-bird-assets/sprites/bluebird-midflap.png")
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH ,BIRD_HEIGHT))
        self.position = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.last_flap_time = 0
        self.previous_position_y = screen_height / 2
        self.alive = True

        self.hit_box = pygame.Rect(self.position.x, self.position.y, BIRD_WIDTH, BIRD_HEIGHT)

    def update(self, dt):
        # Gravity and flap logic
        self.velocity.y += GRAVITY * dt
        self.position.y += self.velocity.y * dt

        # Update the hitbox position based on the player's current position
        self.hit_box.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        if self.position.y > self.previous_position_y:
            rotation = -45
        elif self.position.y < self.previous_position_y:
            rotation = 20
        else:
            rotation = 0
        self.previous_position_y = self.position.y
        screen.blit(pygame.transform.rotate(self.image, rotation), (self.position))

    def flap(self):
        current_time = pygame.time.get_ticks() / 1000
        if(current_time - self.last_flap_time > FLAP_COOLDOWN):
            self.velocity.y = FLAP_STRENGTH
            self.last_flap_time = current_time

