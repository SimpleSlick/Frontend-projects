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

    pygame.display.set_caption('Pong')

    clock = pygame.time.Clock()

    started = False

    paddle_1 = pygame.rect(30, 0, 7, 100)
    paddle_2 = pygame.rect(screen_width - 50, 0, 7, 100)

    # Track for paddle movement
    paddle_1_move = 0
    paddle_2_move = 0

    ball = pygame.rect(screen_width / 2, screen_height /2, 25, 25)

    # speed of ball in x and y
    ball_acc_x = random.randint(2, 4) * 0.1
    ball_acc_y = random.randint(2, 4) * 0.1

    if random.randint(1, 2):
        ball_acc_x *= -1
    if random.randint(1, 2):
        ball_acc_y *= -1

    # Game loop
    while True:
        screen.fill(color_black)

        if not started:
            # Loading the font
            font = pygame.font.SysFont('Consolas, 30')

            # some text at the centre of screen
            text = font.render('Press Space to Start', True, color_white)
            text_rect = text.get_rect()
            text_rect.center = (screen_width // 2, screen_height // 2)
            screen.blit(text, text_rect)

            # Update the display
            pygame.display.flip()

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True

        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return    #Exiting the game
            
        # Drawing player 1 and player 2
        pygame.draw.rect(screen, color_white, paddle_1)
        pygame.draw.rect(screen, color_white, paddle_2)

        # Ball
        pygame.draw.rect(screen, color_white, ball)

        # update
        pygame.display.update()

if __name__ == '__main__':
    main()