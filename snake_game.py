import pygame
import random

# Global constants (optional, but often kept global for Pygame)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255) # Color for Enemy Snake

# Snake class
class Snake:
    def __init__(self, x, y, block_size=10, name="Sssnake"): # Added name parameter
        self.block_size = block_size
        self.body = [[x, y], [x - self.block_size, y], [x - 2 * self.block_size, y]]
        self.direction = "RIGHT"
        self.color = GREEN # Use global constant
        self.should_grow = False
        self.name = name

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

    def draw(self, surface, font): # Added font parameter
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], self.block_size, self.block_size))
        
        if self.body: # Ensure body is not empty
            head_x, head_y = self.body[0]
            name_surface = font.render(self.name, True, WHITE) # WHITE needs to be defined or passed
            
            # Position name centered above the head block
            text_rect = name_surface.get_rect()
            text_rect.centerx = head_x + self.block_size // 2
            text_rect.bottom = head_y - 3 # Small offset above the head
            
            surface.blit(name_surface, text_rect)

    def grow(self):
        self.should_grow = True

    def check_collision(self, current_screen_width, current_screen_height, other_snake_body=None):
        head_x, head_y = self.body[0]
        
        # Wall collision
        if not (0 <= head_x < current_screen_width and 0 <= head_y < current_screen_height):
            return True
            
        # Self-collision
        if [head_x, head_y] in self.body[1:]:
            return True
            
        # Check collision with other_snake_body
        if other_snake_body: # Ensure it's provided
            for segment in other_snake_body:
                if head_x == segment[0] and head_y == segment[1]:
                    return True # Collision with other snake
                    
        return False

    def reset(self, x, y):
        self.body = [[x, y], [x - self.block_size, y], [x - (2 * self.block_size), y]]
        self.direction = "RIGHT"
        self.should_grow = False

# Food class
class Food:
    def __init__(self, current_screen_width, current_screen_height, block_size):
        self.screen_width = current_screen_width
        self.screen_height = current_screen_height
        self.block_size = block_size
        self.color = RED # Use global constant
        self.x = 0 # Will be set by respawn
        self.y = 0 # Will be set by respawn
        # Initial spawn needs to be done carefully if snake_body is not available
        # For now, let's assume respawn is called after player snake is initialized.

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self, snake_body):
        while True:
            self.x = random.randrange(0, self.screen_width // self.block_size) * self.block_size
            self.y = random.randrange(0, self.screen_height // self.block_size) * self.block_size
            # Ensure food does not spawn on any part of the snake
            if not any(segment[0] == self.x and segment[1] == self.y for segment in snake_body):
                break

# EnemySnake class
class EnemySnake:
    def __init__(self, x, y, screen_width, screen_height, block_size, color):
        self.block_size = block_size
        self.body = [[x, y], [x + self.block_size, y], [x + 2 * self.block_size, y]] # Initial body, ensure it's on screen
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_opposite_direction(self, direction):
        if direction == "UP": return "DOWN"
        if direction == "DOWN": return "UP"
        if direction == "LEFT": return "RIGHT"
        if direction == "RIGHT": return "LEFT"
        return ""

    def move(self):
        head_x, head_y = self.body[0]
        
        # Attempt to move in current direction
        potential_new_head_x, potential_new_head_y = head_x, head_y
        if self.direction == "RIGHT": potential_new_head_x += self.block_size
        elif self.direction == "LEFT": potential_new_head_x -= self.block_size
        elif self.direction == "UP": potential_new_head_y -= self.block_size
        elif self.direction == "DOWN": potential_new_head_y += self.block_size

        # Wall Avoidance
        collided_with_wall = False
        if not (0 <= potential_new_head_x < self.screen_width and \
                  0 <= potential_new_head_y < self.screen_height):
            collided_with_wall = True
            
            possible_directions = ["UP", "DOWN", "LEFT", "RIGHT"]
            # Remove opposite of current direction to prevent immediate reversal
            opposite_direction = self.get_opposite_direction(self.direction)
            if opposite_direction in possible_directions:
                possible_directions.remove(opposite_direction)
            
            # Try to find a direction that doesn't immediately lead to another wall collision
            # This is a simplified approach; more complex logic might be needed for corners
            valid_new_direction_found = False
            original_direction = self.direction # Store original direction for next step
            
            for _ in range(len(possible_directions)): # Try available directions
                new_direction_candidate = random.choice(possible_directions)
                possible_directions.remove(new_direction_candidate) # Avoid re-picking immediately

                temp_head_x, temp_head_y = head_x, head_y
                if new_direction_candidate == "RIGHT": temp_head_x += self.block_size
                elif new_direction_candidate == "LEFT": temp_head_x -= self.block_size
                elif new_direction_candidate == "UP": temp_head_y -= self.block_size
                elif new_direction_candidate == "DOWN": temp_head_y += self.block_size

                if (0 <= temp_head_x < self.screen_width and \
                    0 <= temp_head_y < self.screen_height):
                    self.direction = new_direction_candidate
                    potential_new_head_x, potential_new_head_y = temp_head_x, temp_head_y
                    valid_new_direction_found = True
                    break
            
            if not valid_new_direction_found: # If all choices lead to wall (e.g. stuck in a very small space)
                                             # Or if only opposite was left, just pick any non-opposite
                possible_directions = ["UP", "DOWN", "LEFT", "RIGHT"]
                if opposite_direction in possible_directions:
                    possible_directions.remove(opposite_direction)
                if original_direction in possible_directions: # Also remove the one that just caused collision
                     possible_directions.remove(original_direction)
                if possible_directions:
                    self.direction = random.choice(possible_directions)
                # If somehow possible_directions is empty (shouldn't happen with 2+ choices), it will keep old direction and likely stay stuck for a frame.

        new_head = [potential_new_head_x, potential_new_head_y]
        # Re-calculate new_head based on the (potentially new) direction if wall collision occurred
        if collided_with_wall : # This ensures the head is updated if direction changed due to wall
            head_x, head_y = self.body[0] # Get current head again
            if self.direction == "RIGHT": new_head = [head_x + self.block_size, head_y]
            elif self.direction == "LEFT": new_head = [head_x - self.block_size, head_y]
            elif self.direction == "UP": new_head = [head_x, head_y - self.block_size]
            elif self.direction == "DOWN": new_head = [head_x, head_y + self.block_size]


        self.body.insert(0, new_head)
        self.body.pop()

        # Random Direction Change (occasional)
        if random.random() < 0.03: # Changed from 0.05 to 0.03 for less frequent random turns
            opposite = self.get_opposite_direction(self.direction)
            choices = [d for d in ["UP", "DOWN", "LEFT", "RIGHT"] if d != opposite]
            if choices: # Ensure there are choices left
                self.direction = random.choice(choices)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], self.block_size, self.block_size))

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

    # Game states
    game_state = "NAME_INPUT" # "NAME_INPUT", "PLAYING", "GAME_OVER"
    snake_name = ""

    # Game objects - initialized to None, will be created by reset_game_state
    snake_block_size = 10 # Define block size, can be a constant
    start_snake_x = screen_width // 2
    start_snake_y = screen_height // 2
    snake = None
    food = None
    enemy_snake = None # Initialize enemy_snake
    
    # Score and game_over flag
    score = 0
    game_over = False # This will be managed by game_state now primarily

    # Turbo mode variables
    apples_eaten_since_turbo = 0
    turbo_active = False
    turbo_timer_start = 0
    turbo_duration = 4000  # 4 seconds
    normal_game_speed = 15
    turbo_game_speed = 30
    game_speed = normal_game_speed # Initial game speed, might be adjusted before loop if needed

    # Helper functions defined inside main to capture its scope
    def display_score(surface, current_score, current_font, color):
        score_text = current_font.render(f"Score: {current_score}", True, color)
        surface.blit(score_text, [10, 10])

    def display_game_over(surface, current_score, current_font, color, sw, sh):
        game_over_text = current_font.render(f"Game Over! Final Score: {current_score}", True, color)
        text_rect = game_over_text.get_rect(center=(sw // 2, sh // 2))
        surface.blit(game_over_text, text_rect)

        restart_quit_text = current_font.render("Press 'R' to Restart or 'Q' to Quit", True, color)
        restart_quit_rect = restart_quit_text.get_rect(center=(sw // 2, text_rect.centery + 40)) # Corrected center_y to centery
        surface.blit(restart_quit_text, restart_quit_rect)

    def reset_game_state():
        nonlocal score, game_over, apples_eaten_since_turbo, turbo_active, game_speed
        nonlocal snake, food, enemy_snake # Allow creation/modification of these objects
        
        current_snake_name = snake_name # snake_name is from main's scope (user input)
        if snake is None: # Create instances if they don't exist
            snake = Snake(start_snake_x, start_snake_y, snake_block_size, name=current_snake_name)
        else:
            snake.reset(start_snake_x, start_snake_y) 
            
        if food is None:
            food = Food(screen_width, screen_height, snake_block_size)
        
        food.respawn(snake.body) # Call after snake is reset/created

        enemy_start_x = screen_width // 4
        enemy_start_y = screen_height // 2
        if enemy_snake is None:
            enemy_snake = EnemySnake(enemy_start_x, enemy_start_y, screen_width, screen_height, snake_block_size, BLUE)
        else:
            # For now, let's re-initialize it; later we might add a proper reset method to EnemySnake
            enemy_snake = EnemySnake(enemy_start_x, enemy_start_y, screen_width, screen_height, snake_block_size, BLUE)

        score = 0
        # game_over = False # game_state handles this
        apples_eaten_since_turbo = 0
        turbo_active = False
        game_speed = normal_game_speed

    # Game clock
    clock = pygame.time.Clock()
    running = True

    # Game loop
    while running:
        if game_state == "NAME_INPUT":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not snake_name:
                            snake_name = "Sssammy"
                        game_state = "PLAYING"
                        reset_game_state() # Initialize game for first play
                    elif event.key == pygame.K_BACKSPACE:
                        snake_name = snake_name[:-1]
                    else:
                        if len(snake_name) < 10:
                            snake_name += event.unicode
            
            screen.fill(BLACK)
            instruction_text = font.render("Enter Snake Name (max 10 chars, press Enter to start):", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
            screen.blit(instruction_text, instruction_rect)
            
            name_text_surface = font.render(snake_name, True, WHITE)
            name_text_rect = name_text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(name_text_surface, name_text_rect)
            pygame.display.flip()

        elif game_state == "PLAYING":
            # Manage Turbo Timer
            if turbo_active:
                current_time = pygame.time.get_ticks()
                if current_time - turbo_timer_start > turbo_duration:
                    turbo_active = False
                    game_speed = normal_game_speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # No game_over check here as game_state == "PLAYING" implies not game_over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")
            
            # Move snake
            snake.move()
            if enemy_snake: enemy_snake.move() # Move enemy snake

            # Check for food eating
            if snake.body[0][0] == food.x and snake.body[0][1] == food.y:
                snake.grow()
                food.respawn(snake.body)
                score += 1
                if not turbo_active: # Only count apples if turbo is not already active
                    apples_eaten_since_turbo += 1
                
                if apples_eaten_since_turbo >= 3 and not turbo_active:
                    turbo_active = True
                    apples_eaten_since_turbo = 0
                    turbo_timer_start = pygame.time.get_ticks()
                    game_speed = turbo_game_speed

            # Check for collisions
            if enemy_snake and snake.check_collision(screen_width, screen_height, enemy_snake.body):
                game_state = "GAME_OVER" # Change state
            elif not enemy_snake and snake.check_collision(screen_width, screen_height): # Fallback if enemy_snake is None for some reason
                game_state = "GAME_OVER"


            # Drawing for PLAYING state
            screen.fill(BLACK)
            snake.draw(screen, font) # Pass font to snake.draw
            if enemy_snake: enemy_snake.draw(screen) # Draw enemy snake
            food.draw(screen)
            display_score(screen, score, font, WHITE)
            if turbo_active:
                turbo_text = font.render("TURBO!", True, WHITE)
                screen.blit(turbo_text, [screen_width - 100, 10])
            pygame.display.flip()

        elif game_state == "GAME_OVER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "PLAYING"
                        reset_game_state()
                    elif event.key == pygame.K_q:
                        running = False # No nonlocal needed as running is in main scope
            
            # Drawing for GAME_OVER state
            screen.fill(BLACK)
            display_game_over(screen, score, font, WHITE, screen_width, screen_height)
            pygame.display.flip()
        
        clock.tick(game_speed)

    pygame.quit()

if __name__ == '__main__':
    main()
