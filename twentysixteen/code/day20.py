import os
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day20.txt'), 'r') as data_file:
        data = parse_input(data_file.readlines())

    lowest_ip, allowed_ips = get_allowed_ips(data)

    print("The lowest unblocked IP is: {}".format(lowest_ip))
    print("The number of allowed IPs is: {}".format(allowed_ips))


def parse_input(input_data):
    split_data = [line.split('-') for line in input_data]
    return sorted([[int(line[0]), int(line[1])] for line in split_data],
                  lambda x, y: cmp(x[0], y[0]))


def get_allowed_ips(ip_ranges):
    joined_ranges = []
    lowest_ip = None
    for r in ip_ranges:
        joined_ranges = join_ranges(joined_ranges, r)

    allowed_ips = 0
    for i, r in enumerate(joined_ranges):
        potential_ip = r[1] + 1
        if r == joined_ranges[-1]:
            next_min = 2 ** 32 - 1
        else:
            next_min = joined_ranges[i + 1][0]
        if potential_ip < next_min:
            if not lowest_ip:
                lowest_ip = potential_ip
            allowed_ips += next_min - potential_ip

    return lowest_ip, allowed_ips


def join_ranges(joined, sub_range):
    new_range = list(joined)
    if not len(joined):
        new_range.append(sub_range)
    else:
        for i, r in enumerate(joined):
            if ranges_overlap(r, sub_range):
                new_range[i][1] = sub_range[1]
                continue
            elif range_contained(r, sub_range):
                continue

    for r in new_range:
        if range_contained(r, sub_range):
            return new_range

    new_range.append(sub_range)

    return new_range


def ranges_overlap(r1, r2):
    return r1[0] < r2[0] < r1[1] < r2[1]


def range_contained(r1, r2):
    return r1[0] <= r2[0] < r2[1] <= r1[1]


class Test_Day20(unittest.TestCase):
    def test_parse_input(self):
        test_input = ['5-8', '0-2', '4-7']
        parsed_input = parse_input(test_input)
        self.assertEqual([[0, 2], [4, 7], [5, 8]], parsed_input)

    def test_lowest_available_ip(self):
        test_ranges = [[0, 2],
                       [4, 7],
                       [5, 8]]

        lowest_ip = get_allowed_ips(test_ranges)
        self.assertEqual(3, lowest_ip[0])

    def test_compiled_ranges_one_case(self):
        compiled_range = [[4, 7]]
        test_range = [5, 8]

        expected_range = [[4, 8]]
        self.assertEqual(expected_range, join_ranges(compiled_range, test_range))

    def test_compiled_range_loop(self):
        compiled_range = []
        test_ranges = [[0, 2],
                       [4, 7],
                       [5, 8]]

        for r in test_ranges:
            compiled_range = join_ranges(compiled_range, r)

        self.assertEqual([[0, 2], [4, 8]], compiled_range)


if __name__ == '__main__':
    main()
