import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drag Items into Arrays")

# Load original background image
original_background_image = pygame.image.load("background.jpg")

# Resize the background image
background_width, background_height = 800, 600
background_image = pygame.transform.scale(original_background_image, (background_width, background_height))
background_rect = background_image.get_rect()

# Load original overlay image
original_overlay_image = pygame.image.load("fox.png")

# Resize the overlay image
overlay_width, overlay_height = 100, 100
overlay_image = pygame.transform.scale(original_overlay_image, (overlay_width, overlay_height))
overlay_rect = overlay_image.get_rect()
overlay_rect.topleft = (100, 100)  # Initial position of the overlay image

# Arrays for dropped items
array1_rect = pygame.Rect(100, 400, 200, 100)
array2_rect = pygame.Rect(500, 400, 200, 100)

# Set transparency for arrays
array1_surface = pygame.Surface((array1_rect.width, array1_rect.height), pygame.SRCALPHA)
array2_surface = pygame.Surface((array2_rect.width, array2_rect.height), pygame.SRCALPHA)
array1_surface.fill(TRANSPARENT)
array2_surface.fill(TRANSPARENT)

# Variables for drag and drop
dragging = False
offset = (0, 0)
dropped_in_array1 = False
dropped_in_array2 = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if overlay_rect.collidepoint(event.pos):
                dragging = True
                offset = (event.pos[0] - overlay_rect.left, event.pos[1] - overlay_rect.top)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            # Check if the item was dropped in Array 1
            if array1_rect.collidepoint(event.pos) and dropped_in_array1:
                print("Item dropped in Array 1")
                dropped_in_array1 = False
            # Check if the item was dropped in Array 2
            elif array2_rect.collidepoint(event.pos) and dropped_in_array2:
                print("Item dropped in Array 2")
                dropped_in_array2 = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            overlay_rect.topleft = (event.pos[0] - offset[0], event.pos[1] - offset[1])
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

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, background_rect)
    screen.blit(array1_surface, array1_rect)
    screen.blit(array2_surface, array2_rect)
    screen.blit(overlay_image, overlay_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
