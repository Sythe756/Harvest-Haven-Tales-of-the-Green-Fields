import pygame
import sys
import psycopg2  # Import the psycopg2 library for PostgreSQL interaction
from buttons import Button
from settings import *
from db import database, user, password, host, port


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
            (player_name, 200)  # Assuming an initial gold amount of 200
        )

        connection.commit()

    except psycopg2.Error as e:
        print("Error inserting player data:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()

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
                        # When the player presses Enter, insert their data into the database
                        insert_player_data(text, 200)  # Assuming an initial gold amount of 100
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        SCREEN.fill(WHITE)

        # Display the label above the input box
        label = get_font(FONT_SIZE).render("Please enter your name:", True, (0, 0, 0))
        label_rect = label.get_rect(center=(SCREEN_SIZE[0] // 2, 250))
        SCREEN.blit(label, label_rect)

        txt_surface = get_font(FONT_SIZE).render(text, True, color)
        width = max(200, txt_surface.get_width() + 100)
        input_box.w = width
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(SCREEN, color, input_box, 2)

        done_button = Button(pos=(650, 500), image=image, text_input="play", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Handle button interaction outside the name input loop
        done_button.changeColor(pygame.mouse.get_pos())
        done_button.update(SCREEN)
        
        pygame.display.flip()

        # Check if the "PLAY" button is clicked and return the player's name
        if done_button.checkForInput(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            # When the player clicks the "PLAY" button, insert their data into the database
            insert_player_data(text, 200)  # Assuming an initial gold amount of 100
            return text


if __name__ == "__main__":
    player_name = get_player_name()
    print("Player's name:", player_name)
