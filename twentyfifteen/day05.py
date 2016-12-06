import unittest


def has_three_vowels(str_):
    if len([c for c in str_ if c in 'aeiou']) >= 3:
        return True
    return False


def has_double_letter(str_):
    for pos, char in enumerate(str_):
        if pos == len(str_) - 1:
            return False
        if char == str_[pos + 1]:
            return True


def does_not_have_disallowed_substrings(str_):
    blacklist = ['ab', 'cd', 'pq', 'xy']
    for substring in blacklist:
        if substring in str_:
            return False
    return True


def has_repeating_double_sequence(str_):
    for pos, char in enumerate(str_):
        if pos == len(str_) - 2:
            return False
        current_substring = char + str_[pos + 1]
        remaining_string = str_[pos + 2:]
        if current_substring in remaining_string:
            return True


def has_interrupted_repeat(str_):
    for pos, char in enumerate(str_):
        if pos == len(str_) - 2:
            return False
        if char == str_[pos + 2]:
            return True


with open('inputs\day05input.txt', 'r') as data_file:
    data = data_file.readlines()

good_strings = 0
good_strings_b = 0
for str_ in data:
    if has_three_vowels(str_) and has_double_letter(str_) and does_not_have_disallowed_substrings(str_):
        good_strings += 1
    if has_repeating_double_sequence(str_) and has_interrupted_repeat(str_):
        good_strings_b += 1

print "Under the initial rules, there are {} nice strings in the file.".format(good_strings)
print "Under the revised rules, there are {} nice strings in the file.".format(good_strings_b)


class Test_TheThings(unittest.TestCase):
    def test_single_character(self):
        self.assertFalse(
            has_double_letter('a')
        )

    def test_double_characters(self):
        self.assertTrue(
            has_double_letter('aa')
        )
        self.assertTrue(
            has_double_letter('oasiifhwidusk')
        )
        self.assertFalse(
            has_double_letter('oasifhwidusk')
        )

    def test_blacklist_success(self):
        self.assertTrue(
            does_not_have_disallowed_substrings('aced')
        )

    def test_blacklist_failure(self):
        self.assertFalse(
            does_not_have_disallowed_substrings('gagagagagabagaga')
        )

    def test_repeating_sequence_success(self):
        self.assertTrue(
            has_repeating_double_sequence('qjhvhtzxzqqjkmpb')
        )

        self.assertTrue(
            has_repeating_double_sequence('xxyxx')
        )

        self.assertTrue(
            has_repeating_double_sequence('uurcxstgmygtbstg')
        )

    def test_repeating_sequence_failure(self):
        self.assertFalse(
            has_repeating_double_sequence('ieodomkazucvgmuy')
        )

    def test_has_interrupted_repeat_success(self):
        self.assertTrue(
            has_interrupted_repeat('qjhvhtzxzqqjkmpb')
        )
        self.assertTrue(
            has_interrupted_repeat('xxyxx')
        )
        self.assertTrue(
            has_interrupted_repeat('ieodomkazucvgmuy')
        )

    def test_has_interrupted_repeat_failure(self):
        self.assertFalse(
            has_interrupted_repeat('uurcxstgmygtbstg')
        )
