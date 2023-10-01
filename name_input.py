import pygame
import sys
from buttons import Button  # Assuming you have a 'Button' class defined in your 'buttons.py' file
from settings import *

# Constants
SCREEN_SIZE = (1280, 695)
WHITE = (255, 255, 255)
FONT_SIZE = 45
image = pygame.image.load("./assets/menu/Play Rect.png")

# Initialize Pygame
pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Harvest Haven 1.13")

def get_font(size):
    return pygame.font.Font("./assets/font/LycheeSoda.ttf", size)

def get_player_name():
    input_box = pygame.Rect(540, 300, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        SCREEN.fill(WHITE)
        txt_surface = get_font(FONT_SIZE).render(text, True, color)
        width = max(200, txt_surface.get_width() + 100)
        input_box.w = width
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(SCREEN, color, input_box, 2)

        done_button = Button(pos=(600, 500), image=image, text_input="play", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Handle button interaction outside the name input loop
        done_button.changeColor(pygame.mouse.get_pos())
        done_button.update(SCREEN)
        
        pygame.display.flip()

        # Check if the "PLAY" button is clicked and return the player's name
        if done_button.checkForInput(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return text

if __name__ == "__main__":
    player_name = get_player_name()
    print("Player's name:", player_name)

