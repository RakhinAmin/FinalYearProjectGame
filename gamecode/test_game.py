import unittest
import pygame


class TestSoldier(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_player_initialization(self):
        player = Soldier(30, 30, 20, 20, (255, 0, 0))
        self.assertEqual(player.rect.x, 30)
        self.assertEqual(player.rect.y, 30)
        self.assertEqual(player.rect.width, 20)
        self.assertEqual(player.rect.height, 20)
        self.assertEqual(player.color, (255, 0, 0))
        self.assertFalse(player.move_right)
        self.assertFalse(player.move_left)
        self.assertEqual(player.y_direction, 0)
        self.assertEqual(player.air_time, 0)

    def test_player_movement(self):
        player = Soldier(30, 30, 20, 20, (255, 0, 0))
        player.handle_event(pygame.event.Event(
            pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
        player.update([])
        self.assertTrue(player.move_right)
        self.assertEqual(player.rect.x, 35)


if __name__ == '__main__':
    unittest.main()
