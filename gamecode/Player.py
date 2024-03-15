import pygame
from pygame.math import Vector2


from utils.util import utils


class Player(GameObject):
    def __init__(self, pos):
        super().__init__(pos, None)
        self.speed = 5
        self.jumping = False

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
        # self.healthBar = HealthBar(self.health, (23, 233, 233), self.getRect().w + 2)
        self.bullets = 0
        self.onGround = False
        self.gravity = 0.52

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

    def draw(self):
        super().draw()
        # self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))

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

        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.jumping = True
        elif key == pygame.K_w:
            self.shootUp = True

        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.applyForce(pygame.Vector2(0, -7))
            self.jumping = True
            self.gravity = 0.52

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
