import random
import sys

import pygame
from pygame import Vector2

from Game.Bg import Bg
from Game.BulletKit import BulletKit
from Game.Enemy import Enemy
from Game.EnemyBullet import EnemyBullet
from Game.Explosion import Explosion
from Game.HealthKit import HealthKit
from Game.Map import Map
from Game.Player import Player
from Game.PlayerBullet import PlayerBullet
from Game.Spawner import Spawner
from screens.Game import Game
from screens.GameOver import GameOver
from utils.assets_manager import assetsManager
from utils.util import utils


class MainGame(Game):
    def __init__(self):
        self.objects = []
        self.map = Map()
        self.bg = Bg()
        self.player = Player(Vector2(300/2, 70), self.objects.append)
        self.spawner = Spawner(self.objects.append, self.player)
        self.score = 0

    def update(self):

        # addedObjects = []
        #
        self.map.update(self.player)

        self.player.update()
        self.map.collidePlayer(self.player)

        self.spawner.spawn()

        addedObjects = []
        for obj in self.objects:
            obj.update()

            if isinstance(obj, Enemy):
                if obj.pos.x < self.player.pos.x - 200:
                    obj.destroyFlag = True
                    continue

            if utils.collide(obj, self.player):
                if isinstance(obj, HealthKit):
                    obj.destroyFlag = True
                    self.player.health = 10
                    self.score += random.randint(1, 5)

                elif isinstance(obj, BulletKit):
                    obj.destroyFlag = True
                    self.player.bullets = 30
                    self.score += random.randint(1, 5)

                elif isinstance(obj, EnemyBullet):
                    obj.destroyFlag = True
                    addedObjects.append(
                        Explosion(Vector2(obj.pos.x - 24, obj.pos.y - 24)))
                    self.player.health -= 1
                    if self.player.health <= 0:
                        utils.currentScreen = GameOver(self.score)
                        return

            if isinstance(obj, HealthKit) or isinstance(obj, BulletKit) or isinstance(obj, Enemy):
                for tile in self.map.tile_rects:
                    if utils.collide_rect(tile, obj.getRect()):
                        obj.vel.y = 0
                        obj.pos.y = obj.prevPos.y
                        obj.onGround = True
                continue

            if isinstance(obj, PlayerBullet) or isinstance(obj, EnemyBullet):
                for tile in self.map.tile_rects:
                    if utils.collide_rect(tile, obj.getRect()):
                        obj.destroyFlag = True
                        addedObjects.append(
                            Explosion(Vector2(obj.pos.x - 24, obj.pos.y - 24)))
                        continue
            if isinstance(obj, PlayerBullet):
                for otherObj in self.objects:
                    if isinstance(otherObj, Enemy) and utils.collide(obj, otherObj):
                        addedObjects.append(
                            Explosion(Vector2(obj.pos.x - 24, obj.pos.y - 24)))
                        otherObj.health -= 1
                        obj.destroyFlag = True
                        if otherObj.health <= 0:
                            otherObj.destroyFlag = True
                            self.score += random.randint(1, 5)

        self.objects += addedObjects

        # destroy objects
        for obj in self.objects:
            if obj.destroyFlag:
                self.objects.remove(obj)

        self.map.tile_rects = []

    def draw(self):
        # self.map.resetTiles()
        self.bg.draw()
        self.map.draw()
        self.player.draw()
        for obj in self.objects:
            obj.draw()

        utils.drawText(Vector2(35, 17), str(self.score),
                       (233, 233, 233), utils.font6)

        # draw ui

    def onKeyDown(self, key):
        self.player.onKeyDown(key)

    def onKeyUp(self, key):
        self.player.onKeyUp(key)

    def onMouseDown(self, event):
        self.player.shoot()

    def onMouseUp(self, event):
        pass

    def onMouseWheel(self, event):
        pass
