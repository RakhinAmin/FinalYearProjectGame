import pygame.rect
from pygame.math import Vector2
from utils.util import utils  # importing the utils module

# Importing the Enum class from the enum module.
from enum import Enum

# Definition of the GameObject class.


class GameObject:

    # Constructor for the GameObject class.
    def __init__(self, pos, img, visible=True):
        # Initial position of the object (Vector2 is a 2D vector class from Pygame).
        self.pos = pos
        # Image/sprite representing the object.
        self.img = img
        # Velocity vector (initially set to zero).
        self.vel = Vector2(0, 0)
        # Acceleration vector (initially set to zero).
        self.acc = Vector2(0, 0)
        # Visibility state of the object (visible by default).
        self.visible = visible

        # Flag to indicate if the object should be destroyed.
        self.destroyFlag = False
        # Flag to indicate if the image should be flipped horizontally.
        self.flipX = False
        # Health of the object (-1 indicates possibly unlimited or undefined health).
        self.health = -1
        # Damage the object can inflict (-1 indicates possibly no damage or undefined).
        self.damage = -1
        # Placeholder for a health bar object (if any).
        self.healthBar = None

    # Method to update the object's state.
    def update(self):
        # Update velocity by adding acceleration.
        self.vel += self.acc
        # Update position by adding velocity.
        self.pos += self.vel
        # Reset acceleration after applying it.
        self.acc = Vector2(0, 0)

    # Method to apply a force (acceleration) to the object.
    def applyForce(self, f):
        # Add the force vector to the object's acceleration.
        self.acc += f

    # Method to handle the object being hit by another object.
    def hit(self, obj):
        # Decrease health by the damage inflicted by the other object.
        self.health -= obj.damage
        # Set destroy flag if health drops to 0 or below.
        if self.health <= 0:
            self.destroyFlag = True

    # Method to draw the object on the screen.
    def draw(self):
        # Don't draw if the object is not visible.
        if not self.visible:
            return

        # Flip the image horizontally if needed.
        if self.flipX:
            self.img = pygame.transform.flip(self.img, True, False)

        # Draw the image at the object's current position.
        utils.screen.blit(self.img, (self.pos.x, self.pos.y))

    # Method to get the player objects rendering image.
    def getRect(self):
        # Create and return a pygame.Rect object based on the object's position and image dimensions.
        return pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    # Method to set the object's position.
    def setPos(self, pos):
        self.pos = pos

    # Method to get the object's current position.
    def getPos(self):
        return self.pos

    # Method to get the center position of the object.
    def getCenter(self):
        # Calculate and return the center point based on the object's position and dimensions.
        return Vector2(self.pos.x + self.getRect().w / 2, self.pos.y + self.getRect().h / 2)
