import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Shooter Game')


class Player:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.box_x = 100  # Initial x-coordinate of the snake's head
        self.box_y = 100  # Initial y-coordinate of the snake's head
        self.screen = pygame.display.set_mode(
            (700, 700))  # Create the game window
        pygame.display.set_caption("Snake Game")  # Set the window title

        self.direction_x = 0  # Initial x-direction of the snake's movement
        self.direction_y = 0  # Initial y-direction of the snake's movement
        self.move_timer = 0  # Initialize a timer for controlling movement
        # Set the interval for snake movement (milliseconds)
        self.move_interval = 150
        self.clock = pygame.time.Clock()  # Create a Pygame clock object

        # Initialize with a starting segment
        self.body = [pygame.Rect(self.box_x, self.box_y, 25, 25)]

        def move_up(self):
            self.direction_x = 0
            self.direction_y = -25

        def move_down(self):
            self.direction_x = 0
            self.direction_y = 25

        def move_left(self):
            self.direction_x = -25
            self.direction_y = 0

        def move_right(self):
            self.direction_x = 25
            self.direction_y = 0

    def run_program(self):
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
                    run = False  # Exit the game when the window is closed


if __name__ == "__main__":
    game = Player()
    game.run_program()
