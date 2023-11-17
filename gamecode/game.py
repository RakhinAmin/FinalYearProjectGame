import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scrolling Shooter Game')

clock = pygame.time.Clock()
FPS = 60

BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, color):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction_x = 0
        self.direction_y = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.jump = False
        self.jump_height = 10

    def move(self, direction_x):
        self.direction_x = direction_x

    def jump_start(self):
        if not self.jump:
            self.jump = True
            self.jump_height = 10

    def update(self):
        self.rect.x += self.direction_x
        self.check_boundary_collision()
        self.check_enemy_collision()

        if self.jump:
            self.rect.y -= self.jump_height
            self.jump_height -= 1

            if self.rect.y >= 200:  # Modify the value as needed
                self.rect.y = 200
                self.jump = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_boundary_collision(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def check_enemy_collision(self):
        if self.rect.colliderect(enemy.rect):
            print("Player collision with enemy detected!")


player = Soldier(200, 200, 30, 30, 5, (255, 0, 0))
enemy = Soldier(400, 200, 30, 30, 5, (0, 0, 255))

run = True
while run:
    clock.tick(FPS)
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_LEFT:
                player.move(-player.speed)
            if event.key == pygame.K_RIGHT:
                player.move(player.speed)
            if event.key == pygame.K_UP:
                player.jump_start()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.move(0)

    player.update()
    player.draw()
    enemy.draw()
    pygame.display.update()

pygame.quit()
