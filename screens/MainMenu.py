import pygame
from pygame import Vector2

from screens.Game import Game
from screens.HighScores import HighScores
from screens.MainGame import MainGame
# Import the Controls screen if you have one
# from screens.Controls import Controls
from utils.Button import Button
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils


class MainMenu(Game):
    def __init__(self):
        self.buttons = []

        # Existing buttons
        self.buttons.append(Button(0, Vector2(280, 200),
                            "Start", Vector2(3.5, 2.5)))
        self.buttons.append(Button(1, Vector2(280, 300),
                            "HighScores", Vector2(3.5, 2.5)))
        self.buttons.append(
            Button(3, Vector2(280, 400), "Quit", Vector2(3.5, 2.5)))

        # Adding the Controls button
        self.buttons.append(Button(2, Vector2(280, 350),
                            "Controls", Vector2(3.5, 2.5)))

        sounds.playMusic()

    def update(self):
        for button in self.buttons:
            if button.clicked:
                if button.id == 0:
                    utils.currentScreen = MainGame()
                    break
                elif button.id == 1:
                    utils.currentScreen = HighScores()
                    break
                # elif button.id == 2:
                    # Logic when the Controls button is clicked
                    # Replace 'Controls()' with the appropriate screen or function
                    # utils.currentScreen = Controls()
                    # break
                elif button.id == 3:
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
