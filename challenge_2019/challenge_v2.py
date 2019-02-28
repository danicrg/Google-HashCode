#!/usr/local/bin/python3
from profiler import profile
import numpy as np
import tqdm
from fuzzywuzzy import fuzz


class Photo:
    def __init__(self, id, orientation, number_of_tags, tags):
        self.id = int(id)
        self.orientation = orientation
        self.number_of_tags = int(number_of_tags)
        # self.tags = np.array(tags)
        self.tags = ' '.join([i for i in tags])


def get_intersection_score(photo1, photo2):
    return fuzz.ratio(photo1.tags, photo2.tags)


def get_arguments():
    number_of_photos = int(f.readline())
    vertical_photos = []
    horizontal_photos = []
    for i in range(number_of_photos):
        orientation, number_of_tags, *tags = list(f.readline().rstrip().split(' '))
        if orientation == "H":
            horizontal_photos.append(Photo(i, orientation, number_of_tags, tags))
        else:
            vertical_photos.append(Photo(i, orientation, number_of_tags, tags))
    return number_of_photos, horizontal_photos, vertical_photos


@profile
def main():
    N, horizontal_photos, vertical_photos = get_arguments()
    # vertical_matrix = np.zeros([N, N], dtype=type([]))

    # for i in vertical_photos:
    #     for j in vertical_photos:
    #         vertical_matrix[i.id][j.id] = np.union1d(i.tags, j.tags)
    unused = horizontal_photos.copy()
    slideshow = [horizontal_photos[0]]
    unused.remove(horizontal_photos[0])
    delta = 0.2
    i = 0
    while len(unused) > 0:
        print(i)
        i += 1
        for unused_photo in unused:
            score = get_intersection_score(slideshow[-1], unused_photo)
            if 0.5 - delta <= score <= 0.5 + delta:
                slideshow.append(unused_photo)
                unused.remove(unused_photo)
                break

        slideshow.append(unused[-1])
        unused.pop(-1)

    print([photo.id for photo in slideshow])

    # fuzz.ratio

    # unused = photos.copy()
    # print(get_intersection_score(photos[0].tags, photos[0].tags))


if __name__ == '__main__':
    f = open('input/c_memorable_moments.txt', 'r')
    output = open('a_example.out', 'w')
    main()


# np.intersect1d(photos[0].tags, photos[3].tags)
