import pygame
from pygame import Vector2

from Game.GameObject import GameObject
from utils.assets_manager import assetsManager


class BulletKit(GameObject):
    def __init__(self,pos):
        super().__init__(pos,assetsManager.get("bulletKit"))
        self.onGround = False
        self.prevPos = pos

    def update(self):
        self.prevPos = Vector2(self.pos.x,self.pos.y)
        super().update()
        if not self.onGround:
            self.applyForce(Vector2(0,0.52))