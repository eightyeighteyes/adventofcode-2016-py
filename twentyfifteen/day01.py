with open('inputs\day01input.txt', 'r') as data_file:
    data = data_file.read()

floor = 0
basement_position = None
for pos, char in enumerate(data):
    if char == '(':
        floor += 1
    if char == ')':
        floor -= 1
        if floor == -1 and basement_position is None:
            basement_position = pos + 1

print("Final floor: {}".format(floor))
print("First position where elevator enters basement: {}".format(basement_position))
