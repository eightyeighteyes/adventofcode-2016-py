import os
import re
import unittest
from string import ascii_lowercase

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day04.txt'), 'r') as data_file:
        data = [Room(data_line) for data_line in data_file.readlines()]

    real_rooms = [room for room in data if room.is_real]
    real_room_sectors = [room.sector for room in real_rooms]

    npo_sector = [room.sector for room in real_rooms
                  if room.decrypted_name == 'northpole object storage'][0]

    print("The sum of all real room sectors is: {}".format(sum(real_room_sectors)))
    print("These are the real room names:")
    print("-" * 26)
    for room in real_rooms:
        print room.decrypted_name

    print("This is the sector where northpole object storage is: {}".format(npo_sector))


class Room(object):
    def __init__(self, data_line):
        self.data = data_line.split('-')
        self.name = ' '.join(self.data[:-1])
        self.compact_name = self.name.replace(' ', '')

    @property
    def sector(self):
        return int(re.findall(r'\d+', self.data[-1])[0])

    @property
    def checksum(self):
        return re.search(r"\[(\D+)]", self.data[-1]).group(1)

    @property
    def is_real(self):
        return self._validate_room()

    @property
    def decrypted_name(self):
        return self._decrypt_name()

    def _decrypt_name(self):
        shift = self.sector % 26
        decoded = ''

        for letter in self.name:
            if letter == ' ':
                decoded += letter
                continue
            i = ascii_lowercase.find(letter)
            new_i = i + shift
            if new_i > 25:
                new_i -= 26
            decoded += ascii_lowercase[new_i]

        return decoded

    def _validate_room(self):
        name = self._sort_name()

        valid_checksum = name[:5]

        return valid_checksum == self.checksum

    def _sort_name(self):
        name = sorted(self.compact_name)
        letter_group = []
        letter_groups = []

        for i, letter in enumerate(name):
            next_i = i + 1
            letter_group.append(letter)
            if next_i == len(name):
                letter_groups.append(letter_group)
                continue
            if letter != name[next_i]:
                letter_groups.append(letter_group)
                letter_group = []

        sorted_name = sorted(letter_groups, key=lambda x: len(x), reverse=True)

        sorted_name = ''.join([letter_group[0] for letter_group in sorted_name])

        return sorted_name


class Test_Day04(unittest.TestCase):
    def test_room(self):
        room = Room('aaaaa-bbb-z-y-x-123[abxyz]')
        self.assertEqual('aaaaa bbb z y x', room.name)
        self.assertEqual(123, room.sector)
        self.assertEqual('abxyz', room.checksum)

    def test_real_example_one(self):
        room = Room('aaaaa-bbb-z-y-x-123[abxyz]')
        self.assertIs(True, room.is_real)

    def test_real_example_two(self):
        room = Room('a-b-c-d-e-f-g-h-987[abcde]')
        self.assertIs(True, room.is_real)

    def test_real_example_three(self):
        room = Room('not-a-real-room-404[oarel]')
        self.assertIs(True, room.is_real)

    def test_fake_example(self):
        room = Room('totally-real-room-200[decoy]')
        self.assertIs(False, room.is_real)

    def test_decrypted_name(self):
        room = Room('qzmt-zixmtkozy-ivhz-343')
        self.assertEqual('very encrypted name', room.decrypted_name)


if __name__ == "__main__":
    main()
