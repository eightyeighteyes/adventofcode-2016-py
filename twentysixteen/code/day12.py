import os
import unittest

from twentysixteen import INPUTS


def main():
    with open(os.path.join(INPUTS, 'day12.txt'), 'r') as data_file:
        instructions = data_file.readlines()

    assembunny = Assembunny(instructions)
    assembunny.run()

    print("The value in register 'a' is: {}".format(assembunny.registers['a']))

    reassembunny = Assembunny(instructions)
    reassembunny.registers['c'] = 1
    reassembunny.run()

    print("When 'c' is initialized to 1, "
          "the value of 'a' is: {}".format(reassembunny.registers['a']))


VALID_REGISTERS = 'abcd'


class Assembunny(object):
    def __init__(self, instructions):
        self.instructions = [instruction.split() for instruction in instructions]
        self.registers = {register: 0 for register in VALID_REGISTERS}

    def cpy(self, source, destination):
        if source in VALID_REGISTERS:
            self.registers[destination] = self.registers[source]
        else:
            self.registers[destination] = int(source)

    def inc(self, register):
        self.registers[register] += 1

    def dec(self, register):
        self.registers[register] -= 1

    def jnz(self, source, offset):
        if source in VALID_REGISTERS:
            value = self.registers[source]
        else:
            value = source

        if value:
            return int(offset)
        else:
            return 1

    def run(self):
        i = 0
        while i < len(self.instructions):
            line = self.instructions[i]
            command = line[0]
            if command == 'cpy':
                self.cpy(line[1], line[2])
            elif command == 'inc':
                self.inc(line[1])
            elif command == 'dec':
                self.dec(line[1])
            elif command == 'jnz':
                i += self.jnz(line[1], line[2])
                continue
            i += 1


class Test_Day12(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(INPUTS, 'day12.test.txt'), 'r') as data_file:
            self.instructions = data_file.readlines()
        self.assembunny = Assembunny(self.instructions)

    def test_cpy_int(self):
        assembunny = self.assembunny
        assembunny.cpy('41', 'a')
        self.assertEqual(41, assembunny.registers['a'])

    def test_cpy_str(self):
        assembunny = self.assembunny
        assembunny.registers['a'] = 63
        assembunny.cpy('a', 'd')
        self.assertEqual(63, assembunny.registers['d'])

    def test_inc(self):
        assembunny = self.assembunny
        assembunny.inc('b')
        self.assertEqual(1, assembunny.registers['b'])

    def test_dec(self):
        assembunny = self.assembunny
        assembunny.dec('c')
        self.assertEqual(-1, assembunny.registers['c'])

    def test_real_instructions(self):
        assembunny = self.assembunny
        assembunny.run()

        self.assertEqual(42, assembunny.registers['a'])
        self.assertEqual(0, assembunny.registers['b'])
        self.assertEqual(0, assembunny.registers['c'])
        self.assertEqual(0, assembunny.registers['d'])


if __name__ == '__main__':
    main()
