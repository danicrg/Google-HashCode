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


def get_score(input_filename, output_filename):
    input = open(input_filename, 'r')
    R, C, F, N, B, T = list(map(int, input.readline().rsplit()))
    rides = []
    for ride_id in range(N):
        params = list(map(int, input.readline().rsplit()))
        rides.append(Ride(ride_id, params))

    output = open(output_filename, 'r')
    vehicles = output.readlines()
    score = 0
    for vehicle in vehicles:
        vehicle = list(map(int, vehicle.rsplit()))
        time_counter = 0
        vehicle_position = (0, 0)
        for ride_id in vehicle[1:]:
            ride = rides[ride_id]
            distance = ride.get_distance(vehicle_position)
            time_counter += distance
            if time_counter <= ride.earliest_start:
                score += B + ride.get_duration()
                time_counter += ride.earliest_start + ride.get_duration()
            else:
                time_counter += ride.get_duration()
                if time_counter <= ride.latest_finish:
                    score += ride.get_duration()
    return score


get_score('input/a_example.in', 'testOutput.txt')
