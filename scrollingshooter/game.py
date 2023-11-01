import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.8)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shooter Game')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('img/player/Idle/0.png')
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale),
                    int(image.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        window.blit(self.image, self.rect)


player1 = Player(200, 200, 3)
player2 = Player(400, 200, 3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player1.draw()
    player2.draw()

    pygame.display.update()

pygame.quit()

# import pygame

# pygame.init()

# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.8)

# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('Shooter Game')

# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, color):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def draw(self):
#         window.blit(self.image, self.rect)

# player1 = Player(200, 200, 30, 30, (255, 0, 0))  # Red rectangle
# player2 = Player(400, 200, 30, 30, (0, 0, 255))  # Blue rectangle

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     window.fill((0, 0, 0))  # Clear the screen

#     player1.draw()
#     player2.draw()

#     pygame.display.update()

# pygame.quit()
