from score import get_score


class Ride:
    def __init__(self, id, params):
        self.id = id
        self.start_intersection = (params[0], params[1])
        self.finish_intersection = (params[2], params[3])
        self.earliest_start = params[4]
        self.latest_finish = params[5]

    def __repr__(self):
        return str(self.start_intersection) + ' ' + str(self.finish_intersection) + ' ' + str(self.earliest_start) + ' ' + str(self.latest_finish)

    def get_duration(self):
        return abs(self.finish_intersection[0] - self.start_intersection[0]) + abs(self.finish_intersection[1] - self.start_intersection[1])

    def get_distance(self, location):
        """Distance Between a given point and the start intersection of the ride"""
        return abs(location[0] - self.start_intersection[0]) + abs(location[1] - self.start_intersection[1])


def main():
    print(R, C, F, N, B, T)
    rides = []
    for ride_id in range(N):
        params = list(map(int, input.readline().rsplit()))
        rides.append(Ride(ride_id, params))
    rides = sorted(rides, key=lambda ride: ride.earliest_start)

    print(rides)


if __name__ == "__main__":
    input_filename = 'input/a_example.in'
    input = open(input_filename, 'r')
    R, C, F, N, B, T = list(map(int, input.readline().rsplit()))
    main()
