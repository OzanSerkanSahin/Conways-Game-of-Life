#!/usr/bin/env python3

import random
import os
import time
import math
import pickle
import sys


# Game of Life begins here


def cell_state_current(state, cell):
    s = {cell}
    return s.issubset(state)


def cell_state_next(state_prev, cell):
    neigbours = cell_neighbour_get(cell)
    living_neigbours = 0
    for n in neigbours:
        if cell_state_current(state_prev, n):
            living_neigbours += 1
    if living_neigbours == 3:
        return True
    elif living_neigbours == 2 and cell_state_current(state_prev, cell) == 1:
        return True
    else:
        return False


def cell_neighbour_get(cell):
    out = []
    corner = (cell[0] - 1, cell[1] - 1)
    for i in range(9):
        if i == 4:
            continue
        out.append((corner[0] + (i % 3), corner[1] + (int(i / 3))))
    return out


def state_next(state_prev):
    to_check = set()
    state_next = set()
    for cell in state_prev:
        neighbours = cell_neighbour_get(cell)
        to_check.update(neighbours)
        to_check.add(cell)
    for cell in to_check:
        if cell_state_next(state_prev, cell):
            state_next.add(cell)
    return state_next


# Core of The Game of Life ends here

# Printing and misc functions


def state_random(corner1, corner2):
    (corner1, corner2) = normalise_corner(corner1, corner2)
    h = corner2[1] - corner1[1]
    w = corner2[0] - corner1[0]
    state = set()
    for row in range(h):
        for col in range(w):
            if random.randint(0, 1) == 1:
                state.add((corner1[0] + col, corner1[1] + row))
    return state


def normalise_corner(corner1, corner2):
    c1 = (min(corner1[0], corner2[0]), min(corner1[1], corner2[1]))
    c2 = (max(corner1[0], corner2[0]), max(corner1[1], corner2[1]))
    return (c1, c2)


def state_print(state, corner1, corner2):
    (corner1, corner2) = normalise_corner(corner1, corner2)
    h = corner2[1] - corner1[1]
    w = corner2[0] - corner1[0]
    screen = []
    for i in range(h):
        screen.append([0] * w)

    for cell in state:
        cell_x = cell[0]
        cell_y = cell[1]
        if (cell_x >= corner1[0] and cell_x < corner2[0]) and (
            cell_y >= corner1[1] and cell_y < corner2[1]
        ):
            cell_in_screen_x = cell_x - corner1[0]
            cell_in_screen_y = cell_y - corner1[1]
            screen[cell_in_screen_y][cell_in_screen_x] = 1
    for row in screen:
        for cell in row:
            if cell == 0:
                print(".", end="")
            else:
                print("#", end="")
        print("")


def clearConsole():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"
    os.system(command)


def terminal_cords():
    size = os.get_terminal_size()
    h = size.lines - 1
    w = size.columns - 1
    c1 = (-math.floor(w / 2), -math.floor(h / 2))
    c2 = (math.ceil(w / 2), math.floor(h / 2))
    return (c1, c2)


def run_n(n, start):
    state = state_next(start)
    for i in range(n - 1):
        state = state_next(state)
        clearConsole()
        (c1, c2) = terminal_cords()
        state_print(state, c1, c2)
        time.sleep(0.1)


# Functions end here, and the part that runs them start.

(c1, c2) = terminal_cords()

args = {}
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-f":
        args["file"] = sys.argv[i + 1]
    elif sys.argv[i] == "-t":
        args["turns"] = sys.argv[i + 1]

# If no file is provided, create a random state half the length and width of the initial terminal
state = set()
if "file" in args:
    state = pickle.load(open(args["file"], "rb"))
else:
    state = state_random(
        ((int(c1[0] / 2)), int(c1[1] / 2)), (int((c2[0] / 2)), int(c2[1] / 2))
    )

run_n(int(args.get("turns", 300)), state)

# A small project I made
# https://github.com/OzanSerkanSahin
# https://www.linkedin.com/in/ozan-serkan-sahin/
