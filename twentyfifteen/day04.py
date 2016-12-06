import hashlib

santa_secret = 'yzbqklnj'


def find_adventcoin_pair(secret, num_zeroes):
    i = 0
    while True:
        hash_ = hashlib.md5(secret + str(i)).hexdigest()
        if hash_.startswith('0' * num_zeroes):
            print "The lowest hashable integer for the key {} is {}.".format(secret, i)
            break
        i += 1


find_adventcoin_pair(santa_secret, 6)
