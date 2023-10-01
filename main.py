import pygame
import random

pygame.init()


platform_surfaces = []  # Create a list to store the platform surfaces
screen_size = 800, 600
character_size = 57, 81

platform_size = 100, 20

num_platforms = 5  # Adjust the number of platforms as needed
platforms = []

# Initial character position
character_x = screen_size[0] // 2
character_y = screen_size[1] - character_size[1]

# Character movement variables
character_x_speed = 0
character_y_speed = 0
gravity = 1  # You can adjust the gravity value

jump = False
jump_height = -25  # Adjust for the desired jump height


screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Fighter")

background = pygame.image.load("sprites/background.png")
background = pygame.transform.scale(background, screen_size)

character = pygame.image.load("sprites/idle2.png")
character_right = pygame.transform.scale(character, character_size)
character_left = pygame.transform.flip(character_right, flip_x=True, flip_y=False)

# Load and resize the platform image
platform = pygame.image.load("sprites/tile.png")
platform = pygame.transform.scale(platform, (platform_size[0], platform_size[1]))

for platform in platforms:
    platform_surface = pygame.Surface((platform_size[0], platform_size[1]))
    platform_surface.blit(platform, (0, 0))  # Blit the platform image onto the platform surface
    platform_surfaces.append(platform_surface)

character_direction = "right"  # Initially facing right

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Check for key presses
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

        # Check for key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                character_x_speed = 0
                
    character_y_speed += gravity
    character_y += character_y_speed

    # Character boundaries
    if character_x < 0:
        character_x = 0
    if character_x > screen_size[0] - character_size[0]:
        character_x = screen_size[0] - character_size[0]
    if character_y > screen_size[1] - character_size[1]:
        character_y = screen_size[1] - character_size[1]
        jump = False

    # Inside the game loop, check for collisions with the platforms
    for platform in platforms:
        platform_x, platform_y = platform
        if (character_y + character_size[1] >= platform_y) and (character_y + character_size[1] <= platform_y + platform_size[1]) and (character_x + character_size[0] >= platform_x) and (character_x <= platform_x + platform_size[0]):
            character_y = platform_y - character_size[1]
            jump = False

    # Draw the character and platforms
    for i, platform in enumerate(platforms):
        platform_x, platform_y = platform
        screen.blit(platform_surfaces[i], (platform_x, platform_y))
        
    # Update character position
    character_x += character_x_speed
    screen.blit(background, (0, 0))
    # Draw the character
    if character_direction == "right":
        screen.blit(character_right, (character_x, character_y))
    else:
        screen.blit(character_left, (character_x, character_y))
    pygame.display.update()

pygame.quit()


