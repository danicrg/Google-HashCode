from scoring import get_score
import re
import tqdm


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
    rides = []
    for ride_id in range(N):
        params = list(map(int, input.readline().rsplit()))
        rides.append(Ride(ride_id, params))
    rides = sorted(rides, key=lambda ride: ride.earliest_start)
    to_assign = rides.copy()
    for vehicle in tqdm.tqdm(range(F)):
        pos = (0, 0)
        time_counter = 0
        vehicle_rides = []
        while time_counter <= T and to_assign:

            next_ride = min(to_assign, key=lambda ride: ride.get_distance(pos) + ride.earliest_start)
            time_counter += next_ride.get_distance(pos)
            if time_counter <= next_ride.earliest_start:
                time_counter = next_ride.earliest_start + next_ride.get_duration()

            else:
                time_counter += next_ride.get_duration()

            if time_counter <= T:
                to_assign.remove(next_ride)
                vehicle_rides.append(next_ride)
                pos = next_ride.finish_intersection
            else:
                break

        output.write('{} {}\n'.format(len(vehicle_rides), ' '.join(str(r.id) for r in vehicle_rides)))
    output.close()
    input.close()


if __name__ == "__main__":
    input_filenames = ['input/a_example.in', 'input/c_no_hurry.in', 'input/e_high_bonus.in', 'input/b_should_be_easy.in', 'input/d_metropolis.in']
    total_score = 0
    for input_filename in input_filenames:
        output_filename = 'output/' + re.findall('input/(.*).in', input_filename)[0] + '.out'
        input = open(input_filename, 'r')
        output = open(output_filename, 'w')
        R, C, F, N, B, T = list(map(int, input.readline().rsplit()))
        main()
        score = get_score(input_filename, output_filename)
        total_score += score
        print(input_filename, score)
    print(total_score)
