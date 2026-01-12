import json
import os
import random
import unittest
from unittest.mock import MagicMock

import life_proto


life_proto.pygame.display = MagicMock()


class TestGameOfLife(unittest.TestCase):
    """Тесты для прототипа игры 'Жизнь'"""

    def setUp(self):
        self.game = life_proto.GameOfLife(100, 100, 20)

    def test_can_create_an_empty_grid(self):
        grid = self.game.create_grid(randomize=False)
        for row in grid:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_can_create_a_random_grid(self):
        grid = self.game.create_grid(randomize=True)
        has_live_cell = False
        for row in grid:
            for cell in row:
                if cell == 1:
                    has_live_cell = True
                    break
        self.assertTrue(has_live_cell)

    def test_get_neighbours(self):
        game = life_proto.GameOfLife(30, 30, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((1, 1))
        self.assertEqual(sum(neighbours), 8)

    def test_get_neighbours_for_upper_left_corner(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((0, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_right_corner(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((0, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_left_corner(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((2, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_right_corner(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((2, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_side(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((0, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_bottom_side(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((2, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_left_side(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((1, 0))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_right_side(self):
        game = life_proto.GameOfLife(3, 3, 10)
        game.grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        neighbours = game.get_neighbours((1, 2))
        self.assertEqual(sum(neighbours), 5)

    def test_can_update(self):
        game = life_proto.GameOfLife(50, 50, 10)
        game.grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        game.grid = game.get_next_generation()
        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(game.grid, expected)
