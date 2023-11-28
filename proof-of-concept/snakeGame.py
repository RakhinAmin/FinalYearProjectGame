import pygame
from pygame.locals import *
import random

# Define the Fruit class to represent the apple object


class Fruit:
    def __init__(self, screen):
        self.screen = screen
        self.fruit_x = 200
        self.fruit_y = 200

    def draw_fruit(self):
        # Create a rectangle representing the fruit
        fruit_box = pygame.Rect((self.fruit_x, self.fruit_y, 25, 25))
        # Draw the fruit on display with a green color
        pygame.draw.rect(self.screen, (0, 255, 0), fruit_box)

# Define the Snake class to represent the snake object


class Snake:
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
        self.body_length = 1  # Initial length of the snake

        self.apple = Fruit(self.screen)
        self.spawn_apple()

    def spawn_apple(self):
        # Generate random coordinates for the apple
        self.apple.fruit_x = random.randrange(0, 700, 25)
        self.apple.fruit_y = random.randrange(0, 700, 25)

    def draw_snake(self):
        # Draw each segment of the snake
        for segment in self.body:
            pygame.draw.rect(self.screen, (255, 0, 0), segment)

    def move_snake(self):
        # Move the snake by adding a new head segment and removing the tail segment to maintain length
        new_head = pygame.Rect(self.body[0].left + self.direction_x,
                               self.body[0].top + self.direction_y, 25, 25)
        # insert new head as the first element of the list
        self.body.insert(0, new_head)
        # keeps the length correct by popping any overhanging elements off the list
        if len(self.body) > self.body_length:
            self.body.pop()

    def check_collision(self):
        # Check if the snake's head collides with the apple
        if self.body[0].colliderect(self.apple.fruit_x, self.apple.fruit_y, 25, 25):
            self.body_length += 1  # Increase the snake's length
            # increase speed by decreasing the interval between each movement
            self.move_interval -= 5
            self.spawn_apple()  # Spawn a new apple

    def check_self_collision(self):
        for i in self.body[1:]:  # create slice of the list that excludes the snake head
            if self.body[0].colliderect(i):
                pygame.quit()

    # Inside the Snake class, add a method to check for border collision
    def check_border_collision(self):
        if (self.body[0].left < 0 or self.body[0].right > 700 or
                self.body[0].top < 0 or self.body[0].bottom > 700):
            pygame.quit()

    def auto_move(self):
        self.move_timer += self.clock.tick(30)  # Limit frame rate to 30 FPS
        if self.move_timer >= self.move_interval:  # Check if move timer has exceeded the frame time limit
            self.move_snake()  # Move the snake
            self.check_collision()
            self.check_self_collision()  # Check for collision with the apple
            self.check_border_collision()
            self.move_timer = 0  # Reset the move timer

    # Move functions for arrow key controls
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

            self.auto_move()  # Automatically move the snake

            # Clear the screen with a background color
            self.screen.fill((110, 110, 5))

            self.draw_snake()  # Draw the snake on the screen
            self.apple.draw_fruit()  # Draw the apple on the screen

            pygame.display.update()  # Update the display to show the snake and apple

        pygame.quit()


# Run the game when this script is executed
if __name__ == "__main__":
    game = Snake()
    game.run_program()
