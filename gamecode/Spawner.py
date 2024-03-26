import random

from pygame import Vector2

from Game.BulletKit import BulletKit
from Game.Enemy import Enemy
from Game.HealthKit import HealthKit
from utils.util import utils


class Spawner:
    def __init__(self,addObjectCallback,player):
        self.addObjectCallback = addObjectCallback
        self.player = player

        self.healthKitTime = 50
        self.bulletKitTime = 35

        self.enemyTime = 20

    def spawn(self):
        self.spawnItems()
        self.spawnEnemy()

    def spawnEnemy(self):
        self.enemyTime += utils.deltaTime()
        if self.enemyTime >= 10:
            self.enemyTime = 0
            self.addObjectCallback(Enemy(Vector2(self.player.pos.x + random.randint(210,270),-100),self.addObjectCallback))

    def spawnItems(self):
        self.healthKitTime += utils.deltaTime()
        if self.healthKitTime >= 100:
            self.healthKitTime = 0
            self.addObjectCallback(HealthKit(Vector2(self.player.pos.x + 200,-100)))

        self.bulletKitTime += utils.deltaTime()
        if self.bulletKitTime >= 40:
            self.bulletKitTime = 0
            self.addObjectCallback(BulletKit(Vector2(self.player.pos.x + 200, -100)))

