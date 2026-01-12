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
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((1, 1))
        self.assertEqual(sum(neighbours), 8)

    def test_get_neighbours_for_upper_left_corner(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((0, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_right_corner(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((0, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_left_corner(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((2, 0))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_lower_right_corner(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((2, 2))
        self.assertEqual(sum(neighbours), 3)

    def test_get_neighbours_for_upper_side(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((0, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_bottom_side(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((2, 1))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_left_side(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((1, 0))
        self.assertEqual(sum(neighbours), 5)

    def test_get_neighbours_for_right_side(self):
        self.life.curr_generation = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        neighbours = self.life.get_neighbours((1, 2))
        self.assertEqual(sum(neighbours), 5)

    def test_can_update(self):
        self.life.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.life.step()
        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.life.curr_generation, expected)

    def test_is_changing(self):
        self.life.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.life.step()
        self.assertTrue(self.life.is_changing)

    def test_is_not_changing(self):
        self.life.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.life.step()
        self.assertFalse(self.life.is_changing)

    def test_is_max_generations_exceed(self):
        max_generations = 10
        self.life = life.GameOfLife((3, 3), max_generations=max_generations)
        for _ in range(max_generations):
            self.life.step()
        self.assertTrue(self.life.is_max_generations_exceeded)

    def test_prev_generation_is_correct(self):
        self.life.curr_generation = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.life.step()
        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.life.prev_generation, expected)
