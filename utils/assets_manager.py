import pygame


class AssetsManager:
    def __init__(self):
        self.assets = {
            'button': pygame.image.load("assets/btn.png").convert_alpha(),
            'clickButton': pygame.image.load("assets/clickBtn.png").convert_alpha(),
            'player-idle': pygame.image.load("assets/player_idle.png").convert_alpha(),
            'player-jump': pygame.image.load("assets/player_jump.png").convert_alpha(),
            'player-run': pygame.image.load("assets/player_run.png").convert_alpha(),

            'playerBullet': pygame.image.load("assets/playerBullet.png").convert_alpha(),
            'enemyBullet': pygame.image.load("assets/enemyBullet.png").convert_alpha(),

            'bulletIcon': pygame.image.load("assets/bulletIcon.png").convert_alpha(),
            'explo1': pygame.image.load("assets/explo1.png").convert_alpha(),

            'healthKit': pygame.image.load("assets/healthKit.png").convert_alpha(),
            'bulletKit': pygame.image.load("assets/bulletKit.png").convert_alpha(),

            'enemy-idle': pygame.image.load("assets/enemy_idle.png").convert_alpha(),
        }

    def get(self, key):
        return self.assets[key]


assetsManager = AssetsManager()
