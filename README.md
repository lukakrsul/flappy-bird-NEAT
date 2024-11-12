# Flappy Bird AI with NEAT

This project uses the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to evolve an AI that learns to play *Flappy Bird*. Over generations, the AI improves its gameplay without any predefined rules.

## Features

- **AI-Driven Gameplay**: The AI learns through evolving neural networks to achieve higher scores by avoiding pipes.
- **Modular Codebase**: Organized components for background, player, pipes, and NEAT model for easy modification.
- **Visualization**: Real-time connections show the AI's decision-making as it "sees" upcoming pipes.

## Project Structure

- **`main.py`**: Main game loop and NEAT evaluation.
- **`neat_model.py`**: NEAT configuration and population management.
- **`player.py`, `pipes.py`, `background.py`**: Core game elements.

## Installation

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/yourusername/flappy-bird-neat
   cd flappy-bird-neat
   pip install -r requirements.txt
2. Adjust settings if needed in `settings.py`
3. Run simulation

## Decision making

- **Inputs:** Bird’s y position, distance to top and bottom pipe's edge.
- **Outputs:** AI decides when to flap.
- **Fitness:** Based on survival time and pipes passed, encouraging longer survival with each generation.

## Demo

To see a demonstration of the project in action, download the video file from this repository and play it locally.

Below is a screenshot from the video to give you a quick preview:

![Demo Screenshot](https://github.com/lukakrsul/flappy-bird-NEAT/blob/main/demo-img.png?raw=true)

  


Visual assets from: https://github.com/samuelcust/flappy-bird-assets.git.
