import unittest

INPUT = '10001110011110000'


def main():
    checksum_one = expand_and_check(INPUT, 272)
    print("The checksum for the first disk is: {}".format(checksum_one))

    checksum_two = expand_and_check(INPUT, 35651584)
    print("The checksum for the second disk is: {}".format(checksum_two))


def expand_and_check(data, end_size):
    while len(data) <= end_size:
        data = expand(data)
    data = data[:end_size]
    return make_checksum(data)


def transform(char):
    if char == '1':
        return '0'
    else:
        return '1'


def expand(data):
    a = data
    b = [transform(c) for c in data]

    return "{}0{}".format(a, ''.join(reversed(b)))


def make_checksum(data):
    pairs = [data[i:i + 2] for i, d in enumerate(data) if not i % 2]
    checksum = ''
    for pair in pairs:
        if pair[0] == pair[1]:
            checksum += '1'
        else:
            checksum += '0'
    if not len(checksum) % 2:
        checksum = make_checksum(checksum)
    return checksum


class Test_Day16(unittest.TestCase):
    def test_expand_data_case01(self):
        test_input = '1'
        output = expand(test_input)
        self.assertEqual('100', output)

    def test_expand_data_case02(self):
        test_input = '0'
        output = expand(test_input)
        self.assertEqual('001', output)

    def test_expand_data_case03(self):
        test_input = '11111'
        output = expand(test_input)
        self.assertEqual('11111000000', output)

    def test_expand_data_case04(self):
        test_input = '111100001010'
        output = expand(test_input)
        self.assertEqual('1111000010100101011110000', output)

    def test_checksum_case01(self):
        test_input = '110010110100'
        checksum = make_checksum(test_input)
        self.assertEqual('100', checksum)

    def test_expand_and_check(self):
        test_input = '10000'
        disk_size = 20
        actual_checksum = expand_and_check(test_input, disk_size)
        expected_checksum = '01100'

        self.assertEqual(expected_checksum, actual_checksum)


if __name__ == '__main__':
    main()
