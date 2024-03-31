import pygame
from pygame import mixer

class Sounds:
    def __init__(self):
        mixer.init()
        self.ss = {
            'click': mixer.Sound("assets/clickBtn.wav"),
            'shot': mixer.Sound("assets/shot.wav"),
        }

    def playMusic(self):
        return
        mixer.music.load("assets/BossMain.wav")
        mixer.music.play(-1)

    def play(self, key):
        pygame.mixer.Sound.play(self.ss[key])


sounds = Sounds()
