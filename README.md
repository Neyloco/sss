# 3D Python Snake Game (Ursina Engine)

A 3D version of the classic Snake game, implemented in Python using the Ursina engine.

## How to Play

1.  **Ensure Dependencies:**
    *   Make sure you have Python 3 and the Ursina engine installed.
    *   If you don't have Ursina, install it via pip:
        ```bash
        pip install ursina
        ```

2.  **Run the game:**
    *   Execute the Python script:
        ```bash
        python ursina_snake_game.py
        ```

3.  **Controls:**
    *   Use the **Arrow Keys** or **WASD Keys** to control the direction of the snake on the 3D plane (XZ axes).
        *   **Up Arrow / W:** Move snake forward (positive Z)
        *   **Down Arrow / S:** Move snake backward (negative Z)
        *   **Left Arrow / A:** Move snake left (negative X)
        *   **Right Arrow / D:** Move snake right (positive X)
    *   Press **Escape** to quit the game.

4.  **Goal:**
    *   Guide the snake to eat the red food spheres that appear in the game area.
    *   Each piece of food eaten makes the snake grow longer and increases your score.
    *   Avoid running into the game boundaries or the snake's own body. The game ends if this happens.

## Game Features (Current - Part 1)

*   3D snake movement on a grid.
*   Random food placement in 3D space.
*   Snake growth upon eating food.
*   Score tracking and display.
*   Game over detection for boundary and self-collision.
*   Basic 3D environment with a fixed isometric-style camera.

## Future Enhancements (Potential)

*   Restart game option.
*   Advanced visual effects or textures.
*   More complex game levels or obstacles.
*   Enemy snakes or other challenges.
*   Sound effects.
```
