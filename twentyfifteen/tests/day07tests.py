import unittest

import day07


class Test_Day07(unittest.TestCase):
    data = [
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y RSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i"
    ]

    kit = day07.Kit()
    kit.process_data(data)

    def test_wire_d(self):
        self.assertEqual(
            72,
            self.kit.wires['d']
        )

    def test_wire_e(self):
        self.assertEqual(
            507,
            self.kit.wires['e']
        )

    def test_wire_f(self):
        self.assertEqual(
            492,
            self.kit.wires['f']
        )

    def test_wire_g(self):
        self.assertEqual(
            114,
            self.kit.wires['g']
        )

    def test_wire_h(self):
        self.assertEqual(
            65412,
            self.kit.wires['h']
        )

    def test_wire_i(self):
        self.assertEqual(
            65079,
            self.kit.wires['i']
        )

    def test_wire_x(self):
        self.assertEqual(
            123,
            self.kit.wires['x']
        )

    def test_wire_y(self):
        self.assertEqual(
            456,
            self.kit.wires['y']
        )
