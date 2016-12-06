import hashlib
import unittest

DOOR_ID = 'uqwqemis'


def main():
    first_password = find_password()
    print("The first password is: {}".format(first_password))

    second_password = find_positional_password()
    print("The second password is: {}".format(second_password))


def find_five_zero_hash(start=0, door_id=DOOR_ID):
    index = start
    good_hash = ''
    while True:
        good_hash = hashlib.md5("{}{}".format(door_id, index)).hexdigest()
        if good_hash.startswith('00000'):
            break
        index += 1

    return good_hash, index


def find_password(door_id=DOOR_ID):
    password = ''
    index = 0
    for _ in range(8):
        good_hash, index = find_five_zero_hash(index, door_id)
        password += good_hash[5]
        index += 1

    return password


def find_positional_password(door_id=DOOR_ID):
    password = [''] * 8
    index = 0
    while not all(password):
        good_hash, index = find_five_zero_hash(index, door_id)

        try:
            p_index = int(good_hash[5])
        except ValueError:
            index += 1
            continue

        if p_index not in range(8) or password[p_index]:
            index += 1
            continue

        password[p_index] = good_hash[6]

        index += 1

    return ''.join(password)


class Test_Day05(unittest.TestCase):
    def test_find_hash(self):
        door_id = 'abc'
        good_hash, index = find_five_zero_hash(door_id=door_id)

        self.assertEqual(3231929, index)

    def test_find_password(self):
        door_id = 'abc'
        password = find_password(door_id=door_id)

        self.assertEqual('18f47a30', password)

    def test_find_positional_password(self):
        door_id = 'abc'
        password = find_positional_password(door_id=door_id)

        self.assertEqual('05ace8e3', password)


if __name__ == '__main__':
    main()
