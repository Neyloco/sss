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
    *   **Camera (Mouse):**
        *   **Rotate View:** Right-Click + Drag Mouse.
        *   **Zoom:** Scroll Mouse Wheel.
        *   **Pan/Move Camera:** Middle-Click + Drag Mouse. (WASD keys can also pan the camera when the mouse isn't dragging for rotation/panning).
    *   **Snake Movement (Keyboard):**
        *   Use **U Key** or **Up Arrow** to move snake forward (positive Z).
        *   Use **J Key** or **Down Arrow** to move snake backward (negative Z).
        *   Use **H Key** or **Left Arrow** to move snake left (negative X).
        *   Use **K Key** or **Right Arrow** to move snake right (positive X).
    *   Press **Escape** to quit the game.
    *   When the game is over: Press **R** to Restart. 

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
*   Basic 3D environment with free-look mouse camera control (`EditorCamera`).
*   Game restart option from the Game Over screen.

## Future Enhancements (Potential)

*   Advanced visual effects or textures.
*   More complex game levels or obstacles.
*   Enemy snakes or other challenges.
*   Sound effects.
```
