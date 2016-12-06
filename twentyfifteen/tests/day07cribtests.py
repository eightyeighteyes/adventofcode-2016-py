import unittest

import day07crib


class Test_Day07Crib(unittest.TestCase):
    data_file = "day07cribtestsinput.txt"
    graph = day07crib.read_graph(data_file)

    def test_wire_d(self):
        self.assertEqual(
            72,
            day07crib.find_key(self.graph, 'd')
        )

    def test_wire_e(self):
        self.assertEqual(
            507,
            day07crib.find_key(self.graph, 'e')
        )

    def test_wire_f(self):
        self.assertEqual(
            492,
            day07crib.find_key(self.graph, 'f')
        )

    def test_wire_g(self):
        self.assertEqual(
            114,
            day07crib.find_key(self.graph, 'g')
        )

    def test_wire_h(self):
        self.assertEqual(
            65412,
            day07crib.find_key(self.graph, 'h')
        )

    def test_wire_i(self):
        self.assertEqual(
            65079,
            day07crib.find_key(self.graph, 'i')
        )

    def test_wire_x(self):
        self.assertEqual(
            123,
            day07crib.find_key(self.graph, 'x')
        )

    def test_wire_y(self):
        self.assertEqual(
            456,
            day07crib.find_key(self.graph, 'y')
        )
