"""Generates a board usable in the conway.py program."""
import os
import pickle
import random

def print_board(cols):
    """Draw a mockup of the board based on the rows entered so far."""
    # Print top row.
    print("\t" + "+ " * (cols + 2))

    # Print middle rows.
    for i, row in enumerate(board):
        s = "{}\t+ ".format(i)

        for char in row:
            if char == 0:
                s += "  "
            else:
                s += "o "

        s += "+"
        print(s)

    # Print bottom row.
    print("\t" + "+ " * (cols + 2))

def print_screen(filename, cols, e):
    """Print the entire program output to the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(filename)
    print()
    print("Enter each row on a new line, using space-separated 0's and 1's.")
    print("(0 represents a dead cell, 1 represents a live cell)")
    print()
    print("Things to know:")
    print("\tuse 'Nx0' or 'Nx1' to create N amounts of that number.")
    print("\t'dup x' duplicates row x.")
    print("\t'rand' randomly assigns 0 or 1 to each character in a row.")
    print("\tAn empty row becomes all 0's.")
    print("\tA row too small or too large will either be padded with 0's "
          "or cut off.")

    print()

    # Update the image with each row added.
    print_board(cols)

    print()
    print("-" * 10)
    print()

    if e is not None:
        print(e)
        print()

def parse_row(i):
    """Get input for a new row and parse its commands."""
    # Split the input into a list of commands.
    commands = input("row {}: ".format(i)).strip().split()

    if not commands:
        return []

    main_command = commands[0].lower()

    if main_command == "dup":
        if len(commands) < 2:
            raise IndexError("Nothing after dup")

        e = "Invalid line number given: {}".format(commands[1])

        try:
            line_number = int(commands[1])
        except ValueError:
            raise ValueError(e)

        if line_number < 0 or line_number >= i:
            raise IndexError(e)

        return board[line_number]

    elif main_command == "rand":
        return [random.choice([0, 1]) for col in range(cols)]

    else:
        row = []

        for command in commands:
            # Check if command is a multiplier.
            if "x" in command:
                e = "Invalid multiplier given: {}".format(command)

                spl = command.split("x", maxsplit=1)

                try:
                    multiplier, char = (int(c) for c in spl)
                except ValueError:
                    raise ValueError(e)

                if char != 0 and char != 1:
                    raise ValueError(e)

                row.extend([char] * multiplier)

            else:
                e = "Invalid number given: {}".format(command)

                try:
                    char = int(command)
                except ValueError:
                    raise ValueError(e)

                if char != 0 and char != 1:
                    raise ValueError(e)

                if char == 0:
                    row.append(0)
                else:
                    row.append(1)

        return row


def get_valid_number(message, min=0):
    """Repeatedly request input until a number greater than the min is given."""
    while True:
        try:
            num = int(input(message))

            if num < min:
                raise ValueError

        except ValueError:
            continue

        else:
            return num


board = []

os.system('cls' if os.name == 'nt' else 'clear')

board_name = input("Name of board: ").strip()

# Convert board name to a valid filename
if board_name[2] == "." and board_name[-1] == "p":
    filename = "boards/" + board_name
else:
    filename = "boards/" + board_name + ".p"

rows = get_valid_number("Number of rows: ", min=1)
cols = get_valid_number("Number of columns: ", min=1)
pad = get_valid_number("Amount of padding: ")

for i in range(rows):
    error = None

    while True:
        print_screen(filename, cols, error)

        try:
            row = parse_row(i)

        except (IndexError, ValueError) as e:
            error = e
            continue

        else:
            break

    # Pad the end of the row to match the given number of columns
    if len(row) < cols:
        row.extend([0] * (cols - len(row)))

    # Use only the first "cols" elements in the row
    board.append(row[:cols])

print_screen(filename, cols, None)

# Pad board. (todo: potentially slow, rewrite using deque)
for r in board:
    for i in range(pad):
        r.insert(0, 0)
        r.append(0)

padding = [0] * (cols + 2 * pad)
for i in range(pad):
    board.insert(0, padding)
    board.append(padding)

with open(filename, "wb") as f:
    pickle.dump(board, f)

print("Saved '{}'.".format(filename))
