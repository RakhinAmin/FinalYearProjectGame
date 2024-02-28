import unittest
from pygame.locals import *
import pygame
import random
import noise

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')


WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (10, 10))


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
        animation_list = []
        temp_list = []
        for i in range(5):
            img = pygame.image.load(
                f'img/{char_type}/idle/{i}.png').convert_alpha()
            temp_list.append(img)
        animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(
                f'img/{char_type}/run/{i}.png').convert_alpha()
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


class TestSoldier(unittest.TestCase):
    def setUp(self):
        self.player = Soldier(30, 30, 20, 20, (255, 0, 0), 'player')

    def test_initialization(self):
        self.assertTrue(self.player.alive)
        self.assertEqual(self.player.rect.width, 20)
        self.assertEqual(self.player.rect.height, 20)
        # Add more assertions as needed

    def test_collision_test(self):
        # Mock up some tiles for testing
        tiles = [
            pygame.Rect(0, 0, 20, 20),
            pygame.Rect(30, 30, 20, 20),
            # Add more tiles as needed
        ]
        collision_result = self.player.collision_test(self.player.rect, tiles)
        self.assertEqual(len(collision_result), 1)


class TestBullet(unittest.TestCase):
    def test_initialization(self):
        bullet = Bullet(10, 20, 1)
        self.assertEqual(bullet.rect.center, (10, 20))
        self.assertEqual(bullet.direction, 1)


if __name__ == '__main__':
    unittest.main()
