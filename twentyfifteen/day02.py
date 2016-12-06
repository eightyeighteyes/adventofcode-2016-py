def surface_area(dimensions):
    l = dimensions[0]
    w = dimensions[1]
    h = dimensions[2]

    return (2 * l * w) + (2 * w * h) + (2 * h * l)


def smallest_side(dimensions):
    l = dimensions[0]
    w = dimensions[1]
    h = dimensions[2]

    if l <= w and l <= h:
        if w <= h:
            return l * w
        else:
            return l * h
    elif w <= l and w <= h:
        if l <= h:
            return w * l
        else:
            return w * h
    elif h <= w and h <= l:
        if w <= l:
            return h * w
        else:
            return h * l


def get_paper_area(dimensions):
    return surface_area(dimensions) + smallest_side(dimensions)


def ribbon_wrap_length(dimensions):
    sorted_dim = sorted([int(i) for i in dimensions])
    return 2 * sorted_dim[0] + 2 * sorted_dim[1]


def bow_ribbon_length(dimensions):
    return reduce(lambda x, y: x * y, dimensions)


def get_ribbon_length(dimensions):
    return ribbon_wrap_length(dimensions) + bow_ribbon_length(dimensions)


with open('inputs\day02input.txt', 'r') as data_file:
    data = data_file.readlines()

data = [d.rstrip().split('x') for d in data]

total_paper = 0
total_ribbon = 0
for d in data:
    d = [int(i) for i in d]
    total_paper += get_paper_area(d)
    total_ribbon += get_ribbon_length(d)

print("Total paper: {}".format(total_paper))
print("Total ribbon: {}".format(total_ribbon))
