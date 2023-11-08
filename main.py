import pygame
import random

pygame.init()

screen_size = 800, 600
character_size = 57, 81

character_x = screen_size[0] // 2
character_y = screen_size[1] - character_size[1]
character_x_speed = 0
character_y_speed = 0
gravity = 0.3
jump = False
jump_height = -13

scaled_screen_size = screen_size
screen = pygame.display.set_mode(scaled_screen_size)
pygame.display.set_caption("Ninja Dash")

background = pygame.image.load("sprites/background.png")
background = pygame.transform.scale(background, screen_size)

character = pygame.image.load("sprites/idle2.png")
character_right = pygame.transform.scale(character, character_size)
character_left = pygame.transform.flip(character_right, flip_x=True, flip_y=False)

character_direction = "right"

camera_x = 0

fire = pygame.image.load("sprites/fire.png")
fire_size = (32, 38)
fire = pygame.transform.scale(fire, fire_size)

fire_positions = []

spacing = 200

for i in range(40):
    fire_x = i * (fire_size[0] + spacing)
    fire_y = screen_size[1] - fire_size[1]
    fire_positions.append(pygame.Rect(fire_x, fire_y, fire_size[0], fire_size[1]))
    
game_over = False
game_over_font = pygame.font.Font(None, 100)
game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
game_over_text_rect = game_over_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

restart_font = pygame.font.Font(None, 40)
restart_text = restart_font.render("RESTART PRESS P", True, (255, 255, 255))
restart_text_rect = restart_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            game_over = False
            character_x = screen_size[0] // 2
            character_y = screen_size[1] - character_size[1]
            character_x_speed = 0
            character_y_speed = 0
            jump = False
        if not game_over:
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
    if not game_over:    
        character_y_speed += gravity
        character_y += character_y_speed

        if character_y > screen_size[1] - character_size[1]:
            character_y = screen_size[1] - character_size[1]
            jump = False
            character_y_speed = 0

        character_x += character_x_speed

        camera_x = character_x - (screen_size[0] // 2)

        background_repeats = camera_x // background.get_width()

        for i in range(background_repeats, background_repeats + 2):
            screen.blit(background, (i * background.get_width() - camera_x, 0))

        for fire_rect in fire_positions:
            if character_x + character_size[0] > fire_rect.left and character_x < fire_rect.right and \
                character_y + character_size[1] > fire_rect.top and character_y < fire_rect.bottom:
                character_y = fire_rect.top - character_size[1]
                game_over = True

        for fire_rect in fire_positions:
            screen.blit(fire, (fire_rect.x - camera_x, fire_rect.y))

        if character_direction == "right":
            screen.blit(character_right, (character_x - camera_x, character_y))
        else:
            screen.blit(character_left, (character_x - camera_x, character_y))
            
    if game_over:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(restart_text, restart_text_rect)
    pygame.display.update()

pygame.quit()
