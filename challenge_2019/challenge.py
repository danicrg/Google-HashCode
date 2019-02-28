#!/usr/local/bin/python3
from profiler import profile


@profile
def main():
    cases = int(f.readline())


if __name__ == '__main__':
    f = open('a_example.in', 'r')
    output = open('a_example.out', 'w')
    main()
