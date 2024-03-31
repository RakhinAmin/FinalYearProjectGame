from __future__ import annotations


import sys
import pygame
from pygame import Vector2

from utils.util import utils

from utils.Button import Button
from utils.sounds import sounds

from screens.Game import Game
from screens.GameOver import GameOver
from utils.assets_manager import assetsManager

class HighScores(Game):
    def __init__(self,word = "WORD"):
        self.gameObjects = []

        self.buttons = []
        self.buttons.append(Button(0, Vector2(utils.width - 150, utils.height - 60), "Menu", Vector2(1.8, 1.2),utils.font16))
        self.scores = utils.loadScores()
        self.scores = self.scores[0:7]

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    from screens.MainMenu import MainMenu
                    utils.currentScreen = MainMenu()
                    break
                if button.id == 3:
                    exit(1)

    def drawUI(self):
        for button in self.buttons:
            button.draw()
    def draw(self):
        utils.screen.fill((233, 233, 233), (0, 0, utils.width, utils.height))

        utils.drawText(Vector2(40, 10), "Top 7 high scores", (23, 233, 233), utils.font16)

        y = 40
        x = 50
        i = 1
        for score in self.scores:
            pygame.draw.rect(utils.display,(233,233,233),   (x - 10,y - 5,  150   ,20),1)
            pygame.draw.rect(utils.display, (233, 233, 233), (x - 10, y - 5, 50, 20), 1)

            utils.drawText(Vector2(x + 15, y), str(i) , (233, 233, 233), utils.font8)
            utils.drawText(Vector2(x + 80, y), str(score), (233, 233, 233), utils.font8)
            y += 22
            i += 1

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass

    def onMouseWheel(self, event):
        pass

