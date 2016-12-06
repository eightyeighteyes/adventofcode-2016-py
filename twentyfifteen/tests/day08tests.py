import unittest

import day08


class Test_Count_Literals(unittest.TestCase):
    def test_expected_length_simple(self):
        self.assertEqual(
            6,
            day08.count_literals('"dpmxnj"\n')
        )

    def test_escaped_quotes(self):
        self.assertEqual(
            23,
            day08.count_literals('"twybw\"cdvf\"mjdajurokbce"\n')
        )

    def test_escaped_backslash(self):
        self.assertEqual(
            12,
            day08.count_literals('"roc\\vra\\lhrm"\n')
        )

    def test_escaped_hex_notation(self):
        self.assertEqual(
            15,
            day08.count_literals('"aixfk\xc0iom\x21vueob"\n')
        )

    def test_just_double_quotes(self):
        self.assertEqual(
            0,
            day08.count_literals('""\n')
        )

    def test_extra_simple(self):
        self.assertEqual(
            3,
            day08.count_literals('"abc"\n')
        )

    def test_single_escaped_quote(self):
        self.assertEqual(
            7,
            day08.count_literals('"aaa\"aaa"\n')
        )

    def test_basic_hex_escape(self):
        self.assertEqual(
            1,
            day08.count_literals('"\x27"\n')
        )


class Test_Count_Code_Characters(unittest.TestCase):
    def test_expected_length_simple(self):
        self.assertEqual(
            8,
            day08.count_code_characters('"dpmxnj"\n')
        )

    def test_escaped_quotes(self):
        self.assertEqual(
            27,
            day08.count_code_characters('"twybw\"cdvf\"mjdajurokbce"\n')
        )

    def test_escaped_backslash(self):
        self.assertEqual(
            16,
            day08.count_code_characters('"roc\\vra\\lhrm"\n')
        )

    def test_escaped_hex_notation(self):
        self.assertEqual(
            23,
            day08.count_code_characters('"aixfk\xc0iom\x21vueob"\n')
        )

    def test_just_double_quotes(self):
        self.assertEqual(
            2,
            day08.count_code_characters('""\n')
        )

    def test_extra_simple(self):
        self.assertEqual(
            5,
            day08.count_code_characters('"abc"\n')
        )

    def test_single_escaped_quote(self):
        self.assertEqual(
            10,
            day08.count_code_characters('"aaa\"aaa"\n')
        )

    def test_basic_hex_escape(self):
        self.assertEqual(
            6,
            day08.count_code_characters('"\x27"\n')
        )
