import os
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day03.txt'), 'r') as data_file:
        data = data_file.readlines()
        row_data = parse_row_data(data)
        column_data = parse_column_data(row_data)

    possible_triangles_by_row = len(valid_triangles(row_data))
    possible_triangles_by_column = len(valid_triangles(column_data))

    print("Number of possible triangles by row: {}".format(possible_triangles_by_row))
    print("Number of possible triangles by column: {}".format(possible_triangles_by_column))


def parse_row_data(data):
    parsed_data = []
    for line in data:
        line = line.strip().split(' ')
        parsed_data.append([int(side) for side in line if len(side)])

    return parsed_data


def parse_column_data(row_data):
    column_data = []
    group = []
    for i in range(3):
        for row in row_data:
            group.append(row[i])
            if len(group) == 3:
                column_data.append(group)
                group = []

    return column_data


def valid_triangles(parsed_data):
    return [triangle for triangle in parsed_data if valid_triangle(triangle)]


def valid_triangle(sides):
    sides = sorted(sides)
    return sides[0] + sides[1] > sides[2]


class Test_Traingles(unittest.TestCase):
    def test_invalid_traingle(self):
        test_data = [5, 10, 25]
        self.assertFalse(valid_triangle(test_data))

    def test_valid_triangle(self):
        test_data = [10, 20, 25]
        self.assertTrue(valid_triangle(test_data))

    def test_unsorted_vvalues(self):
        self.assertTrue(valid_triangle([25, 10, 20]))
        self.assertFalse(valid_triangle([10, 25, 5]))


if __name__ == '__main__':
    main()
