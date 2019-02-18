#!/usr/local/bin/python3

import sys
import numpy as np
import itertools as it

f = open('a_example.in', 'r')
lines = f.readlines()
arguments = lines[0].split(' ')

# arguments
rows = int(arguments[0])
columns = int(arguments[1])
min_ingredients = int(arguments[2])
max_cells = int(arguments[3])

print(str(rows) + ' rows,', str(columns) + ' columns,', str(min_ingredients) + ' minimum ingredients,', str(max_cells) + ' max cells per slide.')

pizza = []
for line in lines[1:]:
    pizza.append(list(line.replace('\n', '')))
pizza = np.array(pizza)

# Create subsets

column_subsets = []
row_subsets = []
big = max(rows, columns)

print('Calculating arrangements...')

for subset in it.product(range(0, big), repeat=big):
    subset = list(filter(lambda a: a != 0, list(subset)))
    if sum(subset) == rows:
        row_subsets.append(subset)
    if sum(subset) == columns:
        column_subsets.append(subset)

row_subsets = np.unique(row_subsets).tolist()
column_subsets = np.unique(column_subsets).tolist()

print('Trying %i pizzas...' % (len(row_subsets) * len(column_subsets)))

prev_row = 0
prev_column = 0
breaker = False
for row_subset in row_subsets:
    for column_subset in column_subsets:
        counter = []
        for row in row_subset:
            for column in column_subset:
                if column * row <= max_cells:
                    slice = pizza[prev_row:(prev_row + row), prev_column:prev_column + column]
                    prev_column = prev_column + column
                    tomatos = np.count_nonzero(slice == ['T'])
                    mushrooms = np.count_nonzero(slice == ['M'])
                    if tomatos < min_ingredients or mushrooms < min_ingredients:
                        breaker = True
                        counter = []
                        break
                    counter.append(column * row)
                else:
                    breaker = True
                    counter = []
                    break
            prev_column = 0
            prev_row = prev_row + row
            if breaker:
                break
        prev_column = 0
        prev_row = 0
        if len(counter) != 0 and sum(counter) == rows * columns:
            print(counter)

print('finished')
