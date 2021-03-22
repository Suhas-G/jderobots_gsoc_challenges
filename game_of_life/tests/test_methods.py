import unittest

from game_of_life import GameOfLife


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.game = GameOfLife(10, 10)

    def test_set_alive(self):
        self.game.set_alive((0, 0))

        self.assertTrue(self.game.state[0][0])
        self.assertIn((0, 0), self.game.living_cells)

    def test_set_dead(self):
        self.game.set_alive((0, 0))
        self.assertTrue(self.game.state[0][0])
        self.assertIn((0, 0), self.game.living_cells)

        self.game.set_dead((0, 0))
        self.assertFalse(self.game.state[0][0])
        self.assertNotIn((0, 0), self.game.living_cells)

    def test_get_neighbours(self):
        neighbours = self.game.get_neighbours((0, 0))
        self.assertSetEqual(neighbours, set([(0, 1), (1, 0), (1, 1)]))

        neighbours = self.game.get_neighbours((0, 5))
        self.assertSetEqual(neighbours, set(
            [(0, 6), (0, 4), (1, 4), (1, 5), (1, 6)]))

        neighbours = self.game.get_neighbours((5, 0))
        self.assertSetEqual(neighbours, set(
            [(5, 1), (4, 0), (4, 1), (6, 0), (6, 1)]))

        neighbours = self.game.get_neighbours((5, 5))
        self.assertSetEqual(neighbours, set(
            [(5, 6), (5, 4), (4, 4), (4, 5), (4, 6), (6, 4), (6, 5), (6, 6)]))

    def test_life_over(self):
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 0))
        self.game.set_alive((2, 0))

        self.game.update()

        self.assertEqual(len(self.game.living_cells), 2)
        self.assertIn((1, 0), self.game.living_cells)
        self.assertIn((1, 1), self.game.living_cells)

        self.game.update()

        self.assertTrue(self.game.life_over())

    def test_update(self):
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 0))
        self.game.set_alive((2, 0))

        self.game.update()

        self.assertEqual(len(self.game.living_cells), 2)
        self.assertIn((1, 0), self.game.living_cells)
        self.assertIn((1, 1), self.game.living_cells)

    def test_reset(self):
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 1))
        self.game.set_alive((2, 1))

        self.game.update()

        self.assertEqual(len(self.game.living_cells), 3)
        self.assertSetEqual(
            set([(1, 0), (1, 1), (1, 2)]), self.game.living_cells)

        self.game.reset()
        self.assertEqual(len(self.game.living_cells), 0)
        self.assertFalse(any(any(row) for row in self.game.state))


if __name__ == '__main__':
    unittest.main()
