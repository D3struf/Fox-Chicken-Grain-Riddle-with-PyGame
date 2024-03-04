import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
GRAY = (52, 73, 85)
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
fox_overlay_image = pygame.image.load("fox.png")
chicken_overlay_image = pygame.image.load("chicken.png")
farmer_overlay_image = pygame.image.load("farmer.png")
grain_overlay_image = pygame.image.load("grain.png")

# Resize the background image
background_width, background_height = 800, 600
background_image = pygame.transform.scale(original_background_image, (background_width, background_height))
background_rect = background_image.get_rect()

# Overlay text
font = pygame.font.Font(None, 24)  # Use the default font with size 36
instructions_text = [
    "1. Drag and drop items into the Rectangles.",
    "2. Complete the game by placing all",
    "     items in the arrays.",
    "3. Have fun and let the AI do the job!"
]
instructions_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
instructions_surface.fill(TRANSPARENT)
text_surface = font.render("Instructions: ", True, SECONDARY)
instructions_surface.blit(text_surface, (20, 30))

for i, line in enumerate(instructions_text):
    text_surface = font.render(line, True, WHITE)
    instructions_surface.blit(text_surface, (40, 60 + i * 30))

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

# Resize the overlay image
overlay_width, overlay_height = 100, 100
fox_image = pygame.transform.scale(fox_overlay_image, (overlay_width, overlay_height))
fox_rect = fox_image.get_rect()
fox_rect.topleft = (100, 100)

chicken_image = pygame.transform.scale(chicken_overlay_image, (overlay_width, overlay_height))
chicken_rect = chicken_image.get_rect()
chicken_rect.topleft = (100, 100)

farmer_image = pygame.transform.scale(farmer_overlay_image, (overlay_width, overlay_height))
farmer_rect = farmer_image.get_rect()
farmer_rect.topleft = (100, 100)

grain_image = pygame.transform.scale(grain_overlay_image, (overlay_width, overlay_height))
grain_rect = grain_image.get_rect()
grain_rect.topleft = (100, 100)

# Arrays for dropped items
array1_rect = pygame.Rect(0, 50, 400, 550)
array2_rect = pygame.Rect(400, 50, 400, 550)

# Set transparency for arrays
array1_surface = pygame.Surface((array1_rect.width, array1_rect.height), pygame.SRCALPHA)
array2_surface = pygame.Surface((array2_rect.width, array2_rect.height), pygame.SRCALPHA)
array1_surface.fill(TRANSPARENT)
array2_surface.fill(TRANSPARENT)

# Submit button
submit_button_width, submit_button_height = 100, 40
submit_button_rect = pygame.Rect(650, 500, submit_button_width, submit_button_height)

# Arrays for submitted items
submitted_rect = pygame.Rect(650, 400, 100, 100)
submitted_surface = pygame.Surface((submitted_rect.width, submitted_rect.height), pygame.SRCALPHA)
submitted_surface.fill(BLUE)

array1_items = [None, None, None, None]
array2_items = [None, None, None, None]
submitted_items = []

# Variables for drag and drop
dragging_fox = False
offset_fox = (0, 0)
dragging_chicken = False
offset_chicken = (0, 0)
dragging_farmer = False
offset_farmer = (0, 0)
dragging_grain = False
offset_grain = (0, 0)
dropped_in_array1 = False
dropped_in_array2 = False

# Game loop
show_instructions = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fox_rect.collidepoint(event.pos):
                dragging_fox = True
                offset_fox = (event.pos[0] - fox_rect.left, event.pos[1] - fox_rect.top)
            elif chicken_rect.collidepoint(event.pos):
                dragging_chicken = True
                offset_chicken = (event.pos[0] - chicken_rect.left, event.pos[1] - chicken_rect.top)
            elif farmer_rect.collidepoint(event.pos):
                dragging_farmer = True
                offset_farmer = (event.pos[0] - farmer_rect.left, event.pos[1] - farmer_rect.top)
            elif grain_rect.collidepoint(event.pos):
                dragging_grain = True
                offset_grain = (event.pos[0] - grain_rect.left, event.pos[1] - grain_rect.top)
            # elif submit_button_rect.collidepoint(event.pos):
            #     # Check if the submit button is clicked
            #     if dropped_in_array1:
            #         array1_items = [
            #             "Fox" if dragging_fox else array1_items[0],
            #             "Chicken" if dragging_chicken else array1_items[1],
            #             "Farmer" if dragging_farmer else array1_items[2],
            #             "Grain" if dragging_grain else array1_items[3]
            #         ]
            #         print("Array 1 Items:", array1_items)
            #     elif dropped_in_array2:
            #         array2_items = [
            #             "Fox" if dragging_fox else array2_items[0],
            #             "Chicken" if dragging_chicken else array2_items[1],
            #             "Farmer" if dragging_farmer else array2_items[2],
            #             "Grain" if dragging_grain else array2_items[3]
            #         ]
            #         print("Array 2 Items:", array2_items)

            #     # Clear dragging variables after submission
            #     dragging_fox = False
            #     dragging_chicken = False
            #     dragging_farmer = False
            #     dragging_grain = False
            if event.button == 1:
                # Check if the close button is clicked
                if close_button_rect.collidepoint(event.pos):
                    show_instructions = False
                # Check if the help button is clicked
                elif help_button_rect.collidepoint(event.pos):
                    show_instructions = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if the item was dropped in Array 1
            if array1_rect.collidepoint(event.pos) and (dragging_fox or dragging_chicken or dragging_farmer or dragging_grain):
                print("Item dropped in Array 1")
                array1_items = [
                    "Fox" if dragging_fox and dropped_in_array1 else array1_items[0],
                    "Chicken" if dragging_chicken and dropped_in_array1 else array1_items[1],
                    "Farmer" if dragging_farmer and dropped_in_array1 else array1_items[2],
                    "Grain" if dragging_grain and dropped_in_array1 else array1_items[3]
                ]
                print("Array 1 Items:", array1_items)
                dropped_in_array1 = False
                dropped_in_array2 = False
            # Check if the item was dropped in Array 2
            elif array2_rect.collidepoint(event.pos) and (dragging_fox or dragging_chicken or dragging_farmer or dragging_grain):
                print("Item dropped in Array 2")
                array2_items = [
                    "Fox" if dragging_fox and dropped_in_array2 else array2_items[0],
                    "Chicken" if dragging_chicken and dropped_in_array2 else array2_items[1],
                    "Farmer" if dragging_farmer and dropped_in_array2 else array2_items[2],
                    "Grain" if dragging_grain and dropped_in_array2 else array2_items[3]
                ]
                print("Array 2 Items:", array2_items)
                dropped_in_array1 = False
                dropped_in_array2 = False
            dragging_fox = False
            dragging_chicken = False
            dragging_farmer = False
            dragging_grain = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_fox:
                fox_rect.topleft = (event.pos[0] - offset_fox[0], event.pos[1] - offset_fox[1])
                # Check if the item is over Array 1
                if array1_rect.collidepoint(event.pos):
                    dropped_in_array1 = True
                    dropped_in_array2 = False
                # Check if the item is over Array 2
                elif array2_rect.collidepoint(event.pos):
                    dropped_in_array1 = False
                    dropped_in_array2 = True
                else:
                    dropped_in_array1 = False
                    dropped_in_array2 = False
            elif dragging_chicken:
                chicken_rect.topleft = (event.pos[0] - offset_chicken[0], event.pos[1] - offset_chicken[1])
                # Check if the item is over Array 1
                if array1_rect.collidepoint(event.pos):
                    dropped_in_array1 = True
                    dropped_in_array2 = False
                # Check if the item is over Array 2
                elif array2_rect.collidepoint(event.pos):
                    dropped_in_array1 = False
                    dropped_in_array2 = True
                else:
                    dropped_in_array1 = False
                    dropped_in_array2 = False
            elif dragging_farmer:
                farmer_rect.topleft = (event.pos[0] - offset_farmer[0], event.pos[1] - offset_farmer[1])
                # Check if the item is over Array 1
                if array1_rect.collidepoint(event.pos):
                    dropped_in_array1 = True
                    dropped_in_array2 = False
                # Check if the item is over Array 2
                elif array2_rect.collidepoint(event.pos):
                    dropped_in_array1 = False
                    dropped_in_array2 = True
                else:
                    dropped_in_array1 = False
                    dropped_in_array2 = False
            elif dragging_grain:
                grain_rect.topleft = (event.pos[0] - offset_grain[0], event.pos[1] - offset_grain[1])
                # Check if the item is over Array 1
                if array1_rect.collidepoint(event.pos):
                    dropped_in_array1 = True
                    dropped_in_array2 = False
                # Check if the item is over Array 2
                elif array2_rect.collidepoint(event.pos):
                    dropped_in_array1 = False
                    dropped_in_array2 = True
                else:
                    dropped_in_array1 = False
                    dropped_in_array2 = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                show_instructions = not show_instructions

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, background_rect)
    screen.blit(array1_surface, array1_rect)
    screen.blit(array2_surface, array2_rect)
    screen.blit(fox_image, fox_rect)
    screen.blit(chicken_image, chicken_rect)
    screen.blit(farmer_image, farmer_rect)
    screen.blit(grain_image, grain_rect)
    screen.blit(submitted_surface, submitted_rect)
    
    # Draw submit button
    pygame.draw.rect(screen, GRAY, submit_button_rect, border_radius=5)
    text_surface = font.render("Submit", True, WHITE)
    screen.blit(text_surface, (submit_button_rect.centerx - text_surface.get_width() // 2, submit_button_rect.centery - text_surface.get_height() // 2))
    
    if show_instructions:
        pygame.draw.rect(screen, GRAY, instructions_rect, border_radius=10)  # Draw modal background
        screen.blit(instructions_surface, instructions_rect.topleft)
        screen.blit(close_button, close_button_rect.topleft)  # Draw close button
    else:
        screen.blit(help_button, help_button_rect.topleft)  # Draw help button 
    
    pygame.display.flip()

pygame.quit()
sys.exit()
