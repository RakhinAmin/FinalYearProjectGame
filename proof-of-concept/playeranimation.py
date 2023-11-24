import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Shooter Game')


class Player:

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False  # Exit the game when the ESC key is pressed
                if event.key == K_UP:
                    self.move_up()  # Call the move_up method
                if event.key == K_DOWN:
                    self.move_down()  # Call the move_down method
                if event.key == K_LEFT:
                    self.move_left()  # Call the move_left method
                if event.key == K_RIGHT:
                    self.move_right()  # Call the move_right method
                elif event.type == QUIT:
                    run = False
