#!/usr/local/bin/python3

# Too slow (have not finished) with large pizzas
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


def get_shapes():
    subset = it.product(range(1, max_cells + 1), repeat=2)
    subset = [i for i in subset if i[0] * i[1] <= max_cells and i[0] * i[1] >= 2 * min_ingredients]
    subset = [i for i in subset if i[0] <= rows and i[1] <= columns]
    return sorted(subset)


def cut_slice(start_row, start_column, end_row, end_column):
    if end_row < rows and end_column < columns:
        return pizza[start_row:end_row + 1, start_column:end_column + 1]
    return pizza


def get_corners(slices):
    corners = [(0, 0)]
    slice_corners = [(slice[0], slice[1]) for slice in slices]
    for slice in slices:
        corners += [(slice[0], slice[3] + 1)]
        corners += [(slice[2] + 1, slice[1])]
    corners = [corner for corner in corners if corner not in slice_corners]
    corners = [corner for corner in corners if corner[0] < rows and corner[1] < columns]

    return(corners)


def get_points(slices):
    points = [(i[2] - i[0] + 1) * (i[3] - i[1] + 1) for i in slices]
    return sum(points)


def add_slice(slices, shapes):
    corners = get_corners(slices)
    corner = min(corners)
    for shape in shapes:
        slice = cut_slice(corner[0], corner[1], corner[0] + shape[0] - 1, corner[1] + shape[1] - 1)
        if test_slice(slice):
            slices += [(corner[0], corner[1], corner[0] + shape[0] - 1, corner[1] + shape[1] - 1)]
            if get_points(slices) == rows * columns:
                print(len(slices))
                for sliced in slices:
                    print(''.join(str(cor) + ' ' for cor in sliced))
                return slices
            add_slice(slices, shapes)
    del slices[-1]


def main():
    slices = []
    shapes = get_shapes()
    print('Shapes: ', shapes)
    add_slice(slices, shapes)


if __name__ == "__main__":

    f = open('c_medium.in', 'r')
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
    main()
