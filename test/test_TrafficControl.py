import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.TrafficControl import TrafficControl, Direction


# NOTE: Static testing for junctionTimeManager: Dynamic testing not suitable
# due to dynamic behaviour of class as reliant on JunctionEntrance, which has randomness 
# Static testing will include: verifying light sequence, pedestrian crossing (True and False), sim end time, edge case inputs


def print_green(message):
    print(f"\033[92m{message}\033[0m")


# Test initialization of TrafficControl with valid parameters and simulation setup
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

    # Verify that the instance variables are set correctly
    # try:
    assert traffic_control.sideLengthOfJunction == side_length
    assert traffic_control.lengthOfSim == (sim_length / sim_time_unit)
    assert TrafficControl.carSpeed == car_speed * 0.44704 * TrafficControl.simulationTimeUnit # integer from TrafficControl
    assert TrafficControl.carLength == car_length
    assert TrafficControl.carStationaryDistance == car_stationary_distance
    assert TrafficControl.carReactionTime == car_reaction_time / sim_time_unit
    assert TrafficControl.numberOfGeneralLanes == num_general_lanes
    assert TrafficControl.generalVPH == general_vph
    assert TrafficControl.hasLeftTurnLanes == has_left_turn_lanes
    assert TrafficControl.hasRightTurnLanes == has_right_turn_lanes
    assert traffic_control.hasPedestrianCrossings == has_pedestrian_crossings
    assert traffic_control.crossingPedestrianTime == crossing_pedestrian_time / sim_time_unit
    assert traffic_control.crossingRequestsPerHour == crossing_requests_per_hour

    assert TrafficControl.specialLength == special_length
    assert TrafficControl.specialSpeed == special_speed * 0.44704 * sim_time_unit
    assert TrafficControl.hasSpecialVehicleLane == has_special_vehicle_lane
    assert TrafficControl.specialVehicleRatio == special_vehicle_ratio
    assert TrafficControl.specialVPH == special_vph

    print_green("test_trafficcontrol_initialization: Test Passed")

    # except AssertionError as e:
    #     print("Failed initialization test")

    # try:
    assert len(traffic_control.junctionEntrances) == 4
    assert all(entrance.cardinalDirectionOfJunctionEntrance in Direction for entrance in traffic_control.junctionEntrances)

    #Verify each junctionEntrance has correct no. of lanes
    for entrance in traffic_control.junctionEntrances:
        assert len(entrance.generalLanes) == num_general_lanes
        if TrafficControl.hasSpecialVehicleLane:
            assert entrance.specialLane is not None
        else:
            assert entrance.specialLane is None

    print_green("test_trafficcontrol_simulation_setup: Test Passed")
    # except AssertionError as e:
    #     print("Failed simulation setup test")

# Test the conversion methods
def test_trafficcontrol_time_conversion():
    seconds = 60
    time_units = TrafficControl.convertSecondsToTimeUnits(seconds)
    assert time_units == seconds / TrafficControl.simulationTimeUnit

    converted_back = TrafficControl.convertTimeUnitsToSeconds(time_units)
    assert converted_back == seconds

    print_green("test_trafficcontrol_time_conversion: Test Passed")


test_trafficcontrol_initialization()
test_trafficcontrol_time_conversion()