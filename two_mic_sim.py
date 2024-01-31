import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1201, 801
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")

# Initial position of the point
x, y = WIDTH // 2, HEIGHT // 2

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_RIGHT]:
        x += 1
    if keys[pygame.K_UP]:
        y -= 1
    if keys[pygame.K_DOWN]:
        y += 1

    # Draw the coordinate system
    screen.fill(WHITE)
    pygame.draw.line(screen, RED, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    pygame.draw.line(screen, RED, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

    # Draw the point
    pygame.draw.circle(screen, RED, (x, y), 3)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    pygame.time.Clock().tick(30)
