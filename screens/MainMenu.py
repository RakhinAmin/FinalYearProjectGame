import pygame
from pygame import Vector2

from screens.Game import Game
from screens.HighScores import HighScores
from screens.MainGame import MainGame
from utils.Button import Button
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class MainMenu(Game):
    def __init__(self):
        self.buttons = []

        self.buttons.append(Button(0, Vector2(280, 200),"Start",Vector2(3.5,2.5)))
        self.buttons.append(Button(1, Vector2(280, 300), "HighScores", Vector2(3.5,2.5)))
        self.buttons.append(Button(3, Vector2(280, 400), "Quit", Vector2(3.5,2.5)))

        sounds.playMusic()

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    utils.currentScreen = MainGame()
                    break
                if button.id == 1:
                    utils.currentScreen = HighScores()
                    break
                if button.id == 3:
                    exit(1)

    def draw(self):
        pass

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


