class SantaMap(object):
    def __init__(self, input_):
        self.movement_list = input_
        self.current_position = [0, 0]
        self.visited_houses = {
            (self.current_position[0], self.current_position[1]): 1
        }
        self.write_map()

    def move(self, direction):
        compass = {
            '^': [1, 0],
            '>': [0, 1],
            'v': [-1, 0],
            '<': [0, -1]
        }

        self.current_position[0] += compass[direction][0]
        self.current_position[1] += compass[direction][1]

    def write_map(self):
        for movement in self.movement_list:
            self.move(movement)
            pos = (self.current_position[0], self.current_position[1])
            if pos in self.visited_houses:
                self.visited_houses[pos] += 1
            else:
                self.visited_houses[pos] = 1


with open('inputs\day03input.txt', 'r') as data_file:
    data = data_file.read()

santa_map = SantaMap(data)
print("In the first year, Santa visits {} houses.".format(len(santa_map.visited_houses)))

data_1 = ''
data_2 = ''

for i, d in enumerate(data):
    if i % 2 == 0:
        data_1 += d
    else:
        data_2 += d

santa_houses = SantaMap(data_1).visited_houses
robosanta_houses = SantaMap(data_2).visited_houses
all_houses = santa_houses.copy()
for house in robosanta_houses:
    if house in all_houses:
        all_houses[house] += robosanta_houses[house]
    else:
        all_houses[house] = robosanta_houses[house]

print("In the second year, Santa and RoboSanta visit {} houses.".format(len(all_houses)))
