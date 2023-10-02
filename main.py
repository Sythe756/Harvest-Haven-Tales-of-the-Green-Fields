import pygame
import sys
import psycopg2
from buttons import Button
from level import Level
from settings import *
from name_input import get_player_name
from db import *




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

# Function to insert player data into PostgreSQL database
def insert_player_data(player_name, gold_amount):
    try:
        connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()

        # Insert player data into the table
        cursor.execute(
            "INSERT INTO player_data (player_name, gold_amount) VALUES (%s, %s)",
            (player_name, gold_amount)
        )

        connection.commit()

    except psycopg2.Error as e:
        print("Error inserting player data:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to retrieve highscore data from the database
def get_highscore_data():
    try:
        connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()

        # Retrieve highscore data from the table, assuming it has 'player_name' and 'gold_amount' columns
        cursor.execute(
            "SELECT player_name, gold_amount FROM player_data ORDER BY gold_amount DESC LIMIT 10"
        )
        highscores = cursor.fetchall()

        return highscores

    except psycopg2.Error as e:
        print("Error retrieving highscore data:", e)
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

def toggle_black_screen(player, black_screen_visible):
    if black_screen_visible and pygame.key.get_pressed()[pygame.K_i]:
        player.display_inventory(SCREEN)

def game_loop(player_name):
    game_level = Level()
    player = game_level.player

    black_screen_visible = False
    highscore_visible = False
    highscores = []  # Initialize the highscores list

    while True:
        dt = pygame.time.Clock().tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    toggle_black_screen(player, black_screen_visible)
                elif event.key == pygame.K_h:
                    highscore_visible = not highscore_visible  # Toggle visibility
                    if highscore_visible:
                        highscores = get_highscore_data()  # Fetch highscores only when needed

        game_level.run(dt)

        if black_screen_visible:
            pygame.draw.rect(SCREEN, BLACK, (0, 0, *SCREEN_SIZE))

        player.display_inventory(SCREEN)

        if highscore_visible:
            if highscores:
                y = 100
                for idx, (name, gold) in enumerate(highscores, 1):
                    text = f"{idx}. {name}: {gold} gold"
                    highscore_text = get_font(FONT_SIZE).render(text, True, WHITE)
                    SCREEN.blit(highscore_text, (50, y))
                    y += 50

        pygame.display.update()

        # Update player's money in the database
        update_player_money(player_name, player.money)

def options_menu():
    while True:
        SCREEN.fill(BLACK)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        COMING_SOON_TEXT = get_font(MENU_FONT_SIZE).render("Coming Soon!", True, WHITE)
        COMING_SOON_RECT = COMING_SOON_TEXT.get_rect(center=(640, 300))

        BACK_BUTTON = Button(image=pygame.image.load("./assets/menu/Play Rect.png"), pos=(100, 100),
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(COMING_SOON_TEXT, COMING_SOON_RECT)

        buttons = [BACK_BUTTON]

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
                        if button == BACK_BUTTON:
                            return  # Return to the main menu

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
                            player_name = get_player_name()
                            if player_name:
                                game_loop(player_name)
                        elif button == OPTIONS_BUTTON:
                            options_menu()
                        elif button == QUIT_BUTTON:
                            pygame.quit()  
                            sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
