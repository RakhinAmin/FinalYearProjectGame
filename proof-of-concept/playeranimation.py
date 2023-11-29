import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooting bullets POC')

clock = pygame.time.Clock()
FPS = 60

BG = (144, 201, 120)

player_image = pygame.image.load("player.png").convert()
player_image = pygame.transform.scale(player_image, (30, 30))
playerflip = pygame.transform.flip(player_image, True, False)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction_x = 0
        self.direction_y = 0
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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

        if self.direction_x < 0:
            self.image = playerflip
        elif self.direction_x > 0:
            self.image = player_image

        if self.jump:
            self.rect.y -= self.jump_height
            self.jump_height -= 1

            if self.rect.y >= 200:
                self.rect.y = 200
                self.jump = False

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (20, 20))

shoot = False
bullet_group = pygame.sprite.Group()

player = Player(200, 200, 5)

run = True
while run:
    clock.tick(FPS)
    screen.fill(BG)

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
            if event.key == pygame.K_SPACE:
                player.jump_start()
            if event.key == pygame.K_f:
                shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.move(0)
            if event.key == pygame.K_f:
                shoot = False

    bullet_group.update()
    bullet_group.draw(screen)

    player.update()
    player.draw()

    if shoot:
        bullet = Bullet(player.rect.centerx, player.rect.centery,
                        1 if player.direction_x > 0 else -1)
        bullet_group.add(bullet)

    pygame.display.update()

pygame.quit()
