import pygame
import random

pygame.init()

# Original screen size and character size
screen_size = 800, 600
character_size = 57, 81

# Character and platform initialization
character_x = screen_size[0] // 2
character_y = screen_size[1] - character_size[1]
character_x_speed = 0
character_y_speed = 0
gravity = 1
jump = False
jump_height = -25

# Create the screen with original dimensions
scaled_screen_size = screen_size
screen = pygame.display.set_mode(scaled_screen_size)
pygame.display.set_caption("Fighter")

# Load the background image
background = pygame.image.load("sprites/background.png")
background = pygame.transform.scale(background, screen_size)

# Load and scale the character image
character = pygame.image.load("sprites/idle2.png")
character_right = pygame.transform.scale(character, character_size)
character_left = pygame.transform.flip(character_right, flip_x=True, flip_y=False)

character_direction = "right"

# Camera position initialization
camera_x = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                character_x_speed = -2
                character_direction = "left"
            if event.key == pygame.K_d:
                character_x_speed = 2
                character_direction = "right"
            if event.key == pygame.K_SPACE:
                if not jump:
                    jump = True
                    character_y_speed = jump_height

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                character_x_speed = 0
                
    character_y_speed += gravity
    character_y += character_y_speed

    # Character boundaries
    if character_y > screen_size[1] - character_size[1]:
        character_y = screen_size[1] - character_size[1]
        jump = False

    # Update character position
    character_x += character_x_speed

    # Adjust the camera position to follow the character
    camera_x = character_x - (screen_size[0] // 2)

    # Calculate the number of times the background should be duplicated
    background_repeats = camera_x // background.get_width()

    # Draw the duplicated background segments
    for i in range(background_repeats, background_repeats + 2):
        screen.blit(background, (i * background.get_width() - camera_x, 0))

    # Draw the character
    if character_direction == "right":
        screen.blit(character_right, (character_x - camera_x, character_y))
    else:
        screen.blit(character_left, (character_x - camera_x, character_y))

    pygame.display.update()


pygame.quit()


