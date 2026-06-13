import pygame
import random
import sys

# constants for the windows width and height values
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# the RGB values for the colors used in the game
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def main(): 
    # GAME SETUP
    
    # initialize the PyGame library (this is absolutely necessary)
    pygame.init()

    # this creates the window for the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # set the window's title
    pygame.display.set_caption('Pong')

    # create the clock object to keep track of the time
    clock = pygame.time.Clock()
    
    '''
    this is to check whether or not to move the ball
    we will make it move after 3 seconds
    '''
    started = False
    
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT//2 - 50, 10, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT//2 - 50, 10, 100)

    # this is to track by how much the players' paddles will move per frame
    paddle_1_move = 0
    paddle_2_move = 0

    # this is the rectangle that represents the ball
    ball_rect = pygame.Rect(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2 - 12, 25, 25)

    # determine the x and y speed of the ball 
    ball_speed_x = random.randint(4, 6)
    ball_speed_y = random.randint(4, 6)

    # randomize the direction of the ball
    if random.randint(1, 2) == 1:
        ball_speed_x *= -1
    if random.randint(1, 2) == 1:
        ball_speed_y *= -1

    # Score variables
    score_left = 0
    score_right = 0
    font = pygame.font.SysFont('Consolas', 30)
    score_font = pygame.font.SysFont('Consolas', 48)

    # Wait timer for ball reset
    wait_timer = 0
    
    # GAME LOOP
    while True:
        screen.fill(COLOR_BLACK)
        
        # Draw scores
        score_text = score_font.render(f"{score_left}  {score_right}", True, COLOR_WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, 50)
        screen.blit(score_text, score_rect)
        
        # Draw center line
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH//2 - 2, i, 4, 10))
        
        # make the ball move after pressing space
        if not started:
            # draw some text to the center of the screen
            text = font.render('Press SPACE to Start', True, COLOR_WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            
            # update the display
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True

            continue  # Skip the rest of the loop until game starts

        delta_time = clock.tick(60)

        # checking for events
        for event in pygame.event.get():

            # if the user exits the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if the user is pressing a key
            if event.type == pygame.KEYDOWN:

                # PLAYER 1
                # if the key is W, set the movement of paddle_1 to go up
                if event.key == pygame.K_w:
                    paddle_1_move = -0.8

                # if the key is S, set the movement of paddle_1 to go down
                if event.key == pygame.K_s:
                    paddle_1_move = 0.8

                # PLAYER 2
                # if the key is the up arrow, set the movement of paddle_2 to go up
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.8
                # if the key is the down arrow, set the movement of paddle_2 to go down
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.8

            # if the player released a key
            if event.type == pygame.KEYUP:
                # if the key released is w or s, stop the movement of paddle_1
                if event.key == pygame.K_w or event.key == pygame.K_s: 
                    paddle_1_move = 0.0

                # if the key released is the up or down arrow, stop the movement of paddle_2
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle_2_move = 0.0

        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # if paddle_1 is going out of the screen by the top, set it to the maximum to limit its movement
        if paddle_1_rect.top < 0:
            paddle_1_rect.top = 0
        
        # paddle_1 is going out of the screen by the bottom, do the same thing   
        if paddle_1_rect.bottom > SCREEN_HEIGHT:
            paddle_1_rect.bottom = SCREEN_HEIGHT

        # do the same thing with paddle_2
        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0
        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT      

        # Ball movement with wait timer
        if wait_timer > 0:
            wait_timer -= delta_time
        else:
            # Move the ball
            ball_rect.x += ball_speed_x
            ball_rect.y += ball_speed_y

        # Ball collision with top and bottom
        if ball_rect.top <= 0:
            ball_speed_y *= -1
            ball_rect.top = 0
        
        if ball_rect.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
            ball_rect.bottom = SCREEN_HEIGHT

        # Ball collision with paddles
        if paddle_1_rect.colliderect(ball_rect):
            # Calculate hit position relative to paddle center
            hit_position = ball_rect.centery - paddle_1_rect.centery
            # Normalize hit position (-1 to 1)
            hit_position = hit_position / (paddle_1_rect.height / 2)
            # Change angle based on hit position
            ball_speed_y = hit_position * 8
            ball_speed_x = abs(ball_speed_x)  # Make sure it goes right
            ball_rect.left = paddle_1_rect.right + 1
            # Add slight speed increase
            if abs(ball_speed_x) < 12:
                ball_speed_x *= 1.05

        if paddle_2_rect.colliderect(ball_rect):
            # Calculate hit position relative to paddle center
            hit_position = ball_rect.centery - paddle_2_rect.centery
            # Normalize hit position (-1 to 1)
            hit_position = hit_position / (paddle_2_rect.height / 2)
            # Change angle based on hit position
            ball_speed_y = hit_position * 8
            ball_speed_x = -abs(ball_speed_x)  # Make sure it goes left
            ball_rect.right = paddle_2_rect.left - 1
            # Add slight speed increase
            if abs(ball_speed_x) < 12:
                ball_speed_x *= 1.05

        # Check if ball goes out of bounds (scoring)
        if ball_rect.left <= 0:
            score_right += 1
            # Reset ball position
            ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            # Reset speed and direction
            ball_speed_x = random.choice([-5, 5])
            ball_speed_y = random.choice([-4, -3, 3, 4])
            wait_timer = 1000  # Wait 1 second before serving
            started = False  # Pause game until space is pressed again
            
        if ball_rect.right >= SCREEN_WIDTH:
            score_left += 1
            # Reset ball position
            ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            # Reset speed and direction
            ball_speed_x = random.choice([-5, 5])
            ball_speed_y = random.choice([-4, -3, 3, 4])
            wait_timer = 1000  # Wait 1 second before serving
            started = False  # Pause game until space is pressed again

        # draw player 1 and player 2's rects with the white color
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)

        # draw the ball with the white color
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        # update the display (this is necessary for Pygame)
        pygame.display.update()

# run the game
if __name__ == '__main__':
    main()