import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
a = 0.5 # [cm]
A = 1 # amplituda
c = 33000 # cm/s
starting_time = time.time()

freq = 100 # [Hz]
mics = []

#sample rate 10kHz
time_inc = 0.00001  

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")

# Initial position of the point
x, y = 0, 200
center_x, center_y = WIDTH // 2, HEIGHT // 2


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
        y += 1
    if keys[pygame.K_DOWN]:
        y -= 1

    # Draw the coordinate system
    screen.fill(WHITE)
    pygame.draw.line(screen, RED, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    pygame.draw.line(screen, RED, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

    # Draw the point
    pygame.draw.circle(screen, RED, (center_x + x, center_y - y), 3)

    # Update the display
    pygame.display.flip()

    t = time.time() - starting_time
    r = math.sqrt(x*x + y*y)
    th = math.atan2(x,y)*180/math.pi
    d1 = math.sqrt((x+a)*(x+a) + y*y) # levo
    d2 = math.sqrt((x-a)*(x-a) + y*y) # desno
    mics.append((t, (A/d1)*math.sin(2*math.pi*freq*(t-d1/c)), (A/d2)*math.sin(2*math.pi*freq*(t-d2/c)), math.sin(2*math.pi*freq)))


    print(x, " ", y, ", r = ", r, "th = ", th, ", t = ", t)  
    
    # Set the frame rate
    pygame.time.Clock().tick(30)      
