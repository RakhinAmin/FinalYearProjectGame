import random

import noise
import pygame

from utils.util import utils


class Map:
    def __init__(self):
        self.CHUNK_SIZE = 8
        self.grass_img = pygame.image.load('assets/img/grass.png')
        self.dirt_img = pygame.image.load('assets/img/dirt.png')
        self.plant_img = pygame.image.load('assets/img/plant.png').convert()
        self.plant_img.set_colorkey((255, 255, 255))
        self.tile_index = {
            1: self.grass_img,
            2: self.dirt_img,
            3: self.plant_img
        }
        self.true_scroll = [0, 0]
        self.game_map = {}
        self.tile_rects = []

    def procedural_map(self, x, y):
        map_chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
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

    def update(self, player):
        self.true_scroll[0] += (player.pos.x - self.true_scroll[0] - 50) / 20
        self.true_scroll[1] += (player.pos.y - self.true_scroll[1] - 106) / 20

    def draw(self):
        # true_scroll[0] += (player.rect.x - true_scroll[0] - 152) / 20
        # true_scroll[1] += (player.rect.y - true_scroll[1] - 106) / 20

        scroll = self.true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        utils.scroll = scroll
        # pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

        tileSize = 16
        for y in range(3):
            for x in range(4):
                target_x = x - 1 + \
                    int(round(scroll[0] / (self.CHUNK_SIZE * tileSize)))
                target_y = y - 1 + \
                    int(round(scroll[1] / (self.CHUNK_SIZE * tileSize)))
                target_chunk = (target_x, target_y)
                if target_chunk not in self.game_map:
                    self.game_map[target_chunk] = self.procedural_map(
                        target_x, target_y)
                for tile in self.game_map[target_chunk]:
                    utils.display.blit(
                        self.tile_index[tile[1]], (tile[0][0] * tileSize - scroll[0], tile[0][1] * tileSize - scroll[1]))
                    if tile[1] in [1, 2]:
                        rect = pygame.Rect(
                            tile[0][0] * tileSize, tile[0][1] * tileSize, tileSize, tileSize)
                        self.tile_rects.append(rect)

                        # pygame.draw.rect(utils.display,(233,23,23),(rect.x - utils.scroll[0],rect.y - utils.scroll[1],rect.w, rect.h),1)

    def resetTiles(self):
        self.tile_rects = []

    def collidePlayer(self, player):
        rect = player.getRect()
        isCollide = False
        for tile in self.tile_rects:
            if utils.collide_rect(tile, player.getRect()):
                isCollide = True
                if player.vel.y > 0:
                    player.onGround = True
                    player.acc.y = 0
                    player.vel.y = 0
                    player.jumping = False
                    player.pos.y = player.prevPos.y
                    continue
                if player.vel.x > 0:
                    player.pos.x = player.prevPos.x
                elif player.vel.x < 0:
                    player.pos.x = player.prevPos.x

        if not isCollide:
            player.onGround = False
        return False
