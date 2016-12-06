from collections import defaultdict
import operator
import re
import struct

instruction_pattern = r"(?P<source>[a-z]*?)[\s]*(?P<instruction>[A-Z]*?)[\s]*(?P<value>[a-z0-9]*) -> (?P<destination>[a-z]*)"


def op_not(value):
    return ~value & 0xffff


def op_eq(value):
    return value


def memoize(f):
    memo = {}

    def helper(graph, key):
        if key not in memo:
            memo[key] = f(graph, key)
        return memo[key]

    return helper


class Kit(object):
    def __init__(self):
        self.wires = {}
        self.instructions = []
        self.source = None
        self.destination = None
        self.instruction = None
        self.value = None

    def parse_line(self, line):
        parse = re.search(instruction_pattern, line)
        self.source = parse.group('source')
        self.destination = parse.group('destination')
        self.instruction = parse.group('instruction')
        self.value = parse.group('value')
        try:
            self.value = int(self.value)
        except ValueError:
            pass

        self.instructions.append((self.source, self.instruction, self.value, self.destination))

    def process_data(self, data):
        for line in data:
            self.parse_line(line)
            self.wire_circuit()
        self.run_circuit()

    def wire_circuit(self):
        """
        Make sure all the connections exist.
        """
        if self.destination not in self.wires.keys():
            self.wires[self.destination] = 0

            # if self.destination not in self.wires:
            #     self.wires[self.destination] = {}
            # self.wires[self.destination]['source'] = self.source
            # self.wires[self.destination]['instruction'] = self.instruction
            # self.wires[self.destination]['instruction_value'] = self.value
            # if self.instruction == '':
            #     self.wires[self.destination]['value'] = self.value

    def run_circuit(self):
        """
        Compute the values.
        """
        for instruction in self.instructions:
            if instruction[0] == '' and instruction[1] == '':
                self.wires[instruction[3]] = instruction[2]
            elif instruction[0] == '':
                op_not(self.wires[self.instruction[2]])



        pass
        # while 'value' not in self.wires['i'].items():
        #     for wire in self.wires.values():
        #         if 'value' not in wire.values() and wire['source'] != '':
        #             if 'value' in self.wires[wire['source']].items():
        #                 if type(self.wires[wire['source']['instruction_value']]) is int:
        #                     self.get_wire_value(wire)

    def get_wire_value(self, wire):
        if wire['instruction'] == 'AND':
            wire['value'] = self.wires[wire['source']['value']] & wire['instruction_value']
        elif wire['instruction'] == 'OR':
            wire['value'] = self.wires[wire['source']['value']] | wire['instruction_value']
        elif wire['instruction'] == 'LSHIFT':
            wire['value'] = self.wires[wire['source']['value']] << wire['instruction_value']
        elif wire['instruction'] == 'RSHIFT':
            wire['value'] = self.wires[wire['source']['value']] >> wire['instruction_value']
        elif wire['instruction'] == 'NOT':
            wire['value'] = ~ self.wires[wire['source']['value']]
            if wire['value'] < 0:
                wire['value'] = struct.unpack('H', struct.pack('h', wire['value']))


def main():
    if __name__ == '__main__':
        with open("inputs\day07input.txt", 'r') as data_file:
            data = data_file.readlines()
        kit = Kit()
        kit.process_data(data)
        print("The value of wire a is: {}".format(kit.wires['a']))


main()
