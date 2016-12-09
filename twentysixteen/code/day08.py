import os
import unittest

import numpy as np

from twentysixteen import INPUTS

ROW = 0
COLUMN = 1


def main():
    with open(os.path.join(INPUTS, 'day08.txt'), 'r') as data_file:
        data = data_file.readlines()

    screen = Screen((6, 50))

    screen.execute_instructions(data)

    print("The number of lit pixels is: {}".format(screen.sum))
    print("Here's what the screen is trying to display:")
    screen.print_screen()


class Screen(object):
    def __init__(self, dimensions):
        self.screen = np.zeros(dimensions, int)

    @property
    def sum(self):
        return sum(self.screen.flat)

    def execute_instructions(self, data):
        parsed_data = [line.split() for line in data]
        for line in parsed_data:
            if line[0] == 'rect':
                dimensions = [int(num) for num in line[1].split('x')]
                self.draw_rect(dimensions)
            else:
                index = int(line[2].split('=')[1])
                by = int(line[4])
                if line[1] == 'column':
                    self.rotate_column(index, by)
                else:
                    self.rotate_row(index, by)

    def draw_rect(self, dimensions):
        column = dimensions[0]
        row = dimensions[1]
        self.screen[0:row, 0:column] = 1

    def rotate(self, axis, index, by):
        temp = self.screen.take(index, axis)
        return np.append(temp[-by:], temp[:-by])

    def rotate_column(self, index, by):
        self.screen[..., index] = self.rotate(COLUMN, index, by)

    def rotate_row(self, index, by):
        self.screen[index] = self.rotate(ROW, index, by)

    def print_screen(self):
        for row in self.screen:
            print(str(row).strip('[]').replace('\n', '').replace('1', '*').replace('0', ' '))


class Test_Day08(unittest.TestCase):
    def setUp(self):
        self.test_screen = Screen((3, 7))

    def test_rect(self):
        self.test_screen.draw_rect([3, 2])
        self.assertEqual(6, self.test_screen.sum)

    def test_rotate_column_once(self):
        expected_row_0 = np.array([1, 0, 1, 0, 0, 0, 0], int)
        expected_row_1 = np.array([1, 1, 1, 0, 0, 0, 0], int)
        expected_row_2 = np.array([0, 1, 0, 0, 0, 0, 0], int)

        self.test_screen.draw_rect([3, 2])
        self.test_screen.rotate_column(1, 1)

        self.assertTrue(all(self.test_screen.screen[0] == expected_row_0),
                        str(self.test_screen.screen[0] == expected_row_0))
        self.assertTrue(all(self.test_screen.screen[1] == expected_row_1),
                        str(self.test_screen.screen[1] == expected_row_1))
        self.assertTrue(all(self.test_screen.screen[2] == expected_row_2),
                        str(self.test_screen.screen[2] == expected_row_2))

    def test_rotate_row(self):
        expected_row_0 = np.array([0, 0, 0, 0, 1, 0, 1], int)
        expected_row_1 = np.array([1, 1, 1, 0, 0, 0, 0], int)
        expected_row_2 = np.array([0, 1, 0, 0, 0, 0, 0], int)

        self.test_screen.draw_rect([3, 2])
        self.test_screen.rotate_column(1, 1)
        self.test_screen.rotate_row(0, 4)

        self.assertTrue(all(self.test_screen.screen[0] == expected_row_0),
                        str(self.test_screen.screen[0] == expected_row_0))
        self.assertTrue(all(self.test_screen.screen[1] == expected_row_1),
                        str(self.test_screen.screen[1] == expected_row_1))
        self.assertTrue(all(self.test_screen.screen[2] == expected_row_2),
                        str(self.test_screen.screen[2] == expected_row_2))

    def test_rotate_column_twice(self):
        expected_row_0 = np.array([0, 1, 0, 0, 1, 0, 1], int)
        expected_row_1 = np.array([1, 0, 1, 0, 0, 0, 0], int)
        expected_row_2 = np.array([0, 1, 0, 0, 0, 0, 0], int)

        self.test_screen.draw_rect([3, 2])
        self.test_screen.rotate_column(1, 1)
        self.test_screen.rotate_row(0, 4)
        self.test_screen.rotate_column(1, 1)

        self.assertTrue(all(self.test_screen.screen[0] == expected_row_0),
                        str(self.test_screen.screen[0] == expected_row_0))
        self.assertTrue(all(self.test_screen.screen[1] == expected_row_1),
                        str(self.test_screen.screen[1] == expected_row_1))
        self.assertTrue(all(self.test_screen.screen[2] == expected_row_2),
                        str(self.test_screen.screen[2] == expected_row_2))


if __name__ == '__main__':
    main()
