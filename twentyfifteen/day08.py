with open("inputs\day08input.txt", 'r') as data_file:
    data = data_file.readlines()


def count_literals(line):
    return len(line[:-1])


def count_code_characters(line):
    return len(line[:-1])


print(sum(len(s[:-1]) - len(eval(s)) for s in open("inputs\day08input.txt")))
print sum(2 + s.count('\\') + s.count('"') for s in open("inputs\day08input.txt"))
