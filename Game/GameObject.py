import pygame.rect
from pygame.math import Vector2
from utils.util import utils


class GameObject:
    # Initialize the GameObject with position, image, and visibility attributes.
    def __init__(self, pos, img, visible=True):
        # The position of the object (Vector2 for x, y coordinates).
        self.pos = pos
        self.img = img  # The image/sprite associated with the object.
        # The velocity of the object (initially set to 0).
        self.vel = Vector2(0, 0)
        # The acceleration of the object (initially set to 0).
        self.acc = Vector2(0, 0)
        # Visibility flag, determines if the object should be drawn.
        self.visible = visible

        # Additional attributes for managing object state.
        # Flag indicating if the object should be destroyed.
        self.destroyFlag = False
        # Flag indicating if the image should be flipped horizontally.
        self.flipX = False
        self.health = -1
        self.damage = -1
        # Optional attribute for a health bar, if needed.
        self.healthBar = None

    # Update the object's position based on its velocity and acceleration.
    def update(self):
        # Update velocity by adding acceleration.
        self.vel = Vector2(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        # Update position by adding velocity.
        self.pos = Vector2(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        # Reset acceleration after applying it to the velocity.
        self.acc = Vector2(0, 0)

    # Method to apply a force (acceleration) to the object.
    def applyForce(self, f):
        # Add the force vector to the object's acceleration.
        self.acc = Vector2(self.acc.x + f.x, self.acc.y + f.y)

    # Method to handle the object being hit by another object.
    def hit(self, obj):
        # Subtract damage from health.
        self.health -= obj.damage
        # Set the destroy flag if health drops to 0 or below.
        if self.health <= 0:
            self.destroyFlag = True

    # Draw the object on the screen if it is visible.
    def draw(self):
        # Return immediately if the object is not visible.
        if not self.visible:
            return

        # Flip the image horizontally if flipX is true.
        if self.flipX:
            self.img = pygame.transform.flip(self.img, True, False)

        # Calculate the adjusted y-coordinate based on scrolling.
        adjusted_y = self.getRect().y - utils.scroll[1]
        # Draw the image at the adjusted position.
        utils.display.blit(
            self.img, (self.pos.x - utils.scroll[0], adjusted_y))

    # Get the Pygame rect object for the GameObject.
    def getRect(self):
        # Create and return a new rect with the object's position and image dimensions.
        return pygame.rect.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    # Set the position of the GameObject.
    def setPos(self, pos):
        self.pos = pos

    # Get the position of the GameObject.
    def getPos(self):
        return self.pos

    # Get the center position of the GameObject.
    def getCenter(self):
        # Calculate and return the center point of the object.
        return Vector2(self.pos.x + self.getRect().w / 2, self.pos.y + self.getRect().h / 2)
