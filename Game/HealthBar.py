import pygame

from utils.util import utils


class HealthBar:
    def __init__(self,health,color,width,height = 2):
        self.maxHealth = health
        self.color = color
        self.width = width
        self.height = height

    def draw(self,health,pos):
        if health > 0 :
            maxHpWidth = self.width
            hpWidth = int(maxHpWidth / self.maxHealth)
            if hpWidth < 1:
                hpWidth = 1

            pygame.draw.rect(utils.display, (233, 233, 233), (pos.x , pos.y , maxHpWidth, self.height), 1)

            x = pos.x
            for i in range(0, health):
                pygame.draw.rect(utils.display, self.color, (x, pos.y , hpWidth, self.height))
                x += hpWidth