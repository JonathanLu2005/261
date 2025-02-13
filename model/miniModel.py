import simpy
import random

LANE_LENGTH = 100  # length of each lane in meters
CAR_LENGTH = 5  # length of each car in meters
CAR_SPEED = 10  # speed of each car in m/s
JUNCTION_TRAVEL_LENGTH = 10  # length of the junction in meters
LANES = 4
JUNCTION_SPACE = round(JUNCTION_TRAVEL_LENGTH / (CAR_LENGTH + 1)) * LANES  # number of car spaces in the junction
VPH = 800


# README: Loosely followed design, currently generates 4 lanes with cars spawning based on vph


def range_vph(vph):
    vps = 3600 / vph
    return [vps - (vps*0.2), vps + (vps*0.2)]



class Car:
    def __init__(self, env, name, light_state, queue_position, junction, queue_position_var):
        self.env = env
        self.name = name
        self.light_state = light_state
        self.queue_position = queue_position
        self.junction = junction
        self.queue_position_var = queue_position_var
        self.action = env.process(self.run())

    def run(self):
        # calculate travel time to the junction
        travel_distance = LANE_LENGTH - (self.queue_position * CAR_LENGTH)
        travel_time = travel_distance / CAR_SPEED
        print(f"{self.name} starts at time {self.env.now}, will take {travel_time} seconds to reach the junction")

        # simulate travel to the junction
        yield self.env.timeout(travel_time)
        print(f"{self.name} arrives at the junction at time {self.env.now}")

        # record the arrival time
        arrival_time = self.env.now

        # wait for the light to turn green and for space in junction
        with self.junction.request() as req:
            yield req
            while not self.light_state["green"]:
                yield self.env.timeout(1)  # check every second

            # calculate waiting time
            waiting_time = self.env.now - arrival_time
            print(f"{self.name} starts crossing at time {self.env.now} (waited for {waiting_time} seconds)")

            # decrement the queue position
            self.queue_position_var[0] -= 1
          
            # simulate crossing the junction
            yield self.env.timeout(4)  # crossing time
            print(f"{self.name} leaves at time {self.env.now}")




class JunctionEntrance:
    def __init__(self, env, light_state, queue_position_var):
        self.env = env
        self.light_state = light_state
        self.queue_position_var = queue_position_var
        self.action = env.process(self.run())

    def run(self):
        # alternate between green and red ---- TODO: all lights green at once, and red at once
        while True:
            print(f"light turns green at time {self.env.now}")
            self.light_state["green"] = True  # set light to green
            yield self.env.timeout(20)  # green light duration

            print(f"light turns red at time {self.env.now}")
            self.light_state["green"] = False  # set light to red
            yield self.env.timeout(20)  # red light duration

            # After the light turns green, cars leave based on queue position
            if self.light_state["green"]:
                for i in range(self.queue_position_var[0]):
                    yield self.env.timeout(0.5 * (i + 1))  # wait time based on queue position




class TrafficControl:
    def __init__(self, env, junction, direction):
        self.env = env
        self.junction = junction
        self.direction = direction
        self.light_state = {"green": False}
        self.queue_position_var = [0]
        self.traffic_light = JunctionEntrance(env, self.light_state, self.queue_position_var)
        self.action = env.process(self.run())

    def run(self):
        rate = range_vph(VPH)
        for i in range(20): #spawns 20 cars
            Car(self.env, f"car {i+1} ({self.direction})", self.light_state, self.queue_position_var[0], self.junction, self.queue_position_var)
            self.queue_position_var[0] += 1
            yield self.env.timeout(random.randint(int(rate[0]), int(rate[1])))  # arrival rate - calculated by the VPH



# run the simulation
env = simpy.Environment()
junction = simpy.Resource(env, capacity=JUNCTION_SPACE) # TODO: Currently junction * no. of lanes -- not optimised (i.e. 1 lane can take up all spaces in junction)

# Create traffic controls for each direction
directions = ['north', 'south', 'east', 'west'] 
for direction in directions:
    TrafficControl(env, junction, direction)

env.run(until=120)  # run for 120 seconds (time units)
