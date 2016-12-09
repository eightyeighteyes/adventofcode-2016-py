import os
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day09.txt'), 'r') as data_file:
        data = data_file.read()

    decompressed = decompress_v1(data)
    print("The decompressed data length is: {}".format(len(decompressed)))
    print("The size of fully decompressed data is: {}".format(full_decompress_len(data)))


def decompress_v1(data):
    decompressed = ''
    i = 0
    while i < len(data):
        char = data[i]
        if char == '(':
            data_slice, end = slice_data(data, i)
            decompressed += data_slice
            i = end
        else:
            decompressed += char
            i += 1

    return decompressed


def slice_data(data, i):
    end_marker = data[i:].find(')') + i
    marker = data[i + 1:end_marker].split('x')
    size = int(marker[0])
    repeat = int(marker[1])
    beg = end_marker + 1
    end = beg + size
    data_slice = str(data[beg:end] * repeat)
    return data_slice, end


def full_decompress_len(data):
    decompressed_size = 0

    i = 0
    while i < len(data):
        char = data[i]
        if char == '(':
            data_slice, end = slice_data(data, i)
            decompressed_size += full_decompress_len(data_slice)
            i = end
        else:
            decompressed_size += 1
            i += 1

    return decompressed_size


class Test_Day09(unittest.TestCase):
    def test_no_markers(self):
        data = 'ADVENT'
        decompressed = decompress_v1(data)

        self.assertEqual('ADVENT', decompressed)

    def test_repeat_seq_len_1(self):
        data = 'A(1x5)BC'
        decompressed = decompress_v1(data)

        self.assertEqual('ABBBBBC', decompressed)

    def test_repeat_seq_len_3(self):
        data = '(3x3)XYZ'
        decompressed = decompress_v1(data)

        self.assertEqual('XYZXYZXYZ', decompressed)

    def test_double_double(self):
        data = 'A(2x2)BCD(2x2)EFG'
        decompressed = decompress_v1(data)

        self.assertEqual('ABCBCDEFEFG', decompressed)

    def test_marker_in_data_section_case_a(self):
        data = '(6x1)(1x3)A'
        decompressed = decompress_v1(data)

        self.assertEqual('(1x3)A', decompressed)

    def test_marker_in_data_section_case_b(self):
        data = 'X(8x2)(3x3)ABCY'
        decompressed = decompress_v1(data)

        self.assertEqual('X(3x3)ABC(3x3)ABCY', decompressed)

    def test_big_numbers(self):
        data = '(10x10)ABCDEFGHIJ'
        decompressed = decompress_v1(data)

        self.assertEqual('ABCDEFGHIJ' * 10, decompressed)

    def test_v2_no_markers(self):
        data = '(3x3)XYZ'
        size = full_decompress_len(data)

        self.assertEqual(9, size)

    def test_v2_simple_nested_marker(self):
        data = 'X(8x2)(3x3)ABCY'
        size = full_decompress_len(data)

        self.assertEqual(20, size)

    def test_v2_extremely_nested_markers(self):
        data = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
        size = full_decompress_len(data)

        self.assertEqual(241920, size)

    def test_v2_complex_markers(self):
        data = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
        size = full_decompress_len(data)

        self.assertEqual(445, size)


if __name__ == '__main__':
    main()
