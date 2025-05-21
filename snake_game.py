import pygame
import random

# Global constants (optional, but often kept global for Pygame)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self, x, y, block_size=10):
        self.block_size = block_size
        self.body = [[x, y], [x - self.block_size, y], [x - 2 * self.block_size, y]]
        self.direction = "RIGHT"
        self.color = GREEN # Use global constant
        self.should_grow = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "RIGHT":
            new_head = [head_x + self.block_size, head_y]
        elif self.direction == "LEFT":
            new_head = [head_x - self.block_size, head_y]
        elif self.direction == "UP":
            new_head = [head_x, head_y - self.block_size]
        elif self.direction == "DOWN":
            new_head = [head_x, head_y + self.block_size]

        self.body.insert(0, new_head)

        if self.should_grow:
            self.should_grow = False
        else:
            self.body.pop()

    def change_direction(self, new_direction):
        if new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        elif new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], self.block_size, self.block_size))

    def grow(self):
        self.should_grow = True

    def check_collision(self, current_screen_width, current_screen_height):
        head_x, head_y = self.body[0]
        # Wall collision
        if not (0 <= head_x < current_screen_width and 0 <= head_y < current_screen_height):
            return True
        # Self-collision
        if [head_x, head_y] in self.body[1:]:
            return True
        return False

# Food class
class Food:
    def __init__(self, current_screen_width, current_screen_height, block_size):
        self.screen_width = current_screen_width
        self.screen_height = current_screen_height
        self.block_size = block_size
        self.color = RED # Use global constant
        # Initial spawn, snake_body is not available yet
        self.x = random.randrange(0, self.screen_width // self.block_size) * self.block_size
        self.y = random.randrange(0, self.screen_height // self.block_size) * self.block_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self, snake_body):
        while True:
            self.x = random.randrange(0, self.screen_width // self.block_size) * self.block_size
            self.y = random.randrange(0, self.screen_height // self.block_size) * self.block_size
            if [self.x, self.y] not in snake_body:
                break

def main():
    pygame.init()

    # Font
    font = pygame.font.SysFont(None, 30)

    # Screen dimensions
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT

    # Colors - these could be global or local to main.
    # For simplicity here, using the global ones defined outside.
    # black = BLACK
    # white = WHITE
    # green = GREEN # Snake color is set in Snake class
    # red = RED     # Food color is set in Food class

    # Create the game screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")

    # Helper functions defined inside main to capture its scope
    def display_score(surface, current_score, current_font, color):
        score_text = current_font.render(f"Score: {current_score}", True, color)
        surface.blit(score_text, [10, 10])

    def display_game_over(surface, current_score, current_font, color, sw, sh):
        game_over_text = current_font.render(f"Game Over! Final Score: {current_score}", True, color)
        text_rect = game_over_text.get_rect(center=(sw // 2, sh // 2))
        surface.blit(game_over_text, text_rect)

    # Game objects
    snake_block_size = 10 # Define block size, can be a constant
    snake = Snake(screen_width // 2, screen_height // 2, snake_block_size)
    food = Food(screen_width, screen_height, snake_block_size)
    food.respawn(snake.body) # Ensure initial food position is not on snake

    # Score
    score = 0

    # Game clock
    clock = pygame.time.Clock()
    game_speed = 15 # Frames per second

    # Game state
    running = True
    game_over = False

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over: # Only process game input if game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")

        if not game_over:
            # Move snake
            snake.move()

            # Check for food eating
            if snake.body[0][0] == food.x and snake.body[0][1] == food.y:
                snake.grow()
                food.respawn(snake.body)
                score += 1

            # Check for collisions
            if snake.check_collision(screen_width, screen_height):
                game_over = True

        # Drawing
        screen.fill(BLACK) # Fill screen first

        if game_over:
            display_game_over(screen, score, font, WHITE, screen_width, screen_height)
        else:
            # Draw game objects
            snake.draw(screen)
            food.draw(screen)
            # Display score
            display_score(screen, score, font, WHITE)

        # Update the display
        pygame.display.flip()

        # Control game speed
        clock.tick(game_speed)

    pygame.quit()

if __name__ == '__main__':
    main()
