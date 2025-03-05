import pytest
import sys
import os
from simpy import Environment

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.TrafficControl import TrafficControl, Direction, Lane, Car, CarState

'''for similair reasons to test_TrafficControl: junctionTimeManager - Static testing for carTimeManager as dynamic testing not suitable'''


def print_green(message):
    """Helper function to print text in green."""
    print(f"\033[92m{message}\033[0m")

def setup_traffic_control():
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

def test_car_initialization():
    setup_traffic_control()

    env = Environment()
    junction_entrance = Direction.North
    lane = Lane(junction_entrance, False)

    car = Car(0, Direction.West, env.now, None, lane)
    
    # verify that car is initialized correctly
    assert car.distanceFromJunctionEntrance == 0
    assert car.turningExitCardinality == Direction.West
    assert car.timeOfQueueStart == env.now
    assert car.length == TrafficControl.carLength
    assert car.speed == TrafficControl.carSpeed
    assert car.currentState == CarState.Stationary
    assert car.pointerToCarAhead is None
    assert car.pointerToCarBehind is None
    assert car.junctionEntranceLane == lane
    
    print_green("test_car_initialization: Test Passed")


def test_car_set_length():
    setup_traffic_control()
    
    env = Environment()
    junction_entrance = Direction.North
    lane = Lane(junction_entrance, False)

    car = Car(0, Direction.West, env.now, None, lane)
    
    new_length = 10
    car.setLength(new_length)

    assert car.length == new_length

    print_green("test_car_set_length: Test Passed")

def test_car_set_speed():
    setup_traffic_control()

    env = Environment()
    junction_entrance = Direction.North
    lane = Lane(junction_entrance, False)

    car = Car(0, Direction.West, env.now, None, lane)

    new_speed = 20
    car.setSpeed(new_speed)

    assert car.speed == new_speed

    print_green("test_car_set_speed: Test Passed")

def test_get_gap_to_car_ahead():
    setup_traffic_control()

    env = Environment()
    junction_entrance = Direction.North
    lane = Lane(junction_entrance, False)

    car_ahead = Car(10, Direction.West, env.now, None, lane)
    car_behind = Car(0, Direction.West, env.now, car_ahead, lane)

    expected_gap = car_behind.distanceFromJunctionEntrance - car_ahead.distanceFromJunctionEntrance - car_ahead.length
    assert car_behind.getGapToCarAhead() == expected_gap

    print_green("test_get_gap_to_car_ahead: Test Passed")


test_car_initialization()
test_car_set_length()
test_car_set_speed()
test_get_gap_to_car_ahead()
