#!/usr/bin/env python3
"""Runs a simulation of Conway's game of life.

This module uses data from 'sample_board.p' by default. New boards can
be created using the create_board tool and stored into the boards/ 
folder. If 'sample_board.p' has been deleted, or if the requested board
is not found, a randomly generated 20x20 board will be used instead.
"""

import argparse
import os
import pickle
import random
import time

class Screen:
    """A class to create a game, update it, and print its current state"""

    def __init__(self, init_board, decor="+", alive="o", dead=" ",
                 wrap=False, debug=False):
        """Construct the class, optionally given visuals or debug mode."""
        self.w = len(init_board[0])
        self.h = len(init_board)

        # Add spacing to each symbol for easier printout.
        self.decor = decor + " "
        self.alive = alive + " "
        self.dead = dead + " "

        # Create a two-dimensional list of 0's and 1's.
        self.board = init_board

        self.wrap = wrap

        self.debug = debug

        if self.debug is True:
            self.decor = " # "

    def count_neighbors(self, y, x):
        """Count the number of live neighbors around a given cell."""
        sum = 0

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if self.wrap is False:
                    if x+dx >= 0 and x+dx < self.w and y+dy >= 0 and y+dy < self.h:
                        sum += self.board[y+dy][x+dx]

                else:
                    sum += self.board[(y+dy)%self.h][(x+dx)%self.w]

        # Counteract the extra addition in the for loop.
        sum -= self.board[y][x]

        return sum

    def update_cell(self, y, x):
        """Return the value of a cell's new state according to the rules."""
        cell_state = self.board[y][x]
        neighbors = self.count_neighbors(y, x)

        if cell_state == 0:
            if neighbors == 3:
                return 1
            else:
                return 0
        else:
            if neighbors == 2 or neighbors == 3:
                return 1
            else:
                return 0

    def update(self):
        """Update the entire board."""
        # Deepcopy to ensure that updating early cells can't affect later ones.
        temp = [row[:] for row in self.board]

        for y in range(self.h):
            for x in range(self.w):
                temp[y][x] = self.update_cell(y, x)

        self.board = temp

    def output(self):
        """Output the current board to console."""
        # Print the top row.
        print(self.decor * (self.w + 2))

        # Print the middle rows.
        for y in range(self.h):
            s = ""
            s += self.decor

            for x in range(self.w):
                if self.debug is False:
                    if self.board[y][x] == 0:
                        s += self.dead
                    else:
                        s += self.alive

                else:
                    if self.board[y][x] == 0:
                        s += " {} ".format(self.count_neighbors(y, x))
                    else:
                        s += "[{}]".format(self.count_neighbors(y, x))

            s += self.decor
            print(s)

        # Print the bottom rows.
        print(self.decor * (self.w + 2))


def convert_name(board_name):
    """Convert the given board name into a valid filename."""
    if board_name[-2] == "." and board_name[-1] == "p":
        return "boards/" + board_name
    else:
        return "boards/" + board_name + ".p"


def open_board(board_name):
    """Open the pickle file containing the board (a two-dimensional list)."""
    filename = convert_name(board_name)

    try:
        print("Loading '{}'...".format(filename))
        time.sleep(2)

        with open(filename, "rb") as f:
            board = pickle.load(f)

    except FileNotFoundError:
        print("File '{}' not found, randomly generating...".format(filename))
        time.sleep(2)

        board = [[random.randint(0, 1) for i in range(20)] for j in range(20)]

    return board


def refresh_screen(Screen):
    """Clear the screen and re-print all of the text."""
    if Screen.debug is False:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Enter 'q' or 'quit' to exit the program.")
        print("Enter 'save [name]' to save the initial state to a file.")
        print()

    Screen.output()

    print()


# Parse the command-line arguments
parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__
)

parser.add_argument('-w', '--wrap', action='store_true',
                    help='wrap the game board instead of stopping at edges')
parser.add_argument('-d', '--debug', action='store_true',
                    help='load the game in debug mode')
parser.add_argument('-b', '--board', default='sample_board.p', metavar='NAME',
                    help='look in /boards and load the board of the given name')

args = parser.parse_args()

board = open_board(args.board)
game = Screen(board, wrap=args.wrap, debug=args.debug)

# Run the main game loop until the user exits the program.
while True:
    refresh_screen(game)

    commands = input().lower().split()

    if commands:
        if commands[0] == "quit" or commands[0] == "q":
            break

        elif len(commands) > 1 and commands[0] == "save":
            filename = convert_name(commands[1])

            print("Saving '{}'...".format(filename))
            time.sleep(2)

            with open(filename, "wb") as f:
                pickle.dump(board, f)

            continue

    game.update()

refresh_screen(game)
