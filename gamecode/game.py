from pygame.locals import *
import pygame
import random
import noise
clock = pygame.time.Clock()


class Soldier:  # class created for the player character
    # initialising attributes for player character with color, movement and position
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.move_right = False
        self.move_left = False
        self.y_direction = 0
        self.air_time = 0

    # method to update the player position, handle movement, and check for collisions with environment
    def update(self, tile_rects):
        self.player_movement = [0, 0]
        if self.move_right:  # update left and right movements
            self.player_movement[0] += 2
        if self.move_left:
            self.player_movement[0] -= 2
        # update vertical jump movement (simulates gravity)
        self.player_movement[1] += self.y_direction
        self.y_direction += 0.05
        if self.y_direction > 3:
            self.y_direction = 3

        self.rect, collisions = self.move(  # call the movement method and collision method
            self.rect, self.player_movement, tile_rects)

        # collision detection with the ground, eventually will implement game over mechanism
        if collisions['bottom']:
            self.air_time = 0
            self.y_direction = 0
        else:
            self.air_time += 1

    def draw(self, surface):  # draw and display the player character
        pygame.draw.rect(surface, self.color, self.rect)

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


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

player = Soldier(30, 30, 20, 20, (255, 0, 0))
enemy = Soldier(170, 170, 20, 20, (0, 0, 255))

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

bullet_img = pygame.image.load('bullet.png').convert_alpha()

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

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
plant_img = pygame.image.load('plant.png').convert()
plant_img.set_colorkey((255, 255, 255))

tile_index = {1: grass_img,
              2: dirt_img,
              3: plant_img
              }

game_map = {}

while True:  # game loop
    display.fill((146, 244, 255))  # clear screen by filling it with blue

    true_scroll[0] += (player.rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

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

    pygame.draw.rect(display, (255, 0, 0), (player.rect.x -
                     scroll[0], player.rect.y - scroll[1], player.rect.width, player.rect.height))

    enemy.update(tile_rects)
    pygame.draw.rect(display, enemy.color, (enemy.rect.x -
                     scroll[0], enemy.rect.y - scroll[1], enemy.rect.width, enemy.rect.height))

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
