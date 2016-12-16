from heapq import heapify, heappush, heappop
import unittest

# A* maze solving algorithm cribbed from:
# http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
# my tweaks:
#   the Maze object builds its maze off a seed
#   a method to count spaces within a given amount of steps
#   a method to draw the maze

SEED = 1362


def main():
    maze = Maze(size=(40, 40), destination=(31, 39))
    maze.solve()
    print("Ideal path:")
    maze.draw()
    print("The length of the ideal path is {} steps.\n".format(len(maze.path)))

    maze.__init__((maze.width, maze.height), (maze.end.x, maze.end.y))
    in_range = maze.cells_in_range(50)
    print("Cells within 50 steps:")
    maze.draw()
    print("The number of locations that can be visited in 50 steps is: {}\n".format(len(in_range)))


def one_bits(num):
    return len(bin(num).replace('0', '').replace('b', ''))


class Cell(object):
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.reachable = reachable
        self.parent = None
        self.cost = 0
        self.distance = 0
        self.impact = 0

    def __repr__(self):
        return "<Cell ({},{})>".format(self.x, self.y)


class Maze(object):
    def __init__(self, size=(10, 10), destination=(2, 2), seed=SEED):
        self.seed = seed
        self.height = size[1]
        self.width = size[0]
        self.cells = []
        self._make_maze()

        self.start = self._get_cell(1, 1)
        self.end = self._get_cell(*destination)
        self.path = []
        self.in_range = set()

        self.open = []
        heapify(self.open)
        self.closed = set()

    def is_wall(self, x, y):
        if x < 0 or y < 0:
            return 1
        base = (x * x + 3 * x + 2 * x * y + y + y * y) + self.seed
        return one_bits(base) % 2

    def _make_maze(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if self.is_wall(x, y):
                    reachable = False
                else:
                    reachable = True
                cell = Cell(x, y, reachable)
                row.append(cell)
            self.cells.append(row)

    def _get_distance(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def _get_cell(self, x, y):
        return self.cells[y][x]

    def _get_adjacent(self, cell):
        cells = []
        if cell.x < self.width - 1:
            cells.append(self._get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self._get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self._get_cell(cell.x - 1, cell.y))
        if cell.y < self.height - 1:
            cells.append(self._get_cell(cell.x, cell.y + 1))
        return cells

    def _make_path(self):
        cell = self.end
        while cell.parent is not self.start:
            self.path.append(cell)
            cell = cell.parent
        self.path.append(cell)

    def _update_cell(self, adjacent, cell):
        adjacent.cost = cell.cost + 1
        adjacent.distance = self._get_distance(cell)
        adjacent.parent = cell
        adjacent.impact = adjacent.distance + adjacent.cost

    def _draw_cell(self, cell):
        if cell in self.path:
            return 'O'
        if cell in self.in_range:
            return '0'
        if cell in self.closed:
            return 'x'
        if cell.reachable:
            return '.'
        else:
            return '*'

    def solve(self):
        heappush(self.open, (self.start.impact, self.start))
        while len(self.open):
            impact, cell = heappop(self.open)
            self.closed.add(cell)
            if cell is self.end:
                self._make_path()
                break
            adj_cells = self._get_adjacent(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.impact, adj_cell) in self.open:
                        if adj_cell.cost > cell.cost + 1:
                            self._update_cell(adj_cell, cell)
                    else:
                        self._update_cell(adj_cell, cell)
                        heappush(self.open, (adj_cell.impact, adj_cell))

    def cells_in_range(self, num_moves):
        heappush(self.open, (self.start.cost, self.start))
        while any(cost <= num_moves for cost, cell in self.open):
            cost, cell = heappop(self.open)
            self.in_range.add(cell)
            adj_cells = self._get_adjacent(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.in_range:
                    if (adj_cell.cost, adj_cell) in self.open:
                        if adj_cell.cost > cell.cost + 1:
                            self._update_cell(adj_cell, cell)
                    else:
                        self._update_cell(adj_cell, cell)
                        heappush(self.open, (adj_cell.cost, adj_cell))

        return self.in_range

    def draw(self):
        for row in self.cells:
            line = []
            for cell in row:
                line.append(self._draw_cell(cell))
            print(''.join(line))


class Test_Day13(unittest.TestCase):
    def setUp(self):
        self.maze = Maze(size=(10, 7), destination=(7, 4), seed=10)

    def test_one_bits(self):
        self.assertEqual(1, one_bits(2))
        self.assertEqual(3, one_bits(50))
        self.assertEqual(10, one_bits(509281))

    def test_is_wall(self):
        self.assertTrue(self.maze.is_wall(1, 0))
        self.assertTrue(self.maze.is_wall(3, 0))
        self.assertTrue(self.maze.is_wall(5, 1))
        self.assertTrue(self.maze.is_wall(9, 6))
        self.assertTrue(self.maze.is_wall(-1, 6))
        self.assertTrue(self.maze.is_wall(9, -1))

    def test_is_not_wall(self):
        self.assertFalse(self.maze.is_wall(0, 0))
        self.assertFalse(self.maze.is_wall(0, 1))
        self.assertFalse(self.maze.is_wall(2, 0))
        self.assertFalse(self.maze.is_wall(1, 1))
        self.assertFalse(self.maze.is_wall(5, 5))

    def test_solve(self):
        self.maze.solve()
        self.assertEqual(11, len(self.maze.path))

    def test_cells_in_range(self):
        cells_in_range = len(self.maze.cells_in_range(4))
        self.assertEqual(9, cells_in_range)


if __name__ == '__main__':
    main()
