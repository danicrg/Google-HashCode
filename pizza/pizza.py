#!/usr/local/bin/python3

import sys
import numpy as np
import itertools as it
import tqdm
import threading
import random


def get_arguments(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    arguments = lines[0].split(' ')
    rows = int(arguments[0])
    columns = int(arguments[1])
    min_ingredients = int(arguments[2])
    max_cells = int(arguments[3])
    pizza = []
    for line in lines[1:]:
        pizza.append(list(line.replace('\n', '')))
    pizza = np.array(pizza)

    return pizza, rows, columns, min_ingredients, max_cells


def get_shapes(sorting_function=lambda i: i[0] * i[1], reverse=True):
    # Returns a list of tuples of all possible shapes in this pizza
    subset = it.product(range(1, max_cells + 1), repeat=2)
    subset = [i for i in subset if i[0] * i[1] <= max_cells and i[0] * i[1] >= 2 * min_ingredients]
    subset = [i for i in subset if i[0] <= rows and i[1] <= columns]
    subset = sorted(subset, key=sorting_function, reverse=reverse)
    return subset


def print_solution(slices):
    f = open(sys.argv[2], 'w')
    f.write(f'{len(slices)}\n')
    for slice in slices:
        f.write(f'{slice[0]} {slice[1]} {slice[0] + slice[2] - 1} {slice[1] + slice[3] - 1}\n')
    f.close()


def get_score(slices):
    points = sum([(i[2] * i[3]) for i in slices])
    return points


def test_slice(slice, pizza_cut):
    r, c, dr, dc = slice
    if dr * dc > max_cells or c + dc > columns or r + dr > rows:
        return False
    tomatos = np.count_nonzero(pizza[r:(r + dr), c:(c + dc)] == ['T'])
    mushrooms = dr * dc - tomatos
    if tomatos < min_ingredients or mushrooms < min_ingredients:
        return False
    if np.all(pizza_cut[r:(r + dr), c:(c + dc)] == '0'):
        return True
    return False


def cut_slice(slice, slices, pizza_cut):
    r, c, dr, dc = slice
    pizza_cut[r:(r + dr), c:(c + dc)] = 1

    slices.append(slice)
    return slices, pizza_cut


def cut_pizza(cells, shapes):
    global winner, winner_score, event
    pizza_cut = np.zeros_like(pizza)
    pizza_cut[:, :] = 0
    slices = []
    for cell in tqdm.tqdm(cells):
        for shape in shapes:
            if test_slice(cell + shape, pizza_cut):
                slices, pizza_cut = cut_slice(cell + shape, slices, pizza_cut)
    score = get_score(slices)
    event.wait()
    event.clear()
    if score > winner_score:
        winner = slices
        winner_score = score
    event.set()


def main():
    cells = set(tuple(args) for args in np.transpose(np.nonzero(pizza)).tolist())
    cells = sorted(cells, key=lambda i: i[1] * (i[1] + i[0]))
    shape_sorting_functions = [lambda i: i[0] * i[1] + i[0], lambda i: i[0] / i[1], lambda i: random.randint(1, 10)]

    threads = []

    for shape_function in shape_sorting_functions:
        shapes = get_shapes(shape_function)
        thread = threading.Thread(target=cut_pizza, args=(cells, shapes))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('\n\nScore: ', winner_score, ' of ', rows * columns)
    print_solution(winner)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: pizza input.in output.out')
    else:
        pizza, rows, columns, min_ingredients, max_cells = get_arguments(sys.argv[1])
        print(str(rows) + ' rows,', str(columns) + ' columns,', str(min_ingredients) + ' minimum ingredients,', str(max_cells) + ' max cells per slice. \n')
        print('Pizza:\n', pizza, '\n')
        winner = []
        winner_score = 0
        event = threading.Event()
        event.set()
        main()
