#!/usr/local/bin/python3

# PROBLEM: ONLY CUTS ALL THE WAY THROUGH

import sys
import numpy as np
import itertools as it


def test_slice(slice):
    if slice.size > max_cells:
        return False
    tomatos = np.count_nonzero(slice == ['T'])
    mushrooms = np.count_nonzero(slice == ['M'])
    if tomatos < min_ingredients or mushrooms < min_ingredients:
        return False
    return True


def cut_pizza(row_subset, column_subset):
    prev_column = 0
    prev_row = 0
    cut = ''
    number_of_slices = 0
    for row in row_subset:
        for column in column_subset:
            slice = pizza[prev_row:(prev_row + row), prev_column:prev_column + column]
            if test_slice(slice):
                cut = cut + ''.join(str(x) + ' ' for x in (prev_row, prev_column, prev_row + row - 1, prev_column + column - 1)) + '\n'
                number_of_slices += 1
            else:
                return
            prev_column = prev_column + column
        prev_column = 0
        prev_row = prev_row + row
    print(str(number_of_slices) + '\n' + str(cut))
    return True


def iterate_cuttings():
    for i in range(1, rows + 1):
        for row_subset in it.product(range(1, max_cells + 1), repeat=i):
            if sum(row_subset) == rows:
                for j in range(1, columns + 1):
                    for column_subset in it.product(range(1, max_cells + 1), repeat=j):
                        if sum(column_subset) == columns:
                            print('trying', row_subset, column_subset)
                            if cut_pizza(row_subset, column_subset):
                                return


if __name__ == "__main__":

    f = open('b_small.in', 'r')
    lines = f.readlines()
    arguments = lines[0].split(' ')

    # arguments
    rows = int(arguments[0])
    columns = int(arguments[1])
    min_ingredients = int(arguments[2])
    max_cells = int(arguments[3])

    print(str(rows) + ' rows,', str(columns) + ' columns,', str(min_ingredients) + ' minimum ingredients,', str(max_cells) + ' max cells per slice. \n')

    pizza = []
    for line in lines[1:]:
        pizza.append(list(line.replace('\n', '')))
    pizza = np.array(pizza)
    print(pizza, '\n')
    iterate_cuttings()
