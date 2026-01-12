import json
import os
import random
import unittest

import life


class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [1, 1, 0, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1],
        ]
        self.life = life.GameOfLife((6, 8))
        self.life.curr_generation = self.grid

    def test_can_create_an_empty_grid(self):
        game = life.GameOfLife((3, 3), randomize=False)
        grid = game.create_grid(randomize=False)
        expected = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(grid, expected)

    def test_can_create_a_random_grid(self):
        game = life.GameOfLife((3, 3), randomize=True)
        grid_random_true = game.create_grid(randomize=True)
        grid_random_false = game.create_grid(randomize=False)
        self.assertNotEqual(grid_random_true, grid_random_false)

    def test_get_neighbours(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((1, 1))
        self.assertEqual(sum(neighbours), 8)

    def test_get_neighbours_for_upper_left_corner(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((0, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_right_corner(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((0, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_left_corner(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((2, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_right_corner(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((2, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_side(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((0, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_bottom_side(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((2, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_left_side(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((1, 0))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_right_side(self):
        game = life.GameOfLife((3, 3), randomize=False)
        game.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = game.get_neighbours((1, 2))
        self.assertEqual(sum(neighbours), 5)

    def test_can_update(self):
        game = life.GameOfLife((5, 5), randomize=False)
        game.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        game.step()
        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(game.curr_generation, expected)

    def test_is_changing(self):
        game = life.GameOfLife((5, 5), randomize=False)
        game.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        game.step()
        self.assertTrue(game.is_changing)

    def test_is_not_changing(self):
        """Тестирует, что стабильная фигура не изменяется"""
        game = life.GameOfLife((4, 4), randomize=False)
        # Квадрат 2x2 - стабильная фигура
        stable_grid = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ]
        game.curr_generation = [row[:] for row in stable_grid]
        game.step()
        # Стабильная фигура не должна измениться
        self.assertEqual(game.curr_generation, stable_grid)
        # После шага is_changing должно быть False
        self.assertFalse(game.is_changing)

    def test_is_max_generations_exceed(self):
        max_generations = 10
        game = life.GameOfLife((3, 3), max_generations=max_generations)
        for _ in range(max_generations):
            game.step()
        self.assertTrue(game.is_max_generations_exceeded)

    def test_prev_generation_is_correct(self):
        game = life.GameOfLife((5, 5), randomize=False)
        initial_grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        game.curr_generation = initial_grid
        game.step()
        self.assertEqual(game.prev_generation, initial_grid)
