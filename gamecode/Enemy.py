import pygame
from pygame import Vector2

from Game.EnemyBullet import EnemyBullet
from Game.GameObject import GameObject
from Game.HealthBar import HealthBar
from utils.SpriteSheet import SpriteSheet
from utils.assets_manager import assetsManager
from utils.sounds import sounds
from utils.util import utils

# Enemy class, which is a type of GameObject for the enemy object


class Enemy(GameObject):
    # Constructor for the Enemy class.
    def __init__(self, pos, addObjectCallBack):
        # Initialize the base class with the position and no initial image.
        super().__init__(pos, None)
        # Flag to check if the enemy is on the ground.
        self.onGround = False
        # Record the initial position.
        self.prevPos = pos
        # Load and set up the sprite sheet for the enemy's idle animation.
        self.sheet = SpriteSheet(assetsManager.get("enemy-idle"), 1, 5)
        self.sheet.setPlay(0, 4, 0.07, True)
        # Get the current frame from the sprite sheet to display as the enemy's image.
        self.img = self.sheet.getCurrentFrame()
        # Callback function to add objects (like bullets) to the game.
        self.addObjectCallBack = addObjectCallBack

        # Initialize shooting timer and health.
        self.shootTime = 0
        self.health = 3
        # Set up a health bar for the enemy.
        self.healthBar = HealthBar(
            self.health, (233, 23, 23), self.getRect().w + 10)

    # Update method to adjust the enemy's state and properties each frame.
    def update(self):
        # Update the previous position.
        self.prevPos = Vector2(self.pos.x, self.pos.y)
        # Update based on the GameObject class.
        super().update()
        # Handle shooting behavior.
        self.shoot()
        # Update the animation.
        self.sheet.play()
        # Update the image to the current frame of the animation.
        self.img = self.sheet.getCurrentFrame()
        # Apply gravity if the enemy is not on the ground.
        if not self.onGround:
            self.applyForce(Vector2(0, 0.52))

    # Method to handle the enemy shooting.
    def shoot(self):
        # Update the shooting timer.
        self.shootTime += utils.deltaTime()
        # Check if it's time to shoot.
        if self.shootTime >= 1:
            self.shootTime = 0
            # Create a bullet and use the callback to add it to the game.
            bullet = EnemyBullet(
                Vector2(self.getRect().centerx - 8, self.getRect().centery - 4), -1)
            self.addObjectCallBack(bullet)
            # Play the shooting sound.
            sounds.play("shot")

    # Draw method to render the enemy on the screen.
    def draw(self):
        # Call the draw method of the base class.
        super().draw()
        # Draw the health bar above the enemy.
        self.healthBar.draw(self.health, Vector2(
            self.getRect().x - utils.scroll[0] - 2, self.getRect().y - 4 - utils.scroll[1]))

    # Method to get the enemy's rectangle for collision detection and other purposes.
    def getRect(self):
        # Adjust the rectangle for the enemy's position and size.
        return pygame.rect.Rect(self.pos.x + 12, self.pos.y, self.img.get_width() - 18, self.img.get_height())
