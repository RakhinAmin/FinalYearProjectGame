import pygame
from pygame import Vector2

from screens.Game import Game
from utils.Button import Button
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class GameOver(Game):
    def __init__(self,score):
        self.buttons = []
        self.score = score
        utils.saveScore(score)

        self.buttons.append(Button(0, Vector2(280, 100), "GameOver", Vector2(3.5,2.5)))
        self.buttons.append(Button(3, Vector2(280, 500), "Quit", Vector2(3.5,2.5)))

        sounds.playMusic()

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    from screens.MainMenu import MainMenu
                    utils.currentScreen = MainMenu()
                    break
                if button.id == 3:
                    exit(1)

    def draw(self):
        utils.drawText(Vector2(100,100),"your score: " + str(self.score),(233,233,233),utils.font16)

    def drawUI(self):
        for button in self.buttons:
            button.draw()

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass


