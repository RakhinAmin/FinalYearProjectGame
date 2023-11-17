import pygame


class Soldier:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.move_right = False
        self.move_left = False
        self.y_direction = 0
        self.air_time = 0

    def update(self):
        self.player_movement = [0, 0]
        if self.move_right:
            self.player_movement[0] += 2
        if self.move_left:
            self.player_movement[0] -= 2
        self.player_movement[1] += self.y_direction
        self.y_direction += 0.2
        if self.y_direction > 3:
            self.y_direction = 3

        self.rect.x += self.player_movement[0]
        self.rect.y += self.player_movement[1]

        self.handle_collision()

        self.air_time += 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move_right = True
            if event.key == pygame.K_LEFT:
                self.move_left = True
            if event.key == pygame.K_UP:
                if self.air_time < 6:
                    self.y_direction = -5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False

    def handle_collision(self):
        if self.rect.y > WINDOW_SIZE[1] - self.rect.height:
            self.rect.y = WINDOW_SIZE[1] - self.rect.height
            self.y_direction = 0
            self.air_time = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_SIZE[0]:
            self.rect.right = WINDOW_SIZE[0]

    def check_enemy_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            print("Player collision with enemy detected!")


clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption('Scrolling schooter')

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player = Soldier(50, 50, 30, 30, (255, 0, 0))
enemy = Soldier(400, 200, 30, 30, (0, 0, 255))

while True:
    screen.fill((144, 201, 120))

    player.update()

    player.draw(screen)
    enemy.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        player.handle_event(event)

    player.check_enemy_collision(enemy)

    pygame.display.update()
    clock.tick(60)
