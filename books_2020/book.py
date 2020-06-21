import os
import tqdm as tqdm
from statistics import median


def get_score(l_books, book_scores, M, T):
    score = 0
    for book in l_books:

        score += book_scores[book]

    return score / (len(l_books) / (20 * M) + 20 * T)


def sort_libraries(scanned, left_libraries, book_scores, total_order):
    if len(left_libraries) == 1:
        return total_order
    left_libraries.sort(reverse=True)
    best_library = left_libraries[0]

    total_order.append(best_library)
    new_left_libraries = []
    scanned.extend(best_library[-1])
    NEW_SCANNED = scanned

    for lib in left_libraries[1:]:
        new_books = [x for x in lib[-1] if x not in NEW_SCANNED]
        new_left_libraries.append((get_score(new_books, book_scores, lib[-2], lib[-3]), lib[1], lib[2], lib[3], lib[4], new_books))

    sort_libraries(NEW_SCANNED, new_left_libraries, book_scores, total_order)


def select_best_books(b, book_scores):
    PERCENTILE = 0.97
    b.sort(key=lambda x: book_scores[x])
    return b[:int(len(b) * PERCENTILE)]


def scan(FILENAME):
    score = 0
    print(FILENAME)
    filename = './input/' + FILENAME
    DAY = 0
    SCANNED = []
    LIBRARIES_COUNT = 0

    f = open(filename, 'r')
    B, L, D = map(int, f.readline().rsplit())
    book_scores = list(map(int, f.readline().rsplit()))

    libraries = list()
    for l in range(L):
        # N number of books
        # T signup time
        # M books/day
        # l_books ID's of books in the library

        N, T, M = map(int, f.readline().rsplit())
        l_books = list(map(int, f.readline().rsplit()))
        score = get_score(l_books, book_scores, M, T)
        libraries.append((score, l, N, T, M, l_books))

    libraries = sort_libraries([], libraries, book_scores, [])

    out = open('./output/tmp', 'w')
    out.write('#\n')
    print('LIBRARIES: ', L)
    for library in libraries:
        if DAY + library[3] < D:
            # print('LIBRARY: ', library[1])

            unscanned = [book for book in select_best_books(library[-1], book_scores) if book not in SCANNED]
            if len(unscanned) == 0:
                continue
            days_left = D - DAY - library[3]

            books_that_fit = days_left * library[4]
            selected_books = unscanned[:books_that_fit]

            out.write('%i %i\n' % (library[1], len(selected_books)))

            SCANNED.extend(selected_books)

            out.write(' '.join([str(i) for i in selected_books]) + '\n')
            LIBRARIES_COUNT += 1
            DAY += library[3]

            score += sum([book_scores[i] for i in selected_books])

    out.close()

    os.system('sed \'s/#/%i/g\' %s > %s' % (LIBRARIES_COUNT, './output/tmp', './output/' + FILENAME))
    os.system('rm ./output/tmp')

    print(score)
    return score


filenames = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']
# filenames = ['a_example.txt', 'c_incunabula.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']

total_score = 0

for f in tqdm.tqdm(filenames):
    total_score += scan(f)

print('TOTAL SCORE: ', total_score)
