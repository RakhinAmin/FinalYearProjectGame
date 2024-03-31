import pygame
from pygame.math import Vector2

# Importing necessary modules and classes for gameobject, assets and util
from Game.GameObject import GameObject
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils

# Player class, which is a type of GameObject.


class Player(GameObject):
    # Constructor for the Player class.
    def __init__(self, pos):
        # Initialize the base class with the position and no initial image.
        super().__init__(pos, None)
        # Speed at which the player moves.
        self.speed = 5
        # Flag to check if the player is jumping.
        self.jumping = False

        # Dictionary to hold the different sprite sheets for different player animation states.
        self.sheets = {
            'idle': SpriteSheet(assetsManager.get("player-idle"), 1, 5),
            'run': SpriteSheet(assetsManager.get("player-run"), 1, 6),
            'jump': SpriteSheet(assetsManager.get("player-jump"), 1, 1),
        }

        # Setting up animations for each state by defining the frames and loop settings.
        self.sheets['idle'].setPlay(0, 4, 0.07, True)
        self.sheets['run'].setPlay(0, 5, 0.07, True)
        self.sheets['jump'].setPlay(0, 0, 0.07, True)

        # Initializing the current sheet to 'idle'.
        self.currentSheet = 'idle'
        # Setting the current image to the current frame of the current sheet.
        self.img = self.sheets[self.currentSheet].getCurrentFrame()
        # Getting the player's rectangle for collision and positioning.
        self.rect = self.getRect()

        # Initializing additional player properties.
        self.prevPos = None
        self.speed = 2
        self.jumping = True
        self.shootUp = False
        self.health = 10
        # Placeholder for a health bar, currently commented out.
        # self.healthBar = HealthBar(self.health, (23, 233, 233), self.getRect().w + 2)
        self.bullets = 0
        self.onGround = False
        self.gravity = 0.52

    # Update method to adjust the player's state and properties each frame.
    def update(self):
        # Apply gravity if the player is not on the ground.
        if not self.onGround:
            self.applyForce(pygame.Vector2(0, 0.52))

        # Update the player's previous position.
        self.prevPos = Vector2(self.pos.x, self.pos.y)

        # Update the current sheet based on the player's actions.
        if self.jumping:
            self.currentSheet = 'jump'
        elif self.vel.x != 0:
            self.currentSheet = 'run'
        else:
            self.currentSheet = 'idle'

        # Update the GameObject class.
        super().update()

        # Update the animation and current image.
        self.sheets[self.currentSheet].play()
        self.img = self.sheets[self.currentSheet].getCurrentFrame()

    # Draw method to render the player on the screen.
    def draw(self):
        # Call the draw method of the base class.
        super().draw()
        # Placeholder for drawing the health bar, currently commented out until further implemented
        # self.healthBar.draw(self.health, Vector2(self.getRect().x, self.getRect().y - 12))

    # Method to handle key press events.
    def onKeyDown(self, key):
        # Left movement.
        if key == pygame.K_a:
            if not self.flipX:
                self.pos.x -= 6

            self.flipX = True
            self.vel.x = -self.speed
            self.rect = self.getRect()

        # Right movement.
        elif key == pygame.K_d:
            if self.flipX:
                self.pos.x += 12

            self.flipX = False
            self.vel.x = self.speed
            self.rect = self.getRect()

        # Jumping mechanics.
        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.jumping = True

        # Shooting upwards.
        elif key == pygame.K_w:
            self.shootUp = True

        # Double jump (enhanced jump).
        if key == pygame.K_SPACE and not self.jumping:
            self.applyForce(pygame.Vector2(0, -12))
            self.applyForce(pygame.Vector2(0, -7))
            self.jumping = True
            self.gravity = 0.52

    # Method to handle key release events.
    def onKeyUp(self, key):
        # Stop horizontal movement when the up movement key is released.
        if key == pygame.K_a and self.vel.x == -self.speed:
            self.vel.x = 0
        elif key == pygame.K_d and self.vel.x == self.speed:
            self.vel.x = 0

    # Method to get the player's rectangle, adjusting based on the flip state.
    def getRect(self):
        if self.flipX:
            return pygame.rect.Rect(self.pos.x + 12, self.pos.y, self.img.get_width() - 18, self.img.get_height())
        else:
            return pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width() - 12, self.img.get_height())
