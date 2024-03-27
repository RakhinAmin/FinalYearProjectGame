import pygame

from utils.util import utils

BG = (23, 23, 23)
class Bg:
    def __init__(self):
        self.bg_scroll = 0

        self.pine1_img = pygame.image.load('assets/img/Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('assets/img/Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('assets/img/Background/mountain.png').convert_alpha()
        self.sky_img = pygame.image.load('assets/img/Background/sky_cloud.png').convert_alpha()

    def draw(self):
        self.bg_scroll = utils.scroll[0]
        utils.display.fill(BG)
        width = self.sky_img.get_width()
        for x in range(20):
            utils.display.blit(self.sky_img, ((x * width) - self.bg_scroll * 0.5, -70))
            utils.display.blit(self.mountain_img, ((x * width) - self.bg_scroll * 0.6, utils.height - self.mountain_img.get_height() - 350))
            utils.display.blit(self.pine1_img, ((x * width) - self.bg_scroll * 0.7, utils.height - self.pine1_img.get_height() - 250))
            utils.display.blit(self.pine2_img, ((x * width) - self.bg_scroll * 0.8, utils.height - self.pine2_img.get_height() - 200))
