import pygame
import sys

pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Farmer Fox Chicken Grain Riddle")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (50, 50, 100, 100))

    pygame.display.flip()
    
pygame.quit()
sys.exit()