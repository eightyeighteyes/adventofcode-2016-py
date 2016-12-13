import os
import unittest

from collections import Counter

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day06.txt'), 'r') as data_file:
        data = data_file.readlines()

    parsed_data = parse_data(data)
    first_message = decode_message(parsed_data)
    second_message = decode_least_common(parsed_data)

    print("The first decoded message is: {}".format(first_message))
    print("The second decoded message is: {}".format(second_message))


def parse_data(data):
    parsed_data = []

    for i in range(len(data[0]) - 1):
        column = ''
        for line in data:
            column += line[i]
        parsed_data.append(column)

    return parsed_data


def decode_message(parsed_data):
    message = ''
    for column in parsed_data:
        letters = Counter(column)
        message += letters.most_common(1)[0][0]

    return message


def decode_least_common(parsed_data):
    message = ''
    for column in parsed_data:
        letters = Counter(column)
        message += letters.most_common(len(letters))[-1][0]

    return message


class Test_Day06(unittest.TestCase):
    with open(os.path.join(INPUTS, 'day06.test.txt'), 'r') as data_file:
        test_data = data_file.readlines()

    def test_parse_data(self):
        parsed_data = parse_data(self.test_data)

        self.assertEqual('ederatsrnnstvvde', parsed_data[0])

    def test_decode_test_input(self):
        parsed_data = parse_data(self.test_data)
        message = decode_message(parsed_data)

        self.assertEqual('easter', message)

    def test_least_common(self):
        parsed_data = parse_data(self.test_data)

        message = decode_least_common(parsed_data)

        self.assertEqual('advent', message)


if __name__ == '__main__':
    main()
