import pygame
import sys

from settings import *
from background import Background
from player import Player
from pipes import Pipes
from neat_model import *

# Initialize pygame and other components
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Font size 36

generation = -1
population = 0


# Function to reset the game
def reset_game():
    global pipe_list, score, passed_pipes
    pipe_list = [Pipes(SCREEN_WIDTH, SCREEN_HEIGHT)]  # Reset pipes
    score = 0  # Reset score
    passed_pipes = []  # Clear passed pipes

def eval_genoms(genomes, config):
    global generation, instances

    generation += 1

    networks = []
    players = []
    ge = []

    # Game variables
    dt = 0
    score = 0
    passed_pipes = []

    # Initialize game objects
    background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    pipe_list = [Pipes(SCREEN_WIDTH, SCREEN_HEIGHT)]  # Start with one pipe

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        players.append(Player(SCREEN_WIDTH, SCREEN_HEIGHT))
        ge.append(genome)

    # Main game loop
    while True and len(players) > 0:
        population = len(players)

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pipe_ind = 0
        if len(players) > 0:
            if len(pipe_list) > 1 and players[0].position.x > pipe_list[0].position.x + 100:  # Determine whether to use the first or second pipe on the screen for neural network input, 100 is the width of pipe
                pipe_ind = 1

        # Main loop for players
        for i, player in enumerate(players):
            ge[i].fitness += 0.01  # Reward for staying alive
            player.update(dt)

            # Send bird and pipe location
            input = (player.position.y, abs(player.position.y - (pipe_list[pipe_ind].position.y + PIPE_HEIGHT)), abs(player.position.y - (pipe_list[pipe_ind].position.y + PIPE_HEIGHT + GAP)))
            output = networks[i].activate(input)

            if output[0] > 0.5:  # Jump if the output suggests it
                player.flap()

        # # Check for user input
        # keys = pygame.key.get_pressed()
        # # Handle user input for jumping
        # if keys[pygame.K_SPACE]:
        #     player.flap()

        # Draw background
        background.draw(screen)

        # Draw every player
        for player in players:
            player.draw(screen)

        # Draw and move every pipe
        for pipe in pipe_list:
            pipe.update(dt)
            pipe.draw(screen)

        # Draw lines for debugging
        for player in players:
            pygame.draw.line(screen, (255, 0, 0), (player.position.x + 10, player.position.y + 25),
                                 (pipe_list[pipe_ind].position.x, pipe_list[pipe_ind].position.y + PIPE_HEIGHT),
                                 2)
            pygame.draw.line(screen, (255, 0, 0), (player.position.x + 10, player.position.y + 25),
                                 (pipe_list[pipe_ind].position.x, pipe_list[pipe_ind].position.y + PIPE_HEIGHT + GAP),
                                 2)

        # Check if new pipes need to be added
        if pipe_list[-1].position.x < SCREEN_WIDTH - 350:
            new_pipe = Pipes(SCREEN_WIDTH, SCREEN_HEIGHT)
            pipe_list.append(new_pipe)

        # Update score and fitness if player passes pipes
        for pipe in pipe_list:
            for i, player in enumerate(players):
                if pipe.position.x < player.position.x - 120 and pipe not in passed_pipes:
                    passed_pipes.append(pipe)
                    score += 1
                    ge[i].fitness += 5
                    passed_pipes = passed_pipes[-10:]

            # Check for collisions
            to_remove = []  # List to track players to be removed
            for i, player in enumerate(players):
                for pipe in pipe_list:
                    if pipe.check_collision(player.hit_box):
                        print("Collision detected")
                        ge[i].fitness -= 1  # Penalize the fitness for collision
                        to_remove.append(i)  # Mark player for removal

            # Remove dead players from networks, ge, and players list
            # If the last instance from generation dies from hitting the floor instead of pipe there is an bug where networks[i] is out of bounds
            for i in reversed(to_remove):
                del networks[i]
                del players[i]
                del ge[i]

        # Remove off-screen pipes
        pipe_list = [pipe for pipe in pipe_list if pipe.position.x > -pipe.image.get_width()]

        # Draw the data
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH/2, 10))
        generation_text = font.render(f"Generation: {generation}", True, (255, 255, 255))
        screen.blit(generation_text, (10, 10))
        population_text = font.render(f"Population: {population}", True, (255, 255, 255))
        screen.blit(population_text, (10, 40))

        # Update display and tick clock
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Delta time in seconds

        if len(players) == 0:
            break  # Exit the loop when all players are dead

def initialize_network(config):
    p = neat.Population(config)
    winner = p.run(eval_genoms, 50)


if __name__ == '__main__':
    initialize_network(config)
