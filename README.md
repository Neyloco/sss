# Python Snake Game

A classic Snake game implemented in Python using the Pygame library.

## How to Play

1.  **Run the game:**
    ```bash
    python snake_game.py
    ```
2.  **Name Your Snake:**
    *   At the start, type a name for your snake (up to 10 characters) and press **Enter**. If you don't type anything, a default name will be used.
3.  **Controls:**
    *   Use the **Arrow Keys** (Up, Down, Left, Right) to control the direction of the snake.
    *   When the game is over:
        *   Press **R** to Restart the game.
        *   Press **Q** to Quit the game.
4.  **Goal:**
    *   Guide the snake to eat the red food blocks that appear on the screen.
    *   Each piece of food eaten makes the snake grow longer and increases your score.
    *   Eating 3 consecutive apples activates a temporary **Turbo Boost** for your snake!
    *   Avoid running into the walls, the snake's own body, or the blue **Enemy Snake**. The game ends if this happens.

## Requirements

*   Python 3
*   Pygame

## Installation

If you don't have Pygame installed, you can install it using pip:

```bash
pip install pygame
```

## Game Features

*   Classic snake gameplay.
*   Player-definable snake name displayed during gameplay.
*   Score tracking.
*   Turbo Boost: Eating 3 apples activates a temporary speed increase.
*   Enemy Snake: A computer-controlled snake moves randomly, adding an extra challenge.
*   Game over detection (wall collision, self-collision, and enemy collision).
*   Random food placement.
*   Restart and Quit options from the Game Over screen.
