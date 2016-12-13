import logging
import os
import re
import unittest

from twentysixteen import INPUTS

BOT_LOG = logging.getLogger(__name__)
BOT_LOG.addHandler(logging.StreamHandler())
BOT_LOG.setLevel(logging.INFO)


def main():
    with open(os.path.join(INPUTS, 'day10.txt'), 'r') as data_file:
        instructions = data_file.readlines()

    bot_room = BotRoom(instructions)
    bot_room.follow_instructions()

    target_pair = [17, 61]
    target_bot = [bot for bot in bot_room.bots.values() if compares_chips(bot, target_pair)]

    if target_bot:
        print("The ID of the bot that "
              "compares chip pair {} is: {}".format(target_pair, target_bot[0].id))

    output_mult = bot_room.outputs['0'] * bot_room.outputs['1'] * bot_room.outputs['2']
    print("The multiplied values of outputs 0, 1, & 2 are: {}".format(output_mult))


def compares_chips(bot, chip_pair):
    return chip_pair in bot.history


class Bot(object):
    def __init__(self, num):
        self.id = num
        self._chips = []
        self.history = []

    def give_chip(self, chip):
        if len(self._chips) == 2:
            BOT_LOG.debug("Bot %s cannot receive chip %s: "
                          "already holding two chips.", self.id, chip)
        elif chip in self.chips:
            BOT_LOG.debug("Bot %s already has chip %s.", self.id, chip)
        else:
            self._chips.append(chip)
            self._chips.sort()

    def get_low(self):
        if len(self._chips) < 2:
            BOT_LOG.debug("Bot %s needs two chips to distribute low.", self.id)
            return None
        low = self._chips[0]
        return low

    def get_high(self):
        if len(self._chips) < 2:
            BOT_LOG.debug("Bot %s needs two chips to distribute high.", self.id)
            return None
        high = self._chips[1]
        return high

    @property
    def chips(self):
        return self._chips


class BotRoom(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.setters = [line.split() for line in self.instructions if line.startswith('value')]
        self.bot_instructions = [line.split() for line in self.instructions if
                                 line.startswith('bot')]

        self.bots = {}
        self.outputs = {}
        self.init_bots()

    def init_bots(self):
        bot_id_pattern = re.compile(r'bot\s(\d+)')
        for line in self.instructions:
            bot_ids = bot_id_pattern.findall(line)
            if bot_ids:
                for bot_id in bot_ids:
                    self.bots[bot_id] = Bot(bot_id)

    def follow_instructions(self):
        self.set_initial_state()
        while not self.bot_state_known():
            self.outputs = {}
            self.exchange_chips()

    def bot_state_known(self):
        return all(bot.history for bot in self.bots.values())

    def set_initial_state(self):
        for line in self.setters:
            value = int(line[1])
            dest = line[-2]
            dest_id = line[-1]
            if dest == 'bot':
                self.bots[dest_id].give_chip(value)
            if dest == 'output':
                self.outputs[dest_id] = value

    def exchange_chips(self):
        for line in self.bot_instructions:
            bot_id = line[1]
            bot = self.bots[bot_id]
            bot_low = bot.get_low()
            bot_high = bot.get_high()

            low_dest = line[5]
            low_dest_id = line[6]
            high_dest = line[-2]
            high_dest_id = line[-1]

            if bot_low and bot_high:
                compared = [bot_low, bot_high]
                bot.history.append(compared)
                if low_dest == 'bot':
                    self.bots[low_dest_id].give_chip(bot_low)
                elif low_dest == 'output':
                    self.outputs[low_dest_id] = bot_low

                if high_dest == 'bot':
                    self.bots[high_dest_id].give_chip(bot_high)
                elif high_dest == 'output':
                    self.outputs[high_dest_id] = bot_high


TEST_INSTRUCTIONS = [
    "value 5 goes to bot 2",
    "bot 2 gives low to bot 1 and high to bot 0",
    "value 3 goes to bot 1",
    "bot 1 gives low to output 1 and high to bot 0",
    "bot 0 gives low to output 2 and high to output 0",
    "value 2 goes to bot 2"
]


class Test_Day10(unittest.TestCase):
    def test_follow_instructions(self):
        bot_room = BotRoom(TEST_INSTRUCTIONS)
        bot_room.follow_instructions()
        self.assertTrue(compares_chips(bot_room.bots['2'], [2, 5]))


if __name__ == '__main__':
    main()
