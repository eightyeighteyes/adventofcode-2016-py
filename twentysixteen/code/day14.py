import hashlib
import logging
import unittest

KEYGEN_LOG = logging.getLogger(__name__)
KEYGEN_LOG.addHandler(logging.StreamHandler())
KEYGEN_LOG.setLevel(logging.DEBUG)

SALT = 'ahsbgdzn'


def main():
    keygen = Keygen(SALT)
    keygen.find_keys(64)

    print("The index that produces the 64th key is: {}".format(keygen.key_indices[-1]))

    rekeygen = Keygen(SALT)
    rekeygen.find_keys(64, stretched=True)

    print("The index that produces the 64th key "
          "when stretching the hash is: {}".format(rekeygen.key_indices[-1]))


class Keygen(object):
    def __init__(self, salt, stretch=2016):
        self.salt = salt
        self.stretch = stretch

        self.index = 0
        self.key_indices = []

    def find_key_index(self, stretched=False):
        while True:
            current_hash = self.make_hash(stretched=stretched)
            for i, c in enumerate(current_hash):
                if c * 3 in current_hash[i:i + 3]:
                    possible_index = self.index
                    KEYGEN_LOG.debug("Checking hash at index %s: %s", self.index, current_hash)
                    if self.is_valid_hash(c, stretched):
                        self.key_indices.append(possible_index)
                        KEYGEN_LOG.debug("Found %s key indices so far.", len(self.key_indices))
                        self.index += 1
                        return possible_index
                    else:
                        break
            self.index += 1

    def is_valid_hash(self, char, stretched=False):
        for i in range(1, 1001):
            base_index = self.index + i
            current_hash = self.make_hash(base_index, stretched)
            if char * 5 in current_hash:
                KEYGEN_LOG.debug("Found 5-char hash at index %s: %s", base_index, current_hash)
                return True
        return False

    def make_hash(self, index=None, stretched=False):
        if not index:
            index = self.index

        base = "{}{}".format(self.salt, index)
        single_hash = hashlib.md5(base).hexdigest()

        if stretched:
            stretched_hash = single_hash
            for _ in range(self.stretch):
                stretched_hash = hashlib.md5(stretched_hash).hexdigest()
            return stretched_hash
        else:
            return single_hash

    def find_keys(self, num_keys, stretched=False):
        for num in range(num_keys):
            self.find_key_index(stretched)
        KEYGEN_LOG.debug("Key indicies found: %s", self.key_indices)


class Test_Day14(unittest.TestCase):
    def setUp(self):
        self.keygen = Keygen('abc')

    def test_index_first(self):
        index = self.keygen.find_key_index()
        self.assertEqual(39, index)
        self.assertEqual(39, self.keygen.key_indices[0])

    def test_index_second(self):
        self.keygen.find_keys(2)
        self.assertEqual(92, self.keygen.key_indices[-1])

    def test_last_index(self):
        self.keygen.find_keys(64)
        self.assertEqual(22728, self.keygen.key_indices[-1])

    def test_stretched_hash_1(self):
        self.keygen.stretch = 1
        stretched_hash = self.keygen.make_hash(stretched=True)
        self.assertEqual('eec80a0c92dc8a0777c619d9bb51e910', stretched_hash)

    def test_stretched_hash_2(self):
        self.keygen.stretch = 2
        stretched_hash = self.keygen.make_hash(stretched=True)
        self.assertEqual('16062ce768787384c81fe17a7a60c7e3', stretched_hash)

    def test_stretched_hash_full(self):
        stretched_hash = self.keygen.make_hash(stretched=True)
        self.assertEqual('a107ff634856bb300138cac6568c0f24', stretched_hash)

    def test_stretched_index_first(self):
        index = self.keygen.find_key_index(stretched=True)
        self.assertEqual(10, index)

    def test_stretched_index_find_keys(self):
        self.keygen.find_keys(1, stretched=True)
        self.assertEqual(10, self.keygen.key_indices[0])


if __name__ == '__main__':
    main()
