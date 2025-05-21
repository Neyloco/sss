from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController # For basic camera control during dev
import random # Import random for food placement

# Initialize the Ursina application
app = Ursina()

# 1. Ground plane
ground = Entity(model='plane', scale=(30, 1, 30), color=color.lime.tint(-.2), texture='white_cube', texture_scale=(30,30))
# Making it a bit larger for now, will define game area later

# 2. Basic Lighting
DirectionalLight(parent=pivot, y=2, z=3, rotation=(45, -45, 45))
# AmbientLight(color=color.rgba(100, 100, 100, 0.1)) # Softer ambient light

# 3. Camera Setup (Using EditorCamera for easy navigation during early development)
# EditorCamera() 
# For a game, we might want a fixed camera later, e.g.:
camera.position = (15, 18, -22) # Adjusted: slightly lower and closer
camera.rotation_x = 45          # Angled down
camera.rotation_y = -30         # Slightly rotated view
# camera.orthographic = True # For a more classic, non-perspective view if desired later
# camera.fov = 10 # if orthographic

# Snake class
class Snake:
    def __init__(self, start_position=Vec3(0,0.5,0), length=3):
        self.segments = []  # List to hold the Ursina Entity objects
        self.head_color = color.blue
        self.body_color = color.cyan
        self.segment_size = 1  # Size of each cube segment
        self.direction = Vec3(1,0,0)  # Initial direction: positive X
        # self.length = length # No longer needed as length is dynamic
        self.positions = []  # List to store Vec3 positions of segments
        self.grow_pending = 0 # Number of segments to add

        for i in range(length):
            pos = start_position - Vec3(i * self.segment_size, 0, 0)
            self.positions.append(pos)
            segment = Entity(
                model='cube', 
                color=self.head_color if i == 0 else self.body_color, 
                position=pos, 
                scale=self.segment_size
            )
            self.segments.append(segment)

    def move(self):
        new_head_position = self.positions[0] + self.direction * self.segment_size
        self.positions.insert(0, new_head_position) # Add new head position

        if self.grow_pending > 0:
            # Add a new segment Entity at the new head's position
            new_visual_segment = Entity(model='cube', color=self.head_color, position=new_head_position, scale=self.segment_size)
            self.segments.insert(0, new_visual_segment) # Insert at the front
            self.grow_pending -= 1
        else:
            # Remove tail position from logical list
            self.positions.pop() 
            # Move the actual tail segment entity to the new head position
            tail_segment_entity = self.segments.pop() # Remove from end of list
            tail_segment_entity.position = new_head_position # Move it
            self.segments.insert(0, tail_segment_entity) # Add to front of list

        # Update colors for all segments (current head vs body)
        for i, seg_entity in enumerate(self.segments):
            seg_entity.color = self.head_color if i == 0 else self.body_color
        
        # Ensure all visual segment positions are updated (optional, but good for consistency)
        # The above logic should already handle it, but this is a safeguard.
        # for i, seg_entity in enumerate(self.segments):
        #    seg_entity.position = self.positions[i]


    def change_direction(self, new_dir_vec):
        # Prevent the snake from reversing onto itself
        if new_dir_vec != -self.direction:
            self.direction = new_dir_vec
            
    def eat_food(self):
        self.grow_pending += 1

# Instantiate Snake
player_snake = Snake()

# Food class
class Food(Entity):
    def __init__(self, game_area_scale_x, game_area_scale_z, y_position=0.5):
        self.min_x = -int(game_area_scale_x / 2)
        self.max_x = int(game_area_scale_x / 2) - 1 
        self.min_z = -int(game_area_scale_z / 2)
        self.max_z = int(game_area_scale_z / 2) - 1
        self.y_position = y_position # Store for respawn

        super().__init__(
            model='sphere', 
            color=color.red,
            scale=0.8, 
            position=self.get_random_pos(self.y_position) 
        )

    def get_random_pos(self, y_pos):
        x = random.randint(self.min_x, self.max_x)
        z = random.randint(self.min_z, self.max_z)
        return Vec3(x, y_pos, z)

    def respawn(self, occupied_positions=[]): 
        new_pos = self.get_random_pos(self.y_position)
        # Ensure food doesn't spawn on the snake
        # Convert Vec3 positions to tuples for accurate comparison in 'in' operator if needed,
        # but direct Vec3 comparison should work if occupied_positions contains Vec3.
        # For simplicity, assuming direct Vec3 comparison works or occupied_positions are comparable.
        while new_pos in occupied_positions:
            new_pos = self.get_random_pos(self.y_position)
        self.position = new_pos

# Instantiate Food
ground_scale_x = ground.scale_x
ground_scale_z = ground.scale_z
game_food = Food(game_area_scale_x=ground_scale_x, game_area_scale_z=ground_scale_z, y_position=0.5)
# Initial respawn to avoid snake starting position
# Ensure player_snake.positions is populated before calling this.
# player_snake is instantiated with positions, so this should be fine.
game_food.respawn(player_snake.positions)


# Game loop update function
snake_speed = 5  # Moves per second
move_timer = 0

# Game State and UI
game_over_state = False
score = 0
UI_FONT = "arial.ttf" # Ursina should find system fonts or use its default

score_text_display = Text(
    text=f"Score: {score}", 
    position=window.top_left + Vec2(0.05, -0.05), 
    origin=(-0.5,0.5), 
    font=UI_FONT, 
    color=color.black, 
    scale=1.5
)
game_over_text_display = Text(
    text="", 
    position=(0,0), 
    origin=(0,0), 
    scale=2, 
    font=UI_FONT, 
    color=color.red, 
    enabled=False
)

def update():
    global move_timer, game_over_state, score # Changed from nonlocal to global

    if game_over_state:
        return

    move_timer += time.dt * snake_speed # time.dt is delta time since last frame

    if move_timer >= 1:
        player_snake.move()
        move_timer = 0 # Reset timer

        head_pos = player_snake.positions[0]

        # Food Collision
        if distance(head_pos, game_food.position) < player_snake.segment_size:
            player_snake.eat_food()
            score += 1
            game_food.respawn(player_snake.positions)

        # Boundary Collision
        half_ground_x = ground.scale_x / 2 - player_snake.segment_size / 2
        half_ground_z = ground.scale_z / 2 - player_snake.segment_size / 2
        if not (-half_ground_x <= head_pos.x <= half_ground_x and \
                -half_ground_z <= head_pos.z <= half_ground_z):
            game_over_state = True
            
        # Self-Collision
        if head_pos in player_snake.positions[1:]:
            game_over_state = True

    # UI Updates
    score_text_display.text = f"Score: {score}"
    if game_over_state:
        game_over_text_display.text = "Game Over!"
        game_over_text_display.enabled = True

# Function to handle input
def input(key):
    nonlocal game_over_state # To potentially allow restart in future
    if key == 'escape':
        application.quit()
    
    if game_over_state: # No input if game is over (except escape)
        return

    # Snake movement controls (XZ plane)
    if key == 'arrow_right' or key == 'd':
        player_snake.change_direction(Vec3(1,0,0))
    elif key == 'arrow_left' or key == 'a':
        player_snake.change_direction(Vec3(-1,0,0))
    elif key == 'arrow_up' or key == 'w': # Moving "forward" on Z axis
        player_snake.change_direction(Vec3(0,0,1))
    elif key == 'arrow_down' or key == 's': # Moving "backward" on Z axis
        player_snake.change_direction(Vec3(0,0,-1))
    # Future: Add restart key 'r' here if game_over_state is True

# Start the application
app.run()
