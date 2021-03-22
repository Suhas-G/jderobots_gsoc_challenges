import unittest

from game_of_life import GameOfLife


class ShapeTest(unittest.TestCase):
    '''Test for various transitions
    Taken from http://pi.math.cornell.edu/~lipa/mec/lesson6.html
    '''

    def setUp(self):
        self.game = GameOfLife(10, 10)

    def test_triomino_1(self):
        '''Test for following transition
        □             □
        □ => □ □ □ => □ => so on
        □             □
        '''
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 1))
        self.game.set_alive((2, 1))

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 3)
        self.assertSetEqual(
            set([(1, 0), (1, 1), (1, 2)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 3)
        self.assertSetEqual(
            set([(0, 1), (1, 1), (2, 1)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 3)
        self.assertSetEqual(
            set([(1, 0), (1, 1), (1, 2)]), self.game.living_cells)

    def test_triomino_2(self):
        '''Test for following transitions
          □
         □   => □ => Nothing
        □
        '''
        self.game.set_alive((0, 2))
        self.game.set_alive((1, 1))
        self.game.set_alive((2, 0))

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 1)
        self.assertSetEqual(set([(1, 1)]), self.game.living_cells)

        self.game.update()
        self.assertTrue(self.game.life_over())

    def test_tetromino_1(self):
        '''Test for following transitions
        □ □  => □ □ => Stable
        □ □     □ □
        '''
        self.game.set_alive((0, 0))
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 0))
        self.game.set_alive((1, 1))

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 4)
        self.assertSetEqual(
            set([(0, 0), (0, 1), (1, 0), (1, 1)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 4)
        self.assertSetEqual(
            set([(0, 0), (0, 1), (1, 0), (1, 1)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 4)
        self.assertSetEqual(
            set([(0, 0), (0, 1), (1, 0), (1, 1)]), self.game.living_cells)

    def test_tetromino_2(self):
        '''Test for following transitions
        □               □
        □ => □ □ □ => □   □ => stable
        □    □ □ □    □   □
        □               □
        '''
        self.game.set_alive((0, 1))
        self.game.set_alive((1, 1))
        self.game.set_alive((2, 1))
        self.game.set_alive((3, 1))

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 6)
        self.assertSetEqual(
            set([(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 6)
        self.assertSetEqual(
            set([(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)]), self.game.living_cells)

        self.game.update()
        self.assertEqual(len(self.game.living_cells), 6)
        self.assertSetEqual(
            set([(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)]), self.game.living_cells)


if __name__ == '__main__':
    print('Testing different configurations...')
    unittest.main()
