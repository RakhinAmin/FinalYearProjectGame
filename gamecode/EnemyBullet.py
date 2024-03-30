from pygame import Vector2

from Game.GameObject import GameObject
from utils.assets_manager import assetsManager
from utils.util import utils


class EnemyBullet(GameObject):
    def __init__(self, pos, dirX):
        super().__init__(pos, assetsManager.get("enemyBullet"))
        self.cDestroyTime = 0
        self.vel = Vector2(dirX, 0) * 10

    def update(self):
        self.pos += self.vel

        self.cDestroyTime += utils.deltaTime()
        if self.cDestroyTime > 5:
            self.destroyFlag = True
