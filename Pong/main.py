import pygame
import random

screen_width = 960
screen_height = 720

color_black = (0, 0, 0)
color_white = (255, 255, 255)

def main():
    # Game screen setup
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("Pong")

    # Game loop
    while True:
        screen.fill(color_black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return    #Exiting the game

if __name__ == '__main__':
    main()