import pygame
from pygame.locals import *


class Soldier:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.move_right = False
        self.move_left = False
        self.y_direction = 0
        self.air_time = 0

    def update(self, tile_rects):
        self.player_movement = [0, 0]
        if self.move_right:
            self.player_movement[0] += 2
        if self.move_left:
            self.player_movement[0] -= 2
        self.player_movement[1] += self.y_direction
        self.y_direction += 0.2
        if self.y_direction > 3:
            self.y_direction = 3

        self.rect, collisions = self.move(
            self.rect, self.player_movement, tile_rects)

        if collisions['bottom']:
            self.air_time = 0
            self.y_direction = 0
        else:
            self.air_time += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

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

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False,
                           'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types

    def collision_test(self, rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile)]


pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Scrolling shooter')

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

player = Soldier(30, 30, 20, 20, (255, 0, 0))
enemy = Soldier(400, 200, 20, 20, (0, 0, 255))

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('dirt.png')

true_scroll = [0, 0]

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0


def load_map(path):
    with open(path + '.txt', 'r') as f:
        game_map = [list(row) for row in f.read().split('\n')]
    return game_map


game_map = load_map('map')

while True:
    display.fill((146, 244, 255))

    true_scroll[0] += (player.rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(
                    dirt_image, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(
                    grass_image, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player.rect, collisions = player.move(
        player.rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    pygame.draw.rect(display, (255, 0, 0), (player.rect.x -
                     scroll[0], player.rect.y - scroll[1], player.rect.width, player.rect.height))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)


pygame.quit()
