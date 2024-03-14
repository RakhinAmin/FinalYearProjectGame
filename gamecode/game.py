from pygame.locals import *
import pygame
import random
import noise
import os
clock = pygame.time.Clock()


class Soldier:
    def __init__(self, x, y, width, height, color, char_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True
        self.color = color
        self.move_right = False
        self.move_left = False
        self.y_direction = 0
        self.jump = False
        self.air_time = 0
        self.animation_list = self.load_images(char_type)
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.index]

    def load_images(self, char_type):
        animation_types = ['idle', 'run', 'jump']
        animation_list = []
        for animation in animation_types:
            temp_list = []
            path = f'assets/img/{char_type}/{animation}'
            num_of_frames = len(os.listdir(path))
            print(f"Loading {num_of_frames} frames from {path}")
            for i in range(num_of_frames):
                img_path = f'{path}/{i}.png'
                print(f"Loading image {img_path}")
                img = pygame.image.load(img_path).convert_alpha()
                temp_list.append(img)
            animation_list.append(temp_list)
        return animation_list

    def update(self, tile_rects):
        self.player_movement = [0, 0]
        if self.move_right:
            self.player_movement[0] += 2
        if self.move_left:
            self.player_movement[0] -= 2

        self.player_movement[1] += self.y_direction
        self.y_direction += 0.05
        if self.y_direction > 3:
            self.y_direction = 3

        self.rect, collisions = self.move(
            self.rect, self.player_movement, tile_rects)

        if collisions['bottom']:
            self.air_time = 0
            self.y_direction = 0
        else:
            self.air_time += 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # if animation runs out then reset to the start
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def update_action(self, new_action):
        # check if new action is different from previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface, scroll):
        adjusted_y = self.rect.y - scroll[1] - 15  # Adjust 10 pixels higher
        surface.blit(self.image, (self.rect.x - scroll[0], adjusted_y))

    def handle_event(self, event):  # method to handle keyboard inputs for movement
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

    def handle_collision(self):  # method to handle collisions with the display boundaries
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
            # console log shows collision detection with enemy, will be further implemented later
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
                # Check if the player is colliding with a plant tile
            if tile[1] == 3:
                # Slow down the player when colliding with a plant
                movement[0] *= 0.9
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

    def collision_test(self, rect, tiles):  # checking for collision with tile map tiles
        return [tile for tile in tiles if rect.colliderect(tile)]


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
        if self.rect.right < 0 or self.rect.left > WINDOW_SIZE[0]:
            self.kill()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (800, 540)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

player = Soldier(30, 30, 20, 20, (255, 0, 0), 'player')
enemy = Soldier(170, 170, 20, 20, (0, 0, 255), 'enemy')

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0


shoot = False
bullet_group = pygame.sprite.Group()

true_scroll = [0, 0]

CHUNK_SIZE = 8


def procedural_map(x, y):
    map_chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)

            tile_type = 0  # nothing
            if target_y > 8 - height:
                tile_type = 2  # dirt
            elif target_y == 8 - height:
                tile_type = 1  # grass
            elif target_y == 8 - height - 1 and random.randint(1, 5) == 1:
                tile_type = 3  # plant

            if tile_type != 0:
                map_chunk_data.append([[target_x, target_y], tile_type])

    return map_chunk_data


moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

bullet_img = pygame.image.load('assets/img/bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (10, 10))

player_img = pygame.image.load('assets/img/player/idle/4.png').convert_alpha()
enemy_img = pygame.image.load('assets/img/enemy/idle/4.png').convert_alpha()

grass_img = pygame.image.load('assets/img/grass.png')
dirt_img = pygame.image.load('assets/img/dirt.png')
plant_img = pygame.image.load('assets/img/plant.png').convert()
plant_img.set_colorkey((255, 255, 255))

tile_index = {1: grass_img,
              2: dirt_img,
              3: plant_img
              }

game_map = {}

bullet_group = pygame.sprite.Group()

while True:  # game loop
    display.fill((146, 244, 255))  # clear screen by filling it with blue

    true_scroll[0] += (player.rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))
            target_chunk = (target_x, target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = procedural_map(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(
                    tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(
                        tile[0][0] * 16, tile[0][1] * 16, 16, 16))

    # update player actions
    if player.alive:
        if moving_left or moving_right:
            player.update_action(1)  # means run
        else:
            player.update_action(0)  # means idle

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player.update(tile_rects)

    player.rect, collisions = player.move(
        player.rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player.update_animation()
    enemy.update_animation()
    player.draw(display, scroll)

    enemy.update(tile_rects)
    enemy.draw(display, scroll)  # Draw the enemy using its draw method

    bullet_group.update()
    bullet_group.draw(display)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP and player.alive:
                player.jump = True
                if air_timer < 6:
                    vertical_momentum = -5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == K_f:
                bullet = Bullet(
                    player.rect.centerx - scroll[0], player.rect.centery - scroll[1] - 10, 1 if player_movement[0] > 0 else -1)
                bullet_group.add(bullet)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)


pygame.quit()
