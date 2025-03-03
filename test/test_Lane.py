import pytest
import os
import sys
from simpy import Environment

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.TrafficControl import Lane,TrafficControl, Direction, Car

def print_green(message):
    """Helper function to print text in green."""
    print(f"\033[92m{message}\033[0m")

def test_trafficcontrol_initialization():
    side_length = 0.1
    sim_length = 360
    sim_time_unit = 0.01 # from TrafficControl - NOT PASSED AS PARAMETER
    car_speed = 30
    car_length = 5
    realistic_length_fluctuation = 0
    car_stationary_distance = 2
    car_reaction_time = 1
    num_general_lanes = 2
    general_vph = [[0,0,60], [0,0,60], [0,0,60], [0,0,60]]
    has_left_turn_lanes = True
    has_right_turn_lanes = True
    has_pedestrian_crossings = True
    crossing_pedestrian_time = 30
    crossing_requests_per_hour = 60
    traffic_light_sequence = [Direction.North, Direction.East, Direction.South, Direction.West]
    traffic_light_green_times = [30, 30, 30, 30]
    
    special_length = 10
    special_speed = 20
    special_realistic_length_fluctuation = 1.5
    has_special_vehicle_lane = True
    special_vehicle_ratio = 0.2
    special_vph = [[0,0,60], [0,0,60], [0,0,60], [0,0,60]]

    traffic_control = TrafficControl(
        side_length, sim_length, car_speed, car_length, realistic_length_fluctuation, car_stationary_distance,
        car_reaction_time, num_general_lanes, general_vph, has_left_turn_lanes, has_right_turn_lanes,
        has_pedestrian_crossings, crossing_pedestrian_time, crossing_requests_per_hour,
        traffic_light_sequence, traffic_light_green_times, special_length, special_speed,special_realistic_length_fluctuation,
        has_special_vehicle_lane, special_vehicle_ratio, special_vph
    )

    return traffic_control

def test_lane_initialization():
    # Initialize TrafficControl
    test_trafficcontrol_initialization()

    # test initialization of Lane class
    junction_entrance = Direction.North
    is_special_lane = False
    lane = Lane(junction_entrance, is_special_lane)

    # verify that lane is initialized correctly
    assert lane.leadingCar is None
    assert lane.trailingCar is None
    assert lane.numberOfCarsPresent == 0
    assert lane.totalWaitingTime == 0
    assert lane.numberOfVehiclesPassed == 0
    assert lane.maxWaitingTime == -1
    assert lane.maxQueueLength == -1
    assert lane.isGreen is False
    assert lane.junctionEntrance == junction_entrance
    assert lane.isSpecialLane == is_special_lane
    assert lane.timeUntilJunctionClear == 0

    print_green("test_lane_initialization: Test Passed")



def test_lane_add_car():
    test_trafficcontrol_initialization()

    # adding car to lane
    env = Environment()
    junction_entrance = Direction.North
    is_special_lane = False
    lane = Lane(junction_entrance, is_special_lane)

    lane.addCar(Direction.West, True, env)

    # verify correct adding
    assert lane.numberOfCarsPresent == 1
    assert lane.leadingCar is not None
    assert lane.trailingCar is not None
    assert lane.leadingCar == lane.trailingCar
    assert lane.maxQueueLength == 1

    # add another car to lane
    lane.addCar(Direction.East, True, env)

    # verify correct adding of second car
    assert lane.numberOfCarsPresent == 2
    assert lane.leadingCar != lane.trailingCar
    assert lane.maxQueueLength == 2

    print_green("test_lane_add_car: Test Passed")



def test_lane_leading_car_entering_junction():
    test_trafficcontrol_initialization()

    # test leading car entering the junction
    env = Environment()
    junction_entrance = Direction.North
    is_special_lane = False
    lane = Lane(junction_entrance, is_special_lane)

    # add two cars
    lane.addCar(Direction.West, True, env)
    lane.addCar(Direction.East, True, env)

    # simulate leading car entering junction
    env_time = env.now
    lane.leadingCarEnteringJunction(env_time)

    # verify that the leading car has entered the junction
    assert lane.numberOfCarsPresent == 1
    assert lane.numberOfVehiclesPassed == 1
    assert lane.totalWaitingTime == env_time - lane.leadingCar.timeOfQueueStart
    assert lane.maxWaitingTime == env_time - lane.leadingCar.timeOfQueueStart

    # sim a second car entering the junction
    env_time_2 = env.now + 10  # later time
    lane.leadingCarEnteringJunction(env_time_2)

    # verify secnd car entered junction
    assert lane.numberOfCarsPresent == 0
    assert lane.numberOfVehiclesPassed == 2

    print_green("test_lane_leading_car_entering_junction: Test Passed")



def test_lane_add_special_vehicle():
    test_trafficcontrol_initialization()

    env = Environment()
    junction_entrance = Direction.North
    is_special_lane = True
    lane = Lane(junction_entrance, is_special_lane)


    # add special vehicle
    lane.addCar(Direction.West, False, env)

    # verify special vehicle added correctly
    assert lane.numberOfCarsPresent == 1
    assert lane.leadingCar is not None
    assert lane.trailingCar is not None
    assert lane.leadingCar == lane.trailingCar
    assert lane.maxQueueLength == 1

    # verify special vehicle speed is correct
    assert lane.leadingCar.speed == TrafficControl.specialSpeed

    print_green("test_lane_add_special_vehicle: Test Passed")

def test_lane_time_until_junction_clear():
    test_trafficcontrol_initialization()

    # adding car before timeUntilJunctionClear calculation
    env = Environment()
    junction_entrance = Direction.North
    is_special_lane = False
    lane = Lane(junction_entrance, is_special_lane)
    lane.addCar(Direction.West, True, env)

    # store cars speed (pointer set to None after entering junction)
    car_speed = lane.leadingCar.speed

    # sim leading car entering junction
    env_time = env.now
    lane.leadingCarEnteringJunction(env_time)

    # verify timeUntilJunctionClear is correct
    index_of_transfer_distance = ((Direction.West - Direction.North) % 4) - 1
    expected_time = TrafficControl.transferDistances[index_of_transfer_distance] / car_speed
    assert lane.timeUntilJunctionClear == expected_time

    print_green("test_lane_time_until_junction_clear: Test Passed")

test_lane_initialization()
test_lane_add_car()
test_lane_leading_car_entering_junction()
test_lane_add_special_vehicle()
test_lane_time_until_junction_clear()