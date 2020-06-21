#!/usr/local/bin/python3
from profiler import profile
import numpy as np
import tqdm
import fuzz
import re


class Photo:
    def __init__(self, id, orientation, number_of_tags, tags):
        self.id = id
        self.orientation = orientation
        self.number_of_tags = int(number_of_tags)
        # self.tags = np.array(tags)
        self.tags = set(tags)


def get_intersection(arr1, arr2):
    # return np.intersect1d(arr1, arr2, assume_unique=True)
    return set.intersection(arr1, arr2)


def get_intersection_score(photo1, photo2):
    arr1, arr2 = photo1.tags, photo2.tags
    intersection_score = len(get_intersection(arr1, arr2))
    return min(photo1.number_of_tags - intersection_score, photo2.number_of_tags - intersection_score, intersection_score)


def get_arguments():
    number_of_photos = int(f.readline())
    vertical_photos = []
    horizontal_photos = []
    for i in range(number_of_photos):
        orientation, number_of_tags, *tags = list(f.readline().rstrip().split(' '))
        if orientation == "H":
            horizontal_photos.append(Photo(int(i), orientation, number_of_tags, tags))
        else:
            vertical_photos.append(Photo(i, orientation, number_of_tags, tags))
    return number_of_photos, horizontal_photos, vertical_photos


def main():
    N, horizontal_photos, vertical_photos = get_arguments()
    # vertical_matrix = np.zeros([N, N], dtype=type([]))

    # for i in vertical_photos:
    #     for j in vertical_photos:
    #         vertical_matrix[i.id][j.id] = np.union1d(i.tags, j.tags)

    vertical_joined = []
    last_photo = []
    for i, v in enumerate(vertical_photos):
        if (i + 1) % 2 == 0:
            union = list(set(list(last_photo.tags) + list(v.tags)))
            horizontal_photos.append(Photo('%i %i' % (last_photo.id, v.id), 'H', len(union), union))
        else:
            last_photo = v

    unused = horizontal_photos.copy()
    slideshow = [horizontal_photos[0]]
    unused.remove(horizontal_photos[0])
    i = 0
    while len(unused) > 0:
        print(i)
        i += 1

        best = 0
        best_photo = 0
        for unused_photo in unused:
            score = get_intersection_score(slideshow[-1], unused_photo)
            if score > 5:
                best_photo = unused.index(unused_photo)
                slideshow.append(unused[best_photo])
                unused.remove(unused[best_photo])
                break
            slideshow.append(unused[-1])
            unused.remove(unused[-1])
    print(len(slideshow))
    output.write('%i\n' % len(slideshow))
    print('\n'.join([str(photo.id) for photo in slideshow]))
    output.write('\n'.join([str(photo.id) for photo in slideshow]))


if __name__ == '__main__':
    input_name = 'input/d_pet_pictures.txt'
    f = open(input_name, 'r')
    output_name = re.findall('input/(.*).txt', input_name)[0]
    output = open('output_dani/%s.out' % output_name, 'w')
    main()

    # a_example.txt           b_lovely_landscapes.txt c_memorable_moments.txt d_pet_pictures.txt      e_shiny_selfies.txt


# np.intersect1d(photos[0].tags, photos[3].tags)
