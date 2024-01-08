#!/usr/bin/python
"""Module for game of Wordly in command line

Keyword arguments:
argument -- description
Return: return_description
"""

import random as r
import sys
import collections as ct
from pathlib import Path
from colorama import Fore, Back, Style

PATH = Path(__file__).parent
DICTIONARY = (PATH  / "five_letters").resolve()
print(DICTIONARY)
MASK = "____"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
colors_dic = {0: Back.LIGHTWHITE_EX, 
              1: Back.YELLOW, 
              2: Back.GREEN, 
              3: Back.MAGENTA,}
CHEAT = "__CHEAT__"
MAX_COUNT = 4


class Wordly:
    """Game of Wordly in command-line interface"""

    def __init__(self):
        self.mask = [0, 0, 0, 0, 0]
        self.dictionary = self._load_dictionary()
        self.word = self._get_word()

    @staticmethod
    def _load_dictionary():
        with open(DICTIONARY, encoding="utf-8") as file:
            lst = [word.strip().upper() for word in file.readlines()]
            return lst

    def _get_word(self):
        return r.choice(self.dictionary)

    def print_color(self, word):
        """print a word in colors in the terminal"""

        for i, char in enumerate(word):
            print(Fore.BLACK + colors_dic[self.mask[i]] + " " + char, end=" ")
        print(Style.RESET_ALL)

    def next_word(self, prompt: str = "Type a 5-letter word\n"):
        """get the user input: 5-letter word

        Keyword arguments:
        prompt -- text
        Return: 5-letter word
        """

        while True:
            try:
                word = input(prompt).upper()
                if word == CHEAT:
                    return word
                if len(word) != 5:
                    raise ValueError("Five letters only!")
                if not all((char in ABC for char in word)):
                    raise ValueError("English letters only!")
                if word not in self.dictionary:
                    raise ValueError("Only existing 5-letter words!")
                return word
            except ValueError as error:
                print(error)
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit()

    def get_mask(self, candidate: str, rng: range):
        """Returns a 'mask' for a candidate word:, i.e list of 5 numbers (0/1/2)
            representing the result of the guess for a particular letter
        Keyword arguments:
        candidate -- a guessing word
        Return: 'mask'
        """

        mask = [0, 0, 0, 0, 0]
        word_dict = dict(ct.Counter(self.word))
        for i in rng:
            if candidate[i] in self.word and word_dict[candidate[i]]:
                word_dict[candidate[i]] -= 1
                if candidate[i] == self.word[i]:
                    mask[i] = 2
                else:
                    mask[i] = 1
            else:
                mask[i] = 0
        return mask

    def start(self):
        """main function of class"""

        for attempt in range(6):
            candidate = self.next_word(f"Attempt {attempt + 1}/6: ")
            if candidate == CHEAT:
                print(self.word)
                candidate = self.next_word(f"Attempt {attempt + 1}/6: ")

            if candidate == self.word:
                self.mask = [2] * (MAX_COUNT + 1)
                self.print_color(candidate)
                print("you win!")
                return
            mask_forward = self.get_mask(candidate, range(MAX_COUNT))
            mask_backward = self.get_mask(candidate, range(MAX_COUNT, -1, -1))

            self.mask = (
                mask_forward
                if sum(mask_forward) >= sum(mask_backward)
                else mask_backward
            )
            self.print_color(candidate)
        print("You lost!")
        self.mask = [3] * (MAX_COUNT + 1)
        self.print_color(self.word)
        print(Style.RESET_ALL)


if __name__ == "__main__":
    game = Wordly()
    game.start()
