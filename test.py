import pygame
import sys
import time

pygame.init()

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
    pygame.image.load("fox.png"),
    pygame.image.load("chicken.png"),
    pygame.image.load("farmer.png"),
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

# Game loop
show_instructions = False
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
                if submit_button_rect.collidepoint(event.pos):
                    collected_values = [obj["value"] for obj in objects]
                    print("Collected Values:", collected_values)
                    
                    # Delay for 2 seconds (2000 milliseconds) to show the collected values
                    pygame.time.delay(2000)

                    # Clear the screen (remove objects and submit button)
                    objects = []
                    submit_button_rect = pygame.Rect(0, 0, 0, 0)

                # Check if the close button is clicked
                if close_button_rect.collidepoint(event.pos):
                    show_instructions = False
                # Check if the help button is clicked
                elif help_button_rect.collidepoint(event.pos):
                    show_instructions = True

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

    # Increase the submit button rect size to include padding
    submit_button_rect_with_padding = submit_button_rect.inflate(submit_button_padding * 2, submit_button_padding * 2)
    
    if show_instructions:
        pygame.draw.rect(screen, GRAY, instructions_rect, border_radius=10)
        screen.blit(instructions_surface, instructions_rect.topleft)
        screen.blit(close_button, close_button_rect.topleft)
    else:
        screen.blit(help_button, help_button_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()
