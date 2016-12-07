import os
import re
import unittest

from twentysixteen import INPUTS

CHAR_FINDER = r'\w+'
INSIDE_FINDER = r'\[(\w+)\]'


def main():
    with open(os.path.join(INPUTS, 'day07.txt'), 'r') as data_file:
        data = [line.rstrip() for line in data_file.readlines()]

    addrs_with_tls = [addr for addr in data if supports_tls(addr)]
    print("The number of IPs that support "
          "Transport-Layer Snooping is: {}".format(len(addrs_with_tls)))

    addrs_with_ssl = [addr for addr in data if supports_ssl(addr)]
    print("The number of IPs that supprt "
          "Super-Secret Listening is: {}".format(len(addrs_with_ssl)))


def parse_addr(ip_addr):
    char_finder = re.compile(CHAR_FINDER)
    inside_finder = re.compile(INSIDE_FINDER)
    all_groups = char_finder.findall(ip_addr)
    insides = inside_finder.findall(ip_addr)
    outsides = [group for group in all_groups if group not in insides]
    return insides, outsides


def supports_tls(ip_addr):
    insides, outsides = parse_addr(ip_addr)
    if any(has_abba(seq) for seq in outsides) and not any(has_abba(seq) for seq in insides):
        return True
    return False


def has_abba(sequence):
    for i, char in enumerate(sequence):
        if i < len(sequence) - 3:
            if char == sequence[i + 3]:
                if sequence[i + 1] == char:
                    continue
                if sequence[i + 1] == sequence[i + 2]:
                    return True
    return False


def supports_ssl(ip_addr):
    insides, outsides = parse_addr(ip_addr)
    abas, babs = find_good_seqs(outsides)
    if not all([abas, babs]):
        return False
    for bab in babs:
        for inside in insides:
            if bab in inside:
                return True
    return False


def find_good_seqs(outsides):
    abas = []
    for sequence in outsides:
        for i, char in enumerate(sequence):
            if i < len(sequence) - 2:
                if char == sequence[i + 1]:
                    continue
                if char == sequence[i + 2]:
                    abas.append(sequence[i:i + 3])
    babs = make_babs(abas)
    return abas, babs


def make_babs(abas):
    return [aba[1] + aba[0] + aba[1] for aba in abas]


class Test_Day07(unittest.TestCase):
    def test_positive_tls_outside_brackets(self):
        test_data = 'abba[mnop]qrst'
        self.assertTrue(supports_tls(test_data))

    def test_negative_tls_inside_brackets(self):
        test_data = 'abcd[bddb]xyyx'
        self.assertFalse(supports_tls(test_data))

    def test_negative_tls_outside_brackets_but_need_different_interior_chars(self):
        test_data = 'aaaa[qwer]tyui'
        self.assertFalse(supports_tls(test_data))

    def test_positive_tls_outside_brackets_but_in_larger_string(self):
        test_data = 'ioxxoj[asdfgh]zxcvbn'
        self.assertTrue(supports_tls(test_data))

    def test_positive_ssl_aba_outside_with_bab_inside(self):
        test_data = 'aba[bab]xyz'
        self.assertTrue(supports_ssl(test_data))

    def test_negative_ssl_aba_with_no_baba(self):
        test_data = 'xyx[xyx]xyx'
        self.assertFalse(supports_ssl(test_data))

    def test_positive_ssl_aba_with_matching_bab(self):
        test_data = 'aaa[kek]eke'
        self.assertTrue(supports_ssl(test_data))

    def test_positive_ssl_overlapping_aba_with_matching_bab(self):
        test_data = 'zazbz[bzb]cdb'
        self.assertTrue(supports_ssl(test_data))


if __name__ == '__main__':
    main()
