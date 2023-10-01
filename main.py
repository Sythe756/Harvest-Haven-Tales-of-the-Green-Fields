import pygame
import sys
from buttons import Button
from level import Level
from settings import *

# Constants
SCREEN_SIZE = (1280, 695)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 45
MENU_FONT_SIZE = 100

# Initialize Pygame
pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Harvest Haven 1.13")
BG = pygame.image.load("./assets/menu/farm-game-background-vector.jpg").convert_alpha()

def get_font(size):
    return pygame.font.Font("./assets/font/LycheeSoda.ttf", size)

def toggle_black_screen(player, black_screen_visible):
    if black_screen_visible and pygame.key.get_pressed()[pygame.K_i]:
        player.display_inventory(SCREEN)
def game_loop():
    game_level = Level()
    player = game_level.player

    black_screen_visible = False

    while True:
        dt = pygame.time.Clock().tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    toggle_black_screen(player, black_screen_visible)

        game_level.run(dt)

        if black_screen_visible:
            pygame.draw.rect(SCREEN, BLACK, (0, 0, *SCREEN_SIZE))

        player.display_inventory(SCREEN)

        # Update only the parts of the screen that need it
        pygame.display.update()

def options_menu():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(WHITE)
        OPTIONS_TEXT = get_font(FONT_SIZE).render("Coming Soon", True, BLACK)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color=BLACK, hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return

        # Update only the parts of the screen that need it
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(MENU_FONT_SIZE).render("Harvest Haven", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        
        PLAY_BUTTON = Button(image=pygame.image.load("./assets/menu/Play Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("./assets/menu/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./assets/menu/Quit Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        buttons = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]
        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        if button == PLAY_BUTTON:
                            game_loop()
                        elif button == OPTIONS_BUTTON:
                            options_menu()
                        elif button == QUIT_BUTTON:
                            pygame.quit()
                            sys.exit()

        # Update only the parts of the screen that need it
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
