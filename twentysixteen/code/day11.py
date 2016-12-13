import os
import re
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day11.txt')) as data_file:
        data = data_file.readlines()


class Solver(object):
    def __init__(self, data):
        self.data = data
        self.floors = None
        self.generators = None
        self.chips = None


class Test_Day11(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(INPUTS, 'day11.test.txt')) as data_file:
            self.data = data_file.readlines()

    def test_init_state(self):
        pass


if __name__ == '__main__':
    main()
