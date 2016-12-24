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


VALID_REGISTERS = ['a', 'b', 'c', 'd']


def process_instruction(instruction):
    instruction = instruction.split()
    if len(instruction) > 2:
        try:
            instruction[2] = int(instruction[2])
        except ValueError:
            pass

    return instruction


class Assembunny(object):
    def __init__(self, instructions):
        self.instructions = [process_instruction(instruction) for instruction in instructions]
        self.registers = {register: 0 for register in VALID_REGISTERS}
        self.address = 0
        self.incs = []
        self.decs = []

        self.instruction_map = {
            'cpy': self.cpy,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz
        }

    @property
    def line(self):
        return self.instructions[self.address]

    @property
    def command(self):
        return self.line[0]

    @command.setter
    def command(self, value):
        address = value[0]
        self.instructions[address][0] = value[1]

    def cpy(self, *args):
        source = args[0]
        destination = args[1]
        if source in VALID_REGISTERS:
            self.registers[destination] = self.registers[source]
        else:
            self.registers[destination] = int(source)

    def inc(self, *args):
        register = args[0]
        self.registers[register] += 1

    def dec(self, *args):
        register = args[0]
        self.registers[register] -= 1

    def jnz(self, *args):
        source = args[0]
        offset = args[1]
        if source in VALID_REGISTERS:
            value = self.registers[source]
        else:
            value = source

        if offset in VALID_REGISTERS:
            offset = self.registers[offset]

        if value:
            return int(offset)
        else:
            return 1

    def run(self):
        while self.address < len(self.instructions):
            arg1 = self.line[1]
            try:
                arg2 = self.line[2]
            except IndexError:
                arg2 = None

            if self.command == 'jnz':
                self.address += self.jnz(arg1, arg2)
                continue
            else:
                self.instruction_map[self.command](arg1, arg2)
            self.address += 1


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

    def test_indexed_setter(self):
        assembunny = self.assembunny
        assembunny.command = [1, 'dingus']
        assembunny.address = 1

        self.assertEqual('dingus', assembunny.command)


if __name__ == '__main__':
    main()
