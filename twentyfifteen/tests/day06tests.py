import unittest

from day06 import LightGrid


class Test_LightGrid(unittest.TestCase):
    def test_counting(self):
        grid = LightGrid()
        grid.grid[0][0:5] = 1
        grid.count_lights()
        self.assertEqual(
            5,
            grid.on
        )

        grid = LightGrid()
        for y in grid.grid:
            y += 1
        grid.count_lights()
        self.assertEqual(
            1000000,
            grid.on
        )

        for y in grid.grid:
            y -= 1
        grid.count_lights()
        self.assertEqual(
            0,
            grid.on
        )

    def test_following_counting_instructions(self):
        grid = LightGrid()
        grid.run_line("turn on 0,0 through 999,999")
        self.assertEqual(
            1000000,
            grid.on
        )

        grid.run_line("turn off 499,499 through 500,500")
        self.assertEqual(
            999996,
            grid.on
        )

        grid.run_line("toggle 0,0 through 999,0")
        self.assertEqual(
            998996,
            grid.on
        )

        grid.run_line("toggle 0,0 through 999,0")
        self.assertEqual(
            999996,
            grid.on
        )

    def test_following_brightness_instructions(self):
        grid = LightGrid()
        grid.run_brightness("turn on 0,0 through 0,0")
        self.assertEqual(
            1,
            grid.brightness
        )

        grid.run_brightness("toggle 0,0 through 999,999")
        self.assertEqual(
            2000001,
            grid.brightness
        )

        grid.run_brightness("turn off 0,0 through 999,999")
        self.assertEqual(
            1000001,
            grid.brightness
        )
        grid.run_brightness("turn off 0,0 through 999,999")
        self.assertEqual(
            1,
            grid.brightness
        )
        grid.run_brightness("turn off 0,0 through 999,999")
        self.assertEqual(
            0,
            grid.brightness
        )

        grid.run_brightness("toggle 0,0 through 999,999")
        self.assertEqual(
            2000000,
            grid.brightness
        )
