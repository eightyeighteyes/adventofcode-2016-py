import os
import unittest

from twentysixteen import INPUTS
from twentysixteen.code.day12 import Assembunny


def main():
    with open(os.path.join(INPUTS, 'day23.txt'), 'r') as data_file:
        instructions = data_file.readlines()

    bunny = TglAssembunny(instructions)
    bunny.registers['a'] = 7
    bunny.run()

    print("The value to send to the safe is: {}".format(bunny.registers['a']))

    rebunny = TglAssembunny(instructions)
    rebunny.registers['a'] = 12
    rebunny.run()
    print("The actual value to send to the safe is: {}".format(rebunny.registers['a']))


class TglAssembunny(Assembunny):
    def __init__(self, instructions):
        super(TglAssembunny, self).__init__(instructions)
        self.instruction_map['tgl'] = self.tgl
        self.instruction_map['skip'] = self.skip

    def tgl(self, *args):
        register = args[0]
        addr = self.registers[register] + self.address
        if addr >= len(self.instructions):
            return

        line = self.instructions[addr]
        command = line[0]
        if len(line) == 2:
            if command == 'inc':
                self.command = [addr, 'dec']
            else:
                self.command = [addr, 'inc']
        else:
            if command == 'jnz':
                self.command = [addr, 'cpy']
                if isinstance(self.instructions[addr][2], int):
                    self.command = [addr, 'skip']
            else:
                self.command = [addr, 'jnz']

    def skip(self, *args):
        pass


class Test_Day23(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(INPUTS, 'day23.test.txt'), 'r') as data_file:
            self.instructions = data_file.readlines()

        self.bunny = TglAssembunny(self.instructions)

    def test_tgl_inc(self):
        bunny = TglAssembunny(['inc a'])
        bunny.tgl('a')
        self.assertEqual('dec', bunny.instructions[0][0])

    def test_tgl_dec(self):
        bunny = TglAssembunny(['dec a'])
        bunny.tgl('a')
        self.assertEqual('inc', bunny.instructions[0][0])

    def test_tgl_jnz(self):
        bunny = TglAssembunny(['jnz a b'])
        bunny.tgl('a')
        self.assertEqual('cpy', bunny.instructions[0][0])

    def test_tgl_jnz_to_invalid(self):
        bunny = TglAssembunny(['jnz a 5'])
        bunny.tgl('a')
        self.assertEqual('skip', bunny.instructions[0][0])

    def test_tgl_cpy(self):
        bunny = TglAssembunny(['cpy a 5'])
        bunny.tgl('a')
        self.assertEqual('jnz', bunny.instructions[0][0])

    def test_tgl_skip_to_jnz(self):
        bunny = TglAssembunny(['skip a 5'])
        bunny.tgl('a')
        self.assertEqual('jnz', bunny.instructions[0][0])

    def test_tgl_tgl(self):
        bunny = TglAssembunny(['tgl 0'])
        bunny.tgl('a')
        self.assertEqual('inc', bunny.instructions[0][0])

    def test_tglassembunny_run(self):
        self.bunny.run()

        self.assertEqual(3, self.bunny.registers['a'])


if __name__ == '__main__':
    main()
