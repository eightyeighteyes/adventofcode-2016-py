import os
import unittest

from twentysixteen import INPUTS

NORTH = 2
EAST = 4
SOUTH = 8
WEST = 16


def main():
    with open(os.path.join(INPUTS, 'day01.txt'), 'r') as input_file:
        puzzle_input = input_file.read()

    print("The fake Easter Bunny HQ is {} blocks away.".format(find_ebhq(puzzle_input)))
    print("The real EBHQ is {} blocks away".format(find_real_hq(puzzle_input)))


def find_ebhq(puzzle_input):
    data = parse_input(puzzle_input)
    finder = Finder(data)
    finder.find()

    return finder.distance


def find_real_hq(puzzle_input):
    data = parse_input(puzzle_input)
    finder = Finder(data)
    finder.find()

    return finder.real_hq_distance


def parse_input(puzzle_input):
    data = puzzle_input.replace(' ', '').split(',')
    directions = []
    for d in data:
        directions.append({'direction': d[0], 'steps': int(d[1:])})

    return directions


class Finder(object):
    def __init__(self, data):
        self.data = data

        self.position = [0, 0]
        self.direction = NORTH

        self.visited = [list(self.position)]

    @property
    def distance(self):
        return abs(0 - self.position[0]) + abs(0 - self.position[1])

    @property
    def real_hq_position(self):
        return self.find_true_hq()

    @property
    def real_hq_distance(self):
        return abs(0 - self.real_hq_position[0]) + abs(0 - self.real_hq_position[1])

    def find_true_hq(self):
        dupes = {}
        for i, location in enumerate(self.visited):
            if location in self.visited[i + 1:]:
                dupes[i] = location

        return dupes[min(dupes.keys())]

    def find(self):
        for d in self.data:
            self.turn(d['direction'])
            self.walk(d['steps'])

    def turn(self, direction):
        if direction == 'R':
            if self.direction == WEST:
                self.direction = NORTH
            else:
                self.direction <<= 1
        elif direction == 'L':
            if self.direction == NORTH:
                self.direction = WEST
            else:
                self.direction >>= 1

    def walk(self, num_steps):
        if self.direction in [EAST, WEST]:
            axis = 0
        else:
            axis = 1

        if self.direction in [EAST, NORTH]:
            for _ in range(num_steps):
                self.position[axis] += 1
                self.visited.append(list(self.position))
        else:
            for _ in range(num_steps):
                self.position[axis] -= 1
                self.visited.append(list(self.position))


class Test_Finder(unittest.TestCase):
    def test_one_step_right(self):
        data = [{'direction': 'R', 'steps': 1}]
        finder = Finder(data)
        finder.find()

        self.assertEqual(EAST, finder.direction)
        self.assertEqual([1, 0], finder.position)
        self.assertEqual(1, finder.distance)

    def test_two_steps_right(self):
        data = [{'direction': 'R', 'steps': 2}]
        finder = Finder(data)
        finder.find()

        self.assertEqual([2, 0], finder.position)
        self.assertEqual(2, finder.distance)

    def test_one_step_left(self):
        data = [{'direction': 'L', 'steps': 1}]
        finder = Finder(data)
        finder.find()

        self.assertEqual([-1, 0], finder.position)
        self.assertEqual(1, finder.distance)

    def test_right_turns(self):
        finder = Finder([])
        self.assertEqual(NORTH, finder.direction)

        finder.turn('R')
        self.assertEqual(EAST, finder.direction)

        finder.turn('R')
        self.assertEqual(SOUTH, finder.direction)

        finder.turn('R')
        self.assertEqual(WEST, finder.direction)

        finder.turn('R')
        self.assertEqual(NORTH, finder.direction)

    def test_left_turns(self):
        finder = Finder([])
        self.assertEqual(NORTH, finder.direction)

        finder.turn('L')
        self.assertEqual(WEST, finder.direction)

        finder.turn('L')
        self.assertEqual(SOUTH, finder.direction)

        finder.turn('L')
        self.assertEqual(EAST, finder.direction)

        finder.turn('L')
        self.assertEqual(NORTH, finder.direction)

    def test_something_complicated(self):
        data = parse_input('L5, R2, R10, L1')
        finder = Finder(data)
        finder.find()

        self.assertEqual([5, 3], finder.position)
        self.assertEqual(8, finder.distance)

    def test_something_else_complicated(self):
        data = parse_input('R5, L10, L1, L110')
        finder = Finder(data)
        finder.find()

        self.assertEqual([4, -100], finder.position)
        self.assertEqual(104, finder.distance)

    def test_the_real_hq(self):
        data = parse_input('R8, R4, R4, R8')
        finder = Finder(data)
        finder.find()

        self.assertEqual([4, 0], finder.real_hq_position)
        self.assertEqual(4, finder.real_hq_distance)


if __name__ == '__main__':
    main()
