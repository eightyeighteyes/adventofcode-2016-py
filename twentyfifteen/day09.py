def make_distance_map(data):
    # load the data into a dict
    distance_map = {origin[0]: {d[1]: int(d[2]) for d in data if d[0] == origin[0]} for origin in data}
    # complete the dict with mutual routes
    for origin, route in distance_map.items():
        for destination, distance in route.items():
            if destination not in distance_map:
                distance_map[destination] = {}
            if origin not in distance_map[destination]:
                distance_map[destination][origin] = distance
    return distance_map


# fuck all this: branch and bound, baby.
class Journey(object):
    def __init__(self, map_, start):
        self.all_routes = []
        self.route = []
        self.map_ = map_
        self.current_position = start
        self.destinations = self.get_destinations()
        self.visited_places = []

    def get_destinations(self):
        destinations = []
        for place, distance in self.map_[self.current_position].items():
            destination = (distance, place)
            destinations.append(destination)

        destinations = sorted(destinations)
        return destinations

    def move(self):
        pass


def crunch_journeys():
    for start in distance_map.keys():
        # find a journey
        journey = Journey(distance_map, start)


with open('inputs/day09input.txt') as data_file:
    data = data_file.readlines()
    data = [d.rstrip('\n').replace('to', '').replace('=', '').split() for d in data]
distance_map = make_distance_map(data)
# make matrix for branch-and-bound




pass
