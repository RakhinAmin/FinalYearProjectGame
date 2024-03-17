import pygame
from pygame import Vector2

# Importing necessary modules and classes.
from Game.GameObject import GameObject
from utils.assets_manager import assetsManager

# BulletKit class, a type of GameObject for the shootable bullet


class BulletKit(GameObject):
    # Constructor for the BulletKit class.
    def __init__(self, pos):
        # Call the constructor of the base class (GameObject) with the position and the image from the assets manager.
        super().__init__(pos, assetsManager.get("bulletKit"))
        # Initialize whether the BulletKit is on the ground.
        self.onGround = False
        # Store the previous position, the same as the current position.
        self.prevPos = pos

    # Update method called every frame.
    def update(self):
        # Update the previous position to the current position at the start of each frame.
        self.prevPos = Vector2(self.pos.x, self.pos.y)
        # Call the update method of the base class to handle position and movement.
        super().update()
        # Apply gravity to the Bullet if it's not on the ground.
        if not self.onGround:
            # Apply a downward force to simulate gravity (gravity drop on bullet with distance)
            self.applyForce(Vector2(0, 0.52))
