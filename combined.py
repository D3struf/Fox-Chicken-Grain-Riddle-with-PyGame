import pygame
import sys
from collections import deque
    
pygame.init()

class State:
    def __init__(self, farmer, fox, chicken, grain):
        self.farmer = farmer
        self.fox = fox
        self.chicken = chicken
        self.grain = grain
    
    def is_valid(self):
        return (
            self.is_valid_move(self.fox, self.chicken) and
            self.is_valid_move(self.chicken, self.grain)
        )

    def is_valid_move(self, item1, item2):
        # Check if item1 would eat item2 when left alone
        return not (item1 == item2 and self.farmer != item1)
    
    # Returns the moves or the states
    def possible_moves(self):
        moves = []
        for item in ["farmer", "fox", "chicken", "grain"]:
            if getattr(self, item) == self.farmer:
                new_state = State(
                    1 - self.farmer,
                    self.fox if item != "fox" else 1 - self.fox,
                    self.chicken if item != "chicken" else 1 - self.chicken,
                    self.grain if item != "grain" else 1 - self.grain
                )
                if new_state.is_valid():
                    moves.append(new_state)
        return moves
    
    # Checks to see if all of items are on the other side of the river
    def is_goal_state(self):
        return (
            self.farmer == 1 and
            self.fox == 1 and
            self.chicken == 1 and
            self.grain == 1
        )

    def __str__(self):
        return f"| Farmer: {self.farmer} | Fox: {self.fox} | Chicken: {self.chicken} | Grain: {self.grain} | \n|-----------|--------|------------|----------|"

def breadth_first_search(initial_state):
    if not initial_state.is_valid():
        print("Invalid initial state!")
        return None
    
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        state, path = queue.popleft()
        if state.is_goal_state():
            return path + [state]
        if state not in visited:
            visited.add(state)
            for next_state in state.possible_moves():
                queue.append((next_state, path + [state]))

    return None

def print_solution(solution):
    if solution:
        no_valid_states = len(solution)
        print("Number of Valid States:", no_valid_states)
        print("Solution found!")
        print("|-----------|--------|------------|----------|")
        for i, state in enumerate(solution):
            print(f"{state}")
    else:
        print("No solution found.")

# Function to animate the transition of items
def animate_transition(screen, objects, object_images, transition_path):
    final_state = None  # Initialize final_state

    for state in transition_path:
        pygame.time.delay(1000)  # Delay for 1 second between transitions

        # Clear the screen
        screen.fill(WHITE)
        screen.blit(background_image, background_rect)

        # Draw objects at their current positions
        for obj, image, value in zip(objects, object_images, [state.farmer, state.fox, state.chicken, state.grain]):
            pygame.draw.rect(screen, LIGHTGRAY, obj["rect"])
            screen.blit(image, obj["rect"].topleft)

        # Display "Solving..." text at the bottom
        font = pygame.font.Font(None, 36)
        solving_text = font.render("Solving...", True, BLACK)
        solving_rect = solving_text.get_rect(center=(width // 2, height - 30))
        screen.blit(solving_text, solving_rect.topleft)

        pygame.display.flip()

        # Delay before starting the animation
        pygame.time.delay(500)

        # Determine which objects have changed
        changed_objects = [obj for obj, value in zip(objects, [state.farmer, state.fox, state.chicken, state.grain]) if obj["value"] != value]

        # Check if the farmer's value has changed
        farmer_changed = any(obj["value"] != value for obj, value in zip(objects, [state.farmer, state.fox, state.chicken, state.grain]))

        # Animate changed objects simultaneously
        if farmer_changed:
            animate_objects_simultaneously(screen, objects, state)
        elif len(changed_objects) == 2:
            animate_objects_simultaneously(screen, changed_objects, state)
        else:
            # Animate each object individually with different target positions
            for obj, image, value, target_top in zip(objects, object_images, [state.farmer, state.fox, state.chicken, state.grain], [50, 150, 250, 350]):
                target_pos = (100, target_top) if value == 1 else (600, target_top)  # Target position based on the state
                animate_object(screen, obj, image, target_pos, state)

        pygame.display.flip()

        # Update final_state after each transition
        final_state = state

    # Draw the objects in their final positions
    final_positions = [
        get_object_position(value, obj["rect"].height)
        for obj, value in zip(objects, [final_state.farmer, final_state.fox, final_state.chicken, final_state.grain])
    ]

    # Create new Rect objects for the final positions
    final_rects = [pygame.Rect(pos[0], pos[1], obj["rect"].width, obj["rect"].height) for obj, pos in zip(objects, final_positions)]

    for obj, image, final_rect in zip(objects, object_images, final_rects):
        pygame.draw.rect(screen, LIGHTGRAY, final_rect)
        screen.blit(image, final_rect.topleft)

    # Draw the "Solved" text
    font = pygame.font.Font(None, 72)
    solved_text = font.render("Solved!", True, (0, 255, 0))
    solved_rect = solved_text.get_rect(center=(width // 2, height - 30))
    screen.blit(solved_text, solved_rect.topleft)

    pygame.display.flip()

def get_object_position(value, obj_height):
    if value == 0:
        return 100, (height - obj_height) // 2
    else:
        return 600, (height - obj_height) // 2


def animate_object(screen, obj, image, target_pos, state):
    # Animate an individual object from its current position to the target position
    start_pos = obj["rect"].topleft
    total_frames = 30  # Adjust the number of frames for smoother animation
    for frame in range(1, total_frames + 1):
        # Interpolate between start and target positions
        current_pos = (
            start_pos[0] + (target_pos[0] - start_pos[0]) * (frame / total_frames),
            start_pos[1] + (target_pos[1] - start_pos[1]) * (frame / total_frames)
        )

        # Clear the screen
        screen.fill(WHITE)
        screen.blit(background_image, background_rect)

        # Draw other objects at their current positions
        for other_obj, other_image, other_value in zip(objects, object_images, [state.farmer, state.fox, state.chicken, state.grain]):
            if other_obj != obj:
                pygame.draw.rect(screen, LIGHTGRAY, other_obj["rect"])
                screen.blit(other_image, other_obj["rect"].topleft)
                font = pygame.font.Font(None, 36)
                text_surface = font.render(str(other_value), True, BLACK)
                screen.blit(text_surface, (other_obj["rect"].centerx - text_surface.get_width() // 2, other_obj["rect"].centery - text_surface.get_height() // 2))

        # Draw the animated object at the current position
        pygame.draw.rect(screen, LIGHTGRAY, obj["rect"])
        obj["rect"].topleft = current_pos
        screen.blit(image, obj["rect"].topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(obj["value"]), True, BLACK)
        screen.blit(text_surface, (obj["rect"].centerx - text_surface.get_width() // 2, obj["rect"].centery - text_surface.get_height() // 2))

        # Display "Solving..." text at the bottom
        font = pygame.font.Font(None, 36)
        solving_text = font.render("Solving...", True, BLACK)
        solving_rect = solving_text.get_rect(center=(width // 2, height - 30))
        screen.blit(solving_text, solving_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(10)  # Adjust the delay for smoother animation

def animate_objects_simultaneously(screen, objects, state):
    pygame.time.delay(500)  # Delay before starting the simultaneous animation

    start_positions = [(obj["rect"].left, obj["rect"].top) for obj in objects]
    target_positions = [
        (100, 50) if state.farmer == 0 else (600, 50),  # Target position for Farmer
        (100, 150) if state.fox == 0 else (600, 150),      # Target position for Fox
        (100, 250) if state.chicken == 0 else (600, 250),  # Target position for Chicken
        (100, 350) if state.grain == 0 else (600, 350)     # Target position for Grain
    ]

    for i in range(30):  # Number of frames for the simultaneous animation
        screen.fill(WHITE)
        screen.blit(background_image, background_rect)

        for obj, image, start_pos, target_pos in zip(objects, object_images, start_positions, target_positions):
            current_pos = (
                int(start_pos[0] + (target_pos[0] - start_pos[0]) * i / 30),
                int(start_pos[1] + (target_pos[1] - start_pos[1]) * i / 30)
            )
            obj["rect"].topleft = current_pos
            pygame.draw.rect(screen, LIGHTGRAY, obj["rect"])
            screen.blit(image, obj["rect"].topleft)

        # Display "Solving..." text at the bottom
        font = pygame.font.Font(None, 36)
        solving_text = font.render("Solving...", True, BLACK)
        solving_rect = solving_text.get_rect(center=(width // 2, height - 30))
        screen.blit(solving_text, solving_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(30)  # Delay between frames for smooth animation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
GRAY = (52, 73, 85)
LIGHTGRAY = (169, 169, 169)
SECONDARY = (249, 170, 51)
BLUE = (0, 112, 242)

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fox Chicken Grain Problem Agent")

# Load original background image
original_background_image = pygame.image.load("background.jpg")
close_button_image = pygame.image.load("close-button.png")
help_button_image = pygame.image.load("help-button.png")

# Resize the background image
background_width, background_height = 800, 600
background_image = pygame.transform.scale(original_background_image, (background_width, background_height))
background_rect = background_image.get_rect()

# Load object images
object_images = [
    pygame.image.load("farmer.png"),
    pygame.image.load("fox.png"),
    pygame.image.load("chicken.png"),
    pygame.image.load("grain.png")
]

# Objects setup
objects = [
    {"rect": pygame.Rect(150, 250, 100, 100), "value": 0},
    {"rect": pygame.Rect(300, 250, 100, 100), "value": 0},
    {"rect": pygame.Rect(450, 250, 100, 100), "value": 0},
    {"rect": pygame.Rect(600, 250, 100, 100), "value": 0}
]

# Resize object images to match the rectangle dimensions
object_images = [pygame.transform.scale(img, (100, 100)) for img in object_images]

# Overlay text
font = pygame.font.Font(None, 24)
instructions_text = [
    "1. Choose the starting point for the items",
    "2. Complete the game by pressing",
    "    the Submit Button.",
    "3. Have fun and let the AI do the job!"
]
instructions_surface = pygame.Surface((400, 250), pygame.SRCALPHA)
instructions_surface.fill(TRANSPARENT)
text_surface = font.render("Instructions: ", True, SECONDARY)
text_surface2 = font.render("0 - for left land   |   1 - for right land", True, SECONDARY)
instructions_surface.blit(text_surface, (20, 30))
instructions_surface.blit(text_surface2, (60, 60))

for i, line in enumerate(instructions_text):
    text_surface = font.render(line, True, WHITE)
    instructions_surface.blit(text_surface, (40, 90 + i * 30))

# Center the modal on the screen
instructions_rect = instructions_surface.get_rect(center=(width // 2, height // 2))

# Close button
button_width, button_height = 24, 24
close_button = pygame.transform.scale(close_button_image, (button_width, button_height))
close_button_rect = close_button.get_rect()
close_button_rect.topleft = (instructions_rect.right - button_width - 5, instructions_rect.top + 5)

# Help button
help_button_width, help_button_height = 46, 46
help_button = pygame.transform.scale(help_button_image, (help_button_width, help_button_height))
help_button_rect = help_button.get_rect()
help_button_rect.topleft = (740, 10)

# Submit button setup
submit_button_rect = pygame.Rect(350, 400, 100, 50)
submit_button_padding = 20

# Play Again button setup
play_again_button_rect = pygame.Rect(350, 500, 100, 50)
play_again_button_padding = 20

# Game loop
show_instructions = False
puzzle_solved = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for obj in objects:
                    if obj["rect"].collidepoint(event.pos):
                        # Toggle between 0 and 1
                        obj["value"] = 1 if obj["value"] == 0 else 0
                # Check if the submit button is clicked
                if submit_button_rect_with_padding.collidepoint(event.pos):
                    collected_values = [obj["value"] for obj in objects]
                    print("Collected Values:", collected_values)

                    # Find the solution using BFS
                    initial_state = State(*collected_values)
                    solution = breadth_first_search(initial_state)

                    if solution:
                        # Animate the transition based on the solution
                        animate_transition(screen, objects, object_images, solution)

                    # Clear the screen (remove objects and submit button)
                    objects = []
                    submit_button_rect = pygame.Rect(0, 0, 0, 0)

                # Check if the close button is clicked
                if close_button_rect.collidepoint(event.pos):
                    show_instructions = False
                # Check if the help button is clicked
                elif help_button_rect.collidepoint(event.pos):
                    show_instructions = True
                # Check if the play again button is clicked
                if puzzle_solved and play_again_button_rect_with_padding.collidepoint(event.pos):
                    # Reset the game state
                    objects = [
                        {"rect": pygame.Rect(150, 250, 100, 100), "value": 0},
                        {"rect": pygame.Rect(300, 250, 100, 100), "value": 0},
                        {"rect": pygame.Rect(450, 250, 100, 100), "value": 0},
                        {"rect": pygame.Rect(600, 250, 100, 100), "value": 0}
                    ]
                    puzzle_solved = False  # Reset the puzzle_solved flag

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, background_rect)

    # Draw objects
    for obj, image in zip(objects, object_images):
        pygame.draw.rect(screen, LIGHTGRAY, obj["rect"])
        screen.blit(image, obj["rect"].topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(obj["value"]), True, BLACK)
        screen.blit(text_surface, (obj["rect"].centerx - text_surface.get_width() // 2, obj["rect"].centery - text_surface.get_height() // 2))

    # Draw submit button with padding
    pygame.draw.rect(screen, BLUE, submit_button_rect, border_radius=10)
    font = pygame.font.Font(None, 32)
    text_surface = font.render("Submit", True, WHITE)
    text_rect = text_surface.get_rect(center=submit_button_rect.center)
    screen.blit(text_surface, text_rect)

    # Draw play again button with padding if the puzzle is solved
    if puzzle_solved:
        pygame.draw.rect(screen, BLUE, play_again_button_rect, border_radius=10)
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Play Again", True, WHITE)
        text_rect = text_surface.get_rect(center=play_again_button_rect.center)
        screen.blit(text_surface, text_rect)

    # Increase the button rects size to include padding
    submit_button_rect_with_padding = submit_button_rect.inflate(submit_button_padding * 2, submit_button_padding * 2)
    play_again_button_rect_with_padding = play_again_button_rect.inflate(play_again_button_padding * 2, play_again_button_padding * 2)

    if show_instructions:
        pygame.draw.rect(screen, GRAY, instructions_rect, border_radius=10)
        screen.blit(instructions_surface, instructions_rect.topleft)
        screen.blit(close_button, close_button_rect.topleft)
    else:
        screen.blit(help_button, help_button_rect.topleft)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
