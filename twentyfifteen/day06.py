import re
import numpy as np

instruction_pattern = r"(?P<instructions>[a-z\s]+?)(?P<start>[\d,]+)\ through\ (?P<end>[\d,]+)"


class LightGrid(object):
    def __init__(self):
        self.grid = np.zeros((1000, 1000), dtype=np.int)
        self.bright_grid = np.zeros((1000, 1000), dtype=np.int)
        self.on = 0
        self.brightness = 0
        self.start_x = 0
        self.end_x = 0
        self.start_y = 0
        self.end_y = 0
        self.instructions = None

    def run_line(self, line):
        self.parse_line(line)
        if self.instructions == 'turn on':
            self.grid[self.start_y:self.end_y, self.start_x:self.end_x] = 1
        if self.instructions == 'turn off':
            self.grid[self.start_y:self.end_y, self.start_x:self.end_x] = 0
        if self.instructions == 'toggle':
            for y in range(self.start_y, self.end_y):
                for x in range(self.start_x, self.end_x):
                    if self.grid[y][x]:
                        self.grid[y][x] = 0
                    else:
                        self.grid[y][x] = 1
        self.count_lights()

    def parse_line(self, line):
        parse = re.search(instruction_pattern, line)
        self.instructions = parse.group('instructions').rstrip()
        start = map(int, parse.group('start').split(','))
        self.start_x = start[0]
        self.start_y = start[1]
        end = map(int, parse.group('end').split(','))
        self.end_x = end[0] + 1
        self.end_y = end[1] + 1

    def count_lights(self):
        self.on = np.sum(self.grid)

    def count_brightness(self):
        self.brightness = np.sum(self.bright_grid)

    def run_brightness(self, line):
        self.parse_line(line)
        if self.instructions == 'turn on':
            self.bright_grid[self.start_y:self.end_y, self.start_x:self.end_x] += 1
        elif self.instructions == 'toggle':
            self.bright_grid[self.start_y:self.end_y, self.start_x:self.end_x] += 2
        elif self.instructions == 'turn off':
            for y in range(self.start_y, self.end_y):
                for x in range(self.start_x, self.end_x):
                    if self.bright_grid[y][x] > 0:
                        self.bright_grid[y][x] -= 1

        self.count_brightness()


def main():
    grid = LightGrid()
    with open('inputs\day06input.txt', 'r') as data_file:
        data = data_file.readlines()

    for line in data:
        grid.run_line(line.strip())
        grid.run_brightness(line.strip())
    print('Following the instructions as on/off, {} lights are on'.format(grid.on))
    print('Following the instructions for brightness, the brightness value of the array is {}'.format(grid.brightness))


if __name__ == '__main__':
    main()
