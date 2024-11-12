import neat
import os

pwd = os.getcwd()
neat_config = os.path.join(pwd, 'neat_config.txt')

config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, neat_config)
