import os
import unittest

from twentysixteen import INPUTS

PROTOTYPE_BUTTONS = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']
]

REAL_BUTTONS = [
    [None, None, '1', None, None],
    [None, '2', '3', '4', None],
    ['5', '6', '7', '8', '9'],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None]
]

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

OPPOSITES = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}


def main():
    with open(os.path.join(INPUTS, 'day02.txt')) as data_file:
        data = data_file.readlines()
    combo_finder = ComboFinder(data, PROTOTYPE_BUTTONS)
    combo_finder.find()

    print("The bathroom combo for the imagined keypad is: {}".format(combo_finder.combo))

    real_combo_finder = ComboFinder(data, REAL_BUTTONS, start=(2, 0))
    real_combo_finder.find()

    print("The bathroom combo for the real keypad is: {}".format(real_combo_finder.combo))


class ComboFinder(object):
    def __init__(self, data, buttons, start=(1, 1)):
        self.data = data
        self.row = start[0]
        self.column = start[1]
        self.results = []
        self.buttons = buttons

    @property
    def combo(self):
        return ''.join(self.results)

    def find(self):
        for row in self.data:
            self.move(row)

    def move(self, data_row):
        for direction in data_row:
            self.move_once(direction)

        self.results.append(self.buttons[self.row][self.column])

    def move_once(self, direction):
        if direction is UP:
            self.row -= 1
        elif direction is DOWN:
            self.row += 1
        elif direction is LEFT:
            self.column -= 1
        elif direction is RIGHT:
            self.column += 1
        self.get_current_position(direction)

    def get_current_position(self, direction):
        if self.row < 0:
            self.row += 1
        elif self.row > len(self.buttons) - 1:
            self.row -= 1

        if self.column < 0:
            self.column += 1
        elif self.column > len(self.buttons[0]) - 1:
            self.column -= 1

        button = self.buttons[self.row][self.column]
        if button is None:
            self.move_once(OPPOSITES[direction])


class Test_Day02(unittest.TestCase):
    def test_up_from_center(self):
        data = ['U']
        combo_finder = ComboFinder(data, PROTOTYPE_BUTTONS)
        combo_finder.find()

        expected_position = (0, 1)
        actual_position = (combo_finder.row, combo_finder.column)

        self.assertEqual(expected_position, actual_position)

    def test_up_from_top(self):
        data = ['U']
        combo_finder = ComboFinder(data, PROTOTYPE_BUTTONS)
        combo_finder.position = (0, 1)
        combo_finder.find()

        expected_position = (0, 1)
        actual_position = (combo_finder.row, combo_finder.column)

        self.assertEqual(expected_position, actual_position)

    def test_find_prototype_combination(self):
        test_data = ['ULL', 'RRDDD', 'LURDL', 'UUUUD']
        expected_output = '1985'

        combo_finder = ComboFinder(test_data, PROTOTYPE_BUTTONS)
        combo_finder.find()

        actual_output = combo_finder.combo

        self.assertEqual(expected_output, actual_output)

    def test_find_real_combination(self):
        test_data = ['ULL', 'RRDDD', 'LURDL', 'UUUUD']
        expected_output = '5DB3'

        combo_finder = ComboFinder(test_data, REAL_BUTTONS, start=(2, 0))
        combo_finder.find()

        actual_output = combo_finder.combo

        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    main()
