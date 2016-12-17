import os
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day15.txt'), 'r') as data_file:
        discs = parse_data(data_file.readlines())

    timing = correct_timing(discs)

    print("The right time to press the button is at second {}".format(timing))

    discs.append(Disc(11, 0))

    timing_2 = correct_timing(discs)

    print("The right time for the second configuration is second {}".format(timing_2))


def parse_data(data):
    parsed = [line.replace('.', '').split() for line in data]
    return [Disc(int(line[3]), int(line[-1])) for line in parsed]


def correct_timing(discs):
    timing = 0
    while True:
        disc_positions = []
        for i, disc in enumerate(discs):
            level = i + 1
            position = level + timing + disc.start
            disc_positions.append(position % disc.positions)
        if all(pos == 0 for pos in disc_positions):
            return timing
        else:
            timing += 1


class Disc(object):
    def __init__(self, positions, start):
        self.positions = positions
        self.start = start

    def __repr__(self):
        return "<Disc: {} positions, starts at {}>".format(self.positions, self.start)


class Test_Day15(unittest.TestCase):
    def setUp(self):
        self.discs = [Disc(5, 4), Disc(2, 1)]

    def test_correct_timing(self):
        timing = correct_timing(self.discs)

        self.assertEqual(5, timing)


if __name__ == '__main__':
    main()
