#!/usr/bin/env python3
"""Runs a simulation of Conway's game of life.

This module uses data from 'sample_data.p' by default. New boards can be created by
using create_board.py and run by using the '-b [name]' flag. If 'sample_data.p' has
been deleted, or if the board entered is not found, a randomly generated 20x20 board
will be used instead.

List of flags:
-b [name]       loads a board of that name
-w              wraps the board instead of having strict edges
-d              loads the board in debug mode
"""

import os
import pickle
import random
import sys
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


def get_flags():
    """Get and set the flags given in 'sys.argv'."""
    wrap_mode = False
    debug_mode = False
    board_name = "sample_board.p"

    for i, arg in enumerate(sys.argv):
        if arg == "-w":
            wrap_mode = True
        elif arg == "-d":
            debug_mode = True
        elif arg == "-b":
            try:
                board_name = sys.argv[i+1]
            except IndexError:
                print("Invalid board name. Reverting to 'sample_board.p'.")
                time.sleep(2)

    if wrap_mode == True:
        print("Will wrap.")
        time.sleep(1)

    if debug_mode == True:
        print("Booting to debug mode...")
        time.sleep(2)

    return wrap_mode, debug_mode, board_name


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


wrap_mode, debug_mode, board_name = get_flags()
board = open_board(board_name)

game = Screen(board, wrap=wrap_mode, debug=debug_mode)

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
