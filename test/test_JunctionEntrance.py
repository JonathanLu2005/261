import pytest
import sys
import os
from simpy import Environment

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.TrafficControl import JunctionEntrance, TrafficControl, Direction, Lane, Car

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

def test_junction_entrance_initialization():
    setup_traffic_control()

    # test initialization of JunctionEntrance class
    junction_entrance = JunctionEntrance(Direction.North)

    # verify junction entrance is initialized correctly
    assert junction_entrance.cardinalDirectionOfJunctionEntrance == Direction.North
    assert junction_entrance.specialLane is not None
    assert len(junction_entrance.generalLanes) == TrafficControl.numberOfGeneralLanes
    assert junction_entrance.timeUntilJunctionIsEmpty == 0

    print_green("test_junction_entrance_initialization: Test Passed")

def test_junction_entrance_add_car():
    setup_traffic_control()

    # test adding car to junction entrance
    env = Environment()
    junction_entrance = JunctionEntrance(Direction.North)
    junction_entrance.generalLanes[0].addCar(Direction.West, True, env)

    # verify car has been added
    assert junction_entrance.generalLanes[0].numberOfCarsPresent == 1
    assert junction_entrance.generalLanes[0].leadingCar is not None
    assert junction_entrance.generalLanes[0].trailingCar is not None

    # add special vehicle to the special lane
    junction_entrance.specialLane.addCar(Direction.West, False, env)

    # verify special vehicle has been added
    assert junction_entrance.specialLane.numberOfCarsPresent == 1
    assert junction_entrance.specialLane.leadingCar is not None
    assert junction_entrance.specialLane.trailingCar is not None

    print_green("test_junction_entrance_add_car: Test Passed")

def test_junction_entrance_traffic_light_signals():
    setup_traffic_control()

    # testing traffic light signals
    env = Environment()
    junction_entrance = JunctionEntrance(Direction.North)

    junction_entrance.generalLanes[0].addCar(Direction.West, True, env)

    # signal green
    junction_entrance.signalGreen()
    assert junction_entrance.generalLanes[0].isGreen is True

    # signal red 
    junction_entrance.signalRed()
    assert junction_entrance.generalLanes[0].isGreen is False

    # add special vehicle to special lane
    junction_entrance.specialLane.addCar(Direction.West, False, env)

    # signal green for special vehicles
    junction_entrance.signalSpecialGreen()
    assert junction_entrance.specialLane.isGreen is True

    # signal red for special vehicles
    junction_entrance.signalSpecialRed()
    assert junction_entrance.specialLane.isGreen is False

    print_green("test_junction_entrance_traffic_light_signals: Test Passed")

def test_junction_entrance_check_if_cars_waiting():
    setup_traffic_control()

    # test checking if cars waiting
    env = Environment()
    junction_entrance = JunctionEntrance(Direction.North)

    # verify that no cars are waiting initially
    assert junction_entrance.checkIfCarsWaiting() is False

    junction_entrance.generalLanes[0].addCar(Direction.West, True, env)

    # verify cars are waiting
    assert junction_entrance.checkIfCarsWaiting() is True

    # special vehicle added to special lane
    junction_entrance.specialLane.addCar(Direction.West, False, env)

    # verify cars still waiting
    assert junction_entrance.checkIfCarsWaiting() is True

    print_green("test_junction_entrance_check_if_cars_waiting: Test Passed")

def test_junction_entrance_statistics():
    setup_traffic_control()

    # test statistics calculation
    env = Environment()
    junction_entrance = JunctionEntrance(Direction.North)

    # add car to general lane
    junction_entrance.generalLanes[0].addCar(Direction.West, True, env)

    # store cars timeOfQueueStart before it enters junction (lose this after)
    car_time_of_queue_start = junction_entrance.generalLanes[0].leadingCar.timeOfQueueStart

    #car enters jucntion
    env_time = env.now
    junction_entrance.generalLanes[0].leadingCarEnteringJunction(env_time)

    # verify stats
    assert junction_entrance.getMaxWaitingTime() == env_time - car_time_of_queue_start
    assert junction_entrance.getMaxQueueLength() == 1
    assert junction_entrance.getAvgWaitingTime() == env_time - car_time_of_queue_start
    assert junction_entrance.getTotalVehiclesPassed() == 1

    # add special behicle to special lane
    junction_entrance.specialLane.addCar(Direction.West, False, env)

    # store special vehicles timeOfQueueStart
    special_car_time_of_queue_start = junction_entrance.specialLane.leadingCar.timeOfQueueStart

    # special vehicle entering junction
    env_time_2 = env.now + 10
    junction_entrance.specialLane.leadingCarEnteringJunction(env_time_2)

    # verify special stats
    # printing expected and actual
    #print(f"Expected: {TrafficControl.convertSecondsToTimeUnits(env_time_2 - special_car_time_of_queue_start)}")
    #print(f"Actual: {junction_entrance.getSpecialMaxWaitingTime()}")
    assert junction_entrance.getSpecialMaxWaitingTime() == TrafficControl.convertTimeUnitsToSeconds(env_time_2 - special_car_time_of_queue_start)
    assert junction_entrance.getSpecialMaxQueueLength() == 1
    assert junction_entrance.getSpecialAvgWaitingTime() == TrafficControl.convertTimeUnitsToSeconds(env_time_2 - special_car_time_of_queue_start)
    assert junction_entrance.getSpecialTotalVehiclesPassed() == 1

    print_green("test_junction_entrance_statistics: Test Passed")



test_junction_entrance_initialization()
test_junction_entrance_add_car()
test_junction_entrance_traffic_light_signals()
test_junction_entrance_check_if_cars_waiting() 
test_junction_entrance_statistics()

