import pygame
from pygame import Vector2

from Game.EnemyBullet import EnemyBullet
from Game.GameObject import GameObject
from Game.HealthBar import HealthBar
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Enemy(GameObject):
    def __init__(self,pos,addObjectCallBack):
        super().__init__(pos,None)
        self.onGround = False
        self.prevPos = pos
        self.sheet = SpriteSheet(assetsManager.get("enemy-idle"), 1, 5)
        self.sheet.setPlay(0, 4, 0.07, True)
        self.img = self.sheet.getCurrentFrame()
        self.addObjectCallBack = addObjectCallBack

        self.shootTime = 0
        self.health = 3
        self.healthBar = HealthBar(self.health, (233, 23, 23), self.getRect().w + 10)

    def update(self):
        self.prevPos = Vector2(self.pos.x,self.pos.y)
        super().update()
        self.shoot()
        self.sheet.play()
        self.img = self.sheet.getCurrentFrame()
        if not self.onGround:
            self.applyForce(Vector2(0,0.52))

    def shoot(self):
        # dirX = 1
        # if self.flipX:
        #     dirX = -1

        self.shootTime += utils.deltaTime()
        if self.shootTime >= 2:
            self.shootTime = 0
            bullet = EnemyBullet(Vector2(self.getRect().centerx - 8, self.getRect().centery - 4), -1)
            self.addObjectCallBack(bullet)

            sounds.play("shot")

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health,
                            Vector2(self.getRect().x - utils.scroll[0] - 2, self.getRect().y - 4 - utils.scroll[1]))

    def getRect(self):
        rect = pygame.rect.Rect(self.pos.x + 12, self.pos.y, self.img.get_width() - 18, self.img.get_height())
        return rect