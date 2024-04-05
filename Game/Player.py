import pygame
from pygame.math import Vector2

from Game.GameObject import GameObject
from Game.HealthBar import HealthBar
from Game.PlayerBullet import PlayerBullet
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class Player(GameObject):
    def __init__(self, pos, addBulletCallBack):
        super().__init__(pos, None)

        self.sheets = {
            'idle': SpriteSheet(assetsManager.get("player-idle"), 1, 5),
            'run': SpriteSheet(assetsManager.get("player-run"), 1, 6),
            'jump': SpriteSheet(assetsManager.get("player-jump"), 1, 1),
        }

        self.sheets['idle'].setPlay(0, 4, 0.07, True)
        self.sheets['run'].setPlay(0, 5, 0.07, True)
        self.sheets['jump'].setPlay(0, 0, 0.07, True)

        self.currentSheet = 'idle'
        self.img = self.sheets[self.currentSheet].getCurrentFrame()
        self.rect = self.getRect()

        self.prevPos = None
        self.speed = 2
        self.jumping = True
        self.shootUp = False
        self.health = 10

        self.healthBar = HealthBar(self.health, (23, 233, 233), 2 * 10)
        self.healthBar2 = HealthBar(self.health, (23, 233, 233), 80, 4)

        self.health = 10
        self.bullets = 10
        self.onGround = False

        self.addBulletCallBack = addBulletCallBack

    def update(self):
        if not self.onGround:
            self.applyForce(pygame.Vector2(0, 0.52))

        self.prevPos = Vector2(self.pos.x, self.pos.y)

        if self.jumping:
            self.currentSheet = 'jump'
        elif self.vel.x != 0:
            self.currentSheet = 'run'
        else:
            self.currentSheet = 'idle'

        super().update()

        self.sheets[self.currentSheet].play()
        self.img = self.sheets[self.currentSheet].getCurrentFrame()

        if self.pos.x < 50:
            self.pos.x = 50

    def draw(self):
        super().draw()
        self.healthBar.draw(self.health,
                            Vector2(self.getRect().x - utils.scroll[0], self.getRect().y - 4 - utils.scroll[1]))
        self.healthBar2.draw(self.health,
                             Vector2(2, 10))

        utils.display.blit(pygame.transform.scale(
            assetsManager.get("bulletIcon"), (8, 10)), (2, 15))
        utils.drawText(Vector2(10, 16), str(self.bullets),
                       (233, 233, 23), font=utils.font8)

    def onKeyDown(self, key):
        if key == pygame.K_a:
            if not self.flipX:
                self.pos.x = self.pos.x - 6

            self.flipX = True
            self.vel.x = -self.speed
            self.rect = self.getRect()

        elif key == pygame.K_d:
            if self.flipX:
                self.pos.x = self.pos.x + 12

            self.flipX = False
            self.vel.x = self.speed
            self.rect = self.getRect()

        elif key == pygame.K_f:
            self.shoot()

        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -7))
            self.jumping = True

    def onKeyUp(self, key):
        if key == pygame.K_a and self.vel.x == -self.speed:
            self.vel.x = 0
        elif key == pygame.K_d and self.vel.x == self.speed:
            self.vel.x = 0

    def getRect(self):
        if self.flipX:
            rect = pygame.rect.Rect(
                self.pos.x + 12, self.pos.y, self.img.get_width() - 18, self.img.get_height())
        else:
            rect = pygame.rect.Rect(
                self.pos.x, self.pos.y, self.img.get_width() - 12, self.img.get_height())
        return rect

    def shoot(self):
        if self.bullets <= 0:
            return

        self.bullets -= 1

        dirX = 1
        if self.flipX:
            dirX = -1
        bullet = PlayerBullet(
            Vector2(self.getRect().centerx + 8, self.getRect().centery - 4), dirX)
        self.addBulletCallBack(bullet)

        sounds.play("shot")
