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


pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Scrolling shooter')

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player = Soldier(50, 50, 30, 30, (255, 0, 0))
enemy = Soldier(400, 200, 30, 30, (0, 0, 255))

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('dirt.png')

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [
    0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

true_scroll = [0, 0]

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '2', '2', '0',
                '2', '2', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '2', '0', '0', '2', '2', '0', '0', '0', '0',
                '0', '0', '0', '2', '2', '0', '0', '2', '2'],
            ['1', '1', '2', '2', '1', '1', '2', '2', '2', '2',
                '2', '2', '2', '1', '1', '2', '2', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        player.handle_event(event)

    true_scroll[0] += (player.rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(screen, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                               background_object[1][1] -
                               scroll[1] * background_object[0],
                               background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(screen, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(screen, (9, 91, 85), obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                screen.blit(
                    dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                screen.blit(
                    grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player.update()

    player.draw(screen)
    enemy.draw(screen)

    player.check_enemy_collision(enemy)

    pygame.display.update()
    clock.tick(60)
