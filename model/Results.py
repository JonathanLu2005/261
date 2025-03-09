from TrafficControl import TrafficControl, Direction
import time

class Results:
    def __init__(self, trafficControlInstance):
        self.northMaxWaitingTime = trafficControlInstance.northMaxWaitingTime
        self.northMaxQueueLength = trafficControlInstance.northMaxQueueLength
        self.northAvgWaitingTime = trafficControlInstance.northAvgWaitingTime
        self.northTotalVehiclesPassed = trafficControlInstance.northTotalVehiclesPassed

        self.eastMaxWaitingTime = trafficControlInstance.eastMaxWaitingTime
        self.eastMaxQueueLength = trafficControlInstance.eastMaxQueueLength
        self.eastAvgWaitingTime = trafficControlInstance.eastAvgWaitingTime
        self.eastTotalVehiclesPassed = trafficControlInstance.eastTotalVehiclesPassed

        self.southMaxWaitingTime = trafficControlInstance.southMaxWaitingTime
        self.southMaxQueueLength = trafficControlInstance.southMaxQueueLength
        self.southAvgWaitingTime = trafficControlInstance.southAvgWaitingTime
        self.southTotalVehiclesPassed = trafficControlInstance.southTotalVehiclesPassed

        self.westMaxWaitingTime = trafficControlInstance.westMaxWaitingTime
        self.westMaxQueueLength = trafficControlInstance.westMaxQueueLength
        self.westAvgWaitingTime = trafficControlInstance.westAvgWaitingTime
        self.westTotalVehiclesPassed = trafficControlInstance.westTotalVehiclesPassed


        if (trafficControlInstance.hasSpecialVehicleLane == True):
            self.specialNorthMaxWaitingTime = trafficControlInstance.specialNorthMaxWaitingTime
            self.specialNorthMaxQueueLength = trafficControlInstance.specialNorthMaxQueueLength
            self.specialNorthAvgWaitingTime = trafficControlInstance.specialNorthAvgWaitingTime
            self.specialNorthTotalVehiclesPassed = trafficControlInstance.specialNorthTotalVehiclesPassed

            self.specialEastMaxWaitingTime = trafficControlInstance.specialEastMaxWaitingTime
            self.specialEastMaxQueueLength = trafficControlInstance.specialEastMaxQueueLength
            self.specialEastAvgWaitingTime = trafficControlInstance.specialEastAvgWaitingTime
            self.specialEastTotalVehiclesPassed = trafficControlInstance.specialEastTotalVehiclesPassed

            self.specialSouthMaxWaitingTime = trafficControlInstance.specialSouthMaxWaitingTime
            self.specialSouthMaxQueueLength = trafficControlInstance.specialSouthMaxQueueLength
            self.specialSouthAvgWaitingTime = trafficControlInstance.specialSouthAvgWaitingTime
            self.specialSouthTotalVehiclesPassed = trafficControlInstance.specialSouthTotalVehiclesPassed

            self.specialWestMaxWaitingTime = trafficControlInstance.specialWestMaxWaitingTime
            self.specialWestMaxQueueLength = trafficControlInstance.specialWestMaxQueueLength
            self.specialWestAvgWaitingTime = trafficControlInstance.specialWestAvgWaitingTime
            self.specialWestTotalVehiclesPassed = trafficControlInstance.specialWestTotalVehiclesPassed
        

        self.print_results(trafficControlInstance.hasSpecialVehicleLane) # Comment this out in production

    def print_results(self, isSpecialLane):
        print(f"North Bound Junction Entrance: Max Waiting Time = {self.northMaxWaitingTime}, Max Queue Length = {self.northMaxQueueLength}, "
              f"Avg Waiting Time = {self.northAvgWaitingTime}, Total Vehicles Passed = {self.northTotalVehiclesPassed}")
        
        print(f"East Bound Junction Entrance: Max Waiting Time = {self.eastMaxWaitingTime}, Max Queue Length = {self.eastMaxQueueLength}, "
              f"Avg Waiting Time = {self.eastAvgWaitingTime}, Total Vehicles Passed = {self.eastTotalVehiclesPassed}")
        
        print(f"South Bound Junction Entrance: Max Waiting Time = {self.southMaxWaitingTime}, Max Queue Length = {self.southMaxQueueLength}, "
              f"Avg Waiting Time = {self.southAvgWaitingTime}, Total Vehicles Passed = {self.southTotalVehiclesPassed}")
        
        print(f"West Bound Junction Entrance: Max Waiting Time = {self.westMaxWaitingTime}, Max Queue Length = {self.westMaxQueueLength}, "
              f"Avg Waiting Time = {self.westAvgWaitingTime}, Total Vehicles Passed = {self.westTotalVehiclesPassed}")

        if (isSpecialLane):
            print(f"North Bound Junction Entrance Bus/Cycle: Max Waiting Time = {self.specialNorthMaxWaitingTime}, Max Queue Length = {self.specialNorthMaxQueueLength}, "
                f"Avg Waiting Time = {self.specialNorthAvgWaitingTime}, Total Vehicles Passed = {self.specialNorthTotalVehiclesPassed}")

            print(f"East Bound Junction Entrance Bus/Cycle: Max Waiting Time = {self.specialEastMaxWaitingTime}, Max Queue Length = {self.specialEastMaxQueueLength}, "
                f"Avg Waiting Time = {self.specialEastAvgWaitingTime}, Total Vehicles Passed = {self.specialEastTotalVehiclesPassed}")

            print(f"South Bound Junction Entrance Bus/Cycle: Max Waiting Time = {self.specialSouthMaxWaitingTime}, Max Queue Length = {self.specialSouthMaxQueueLength}, "
                f"Avg Waiting Time = {self.specialSouthAvgWaitingTime}, Total Vehicles Passed = {self.specialSouthTotalVehiclesPassed}")

            print(f"West Bound Junction Entrance Bus/Cycle: Max Waiting Time = {self.specialWestMaxWaitingTime}, Max Queue Length = {self.specialWestMaxQueueLength}, "
                f"Avg Waiting Time = {self.specialWestAvgWaitingTime}, Total Vehicles Passed = {self.specialWestTotalVehiclesPassed}")


# This is the function that the front-end calls to get results of a simulation
def runModel(sideLengthOfJunction, lengthOfSim, carSpeed, carLength, realisticLengthFluctuation, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes, hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes, specialLength, specialSpeed, specialRealisticLengthFluctuation, hasSpecialVehicleLane, specialVehicleRatio, specialVPH):
    simulation = TrafficControl(sideLengthOfJunction, lengthOfSim, carSpeed, carLength, realisticLengthFluctuation, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes,  hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes, specialLength, specialSpeed, specialRealisticLengthFluctuation, hasSpecialVehicleLane, specialVehicleRatio, specialVPH)
    
    while not simulation.simulationComplete:
        time.sleep(0.5)
    
    print("Printing results!")
    return Results(simulation)

"""
    Note to front-end developers, you simply need to call runModel() with all of its paramaters and it will return a Results object which you can pick
    through to get the results gathered from the simulation. (Refer to the definition of the Results class above to know how to do this).

    Parameters will be listed in the order they need to be inputted into runModel:

    sideLengthOfJunction: The side length of the junction in meters. Cannot be less than or equal to 0
    lengthOfSim: The length of the simulation in seconds. For example, if the simulation is 1 hour, this would be 3600. Greater than 0.
    carSpeed: Speed of cars in mph. Greater than 0 and not fractional.
    carLength: Length of cars in meters. Greater or equal to 1.5 meters (can be fracitonal)
    realisticLengthFluctuation: A length in meters representing the range of values which carLength can fluctuate by. Testing team must ensure that carLength - realisticLengthFluctuation >= 1.5 metres.  
    carStationaryDistance: How far the cars are from each other in meters. Greater or equal to 0.5m.
    carReactionTime: The delay car behind takes to respond to the car's changes in speed. Greater or equal to 0.
    numberOfGeneralLanes: Number of general lanes (excluding bus lanes and cycle lanes and currently left turn lanes). Must be at least 1.
    generalVPH: An array of arrays holding the VPH values. It is a 2D array in the form of [[North Bound Traffic Exiting North, North Bound Traffic Exiting East, North Bound Traffic Exiting West], [East Bound Traffic Exiting East, East Bound Traffic Exiting South, East Bound Traffic Exiting North], [South Bound Traffic Exiting South, South Bound Traffic Exiting West, South Bound Traffic Exiting East], [West Bound Traffic Exiting West, West Bound Traffic Exiting North, West Bound Traffic Exiting South]] - Values must be non fractional and greater or equal to 0.
    hasLeftTurnLanes: True or False. If both the junction has both left turn and right turn exclusive lanes, the number of general lanes must be at least 3. 
    hasRightTurnLanes: True or False. If both the junction has both left turn and right turn exclusive lanes, the number of general lanes must be at least 3.
    hasPedestrianCrossings: True or False.
    crossingPedestrianTime: How long pedestrians crossings last for in seconds. Must be greater than 0 strictly and not fractional. This should be None when no crossings occur. The following must hold: (60 / CrossingRequestsPerHour) > crossingPedestrianTime
    crossingRequestsPerHour: The number of pedestrian crossings occuring each hour. Must be greater than 0 and can be fractional. This should be None when no crossings occur. The following must hold: (60 / CrossingRequestsPerHour) > crossingPedestrianTime
    trafficLightSequence: Specify the sequence in which traffic lights should trigger. Example: [Direction.North, Direction.East, Direction.South, Direction.West].
    trafficLightGreenTimes: The following times are in seconds: [Green light time for North Arm, Green light time for East Arm, Green light time for South Arm, Green light time for West arm] This cannot be fractional and must greater than 0.
    specialLength: Length of special vehicle (bus/cycle) in meters. Greater or equal to 1 meter (can be fractional). 
    specialSpeed: Speed of special vehicle (bus/cycle) in mph. Greater than 0 and not fractional.
    specialRealisticLengthFluctuation: A length in meters representing the range of values which carLength can fluctuate by. Testing team must ensure that specialLength - realisticLengthFluctuation >= 1 metre.  
    hasSpecialVehicleLane: True or False. If the user has requested a bus lane or a cycle lane, then this variable should be set to True. The user cannot request bus lanes at the same time as cycle lanes.
    specialVehicleRatio: A float in the interval (0,1]. This represents the ratio of green light time that the buses/cycles will receive - if this is 0.75, then the cars will receive 25% of the green light time specified in trafficGreenLightTimes, and the buses/cycles will receive the other 75%. This number may be 1, but not ever 0 - if this is 0, then hasSpecialLane should be set to False since there is no support for this ratio being 0 and hasSpecialLane being True. 
    specialPVH: Similar to generalVPH, except for buses/cycles instead of Cars. 
"""
#runModel(0.1, 360, 15, 3, 0, 1, 0, 1, [[0,0,0], [0,0,0], [0,0,0], [0,0,0]], False, False, True, 10, 60, [Direction.North, Direction.East, Direction.South, Direction.West], [60,60,60,60], 3, 15, 1.5, True, 1, [[0,0,60], [0,0,60], [0,0,60], [0,0,60]])
runModel(10, 360, 15, 3, 0, 1, 0, 1, [[400,400,400], [400,400,400], [400,400,400], [400,400,400]], False, False, True, 10, 60, [Direction.North, Direction.East, Direction.South, Direction.West], [0,60,60,60], 3, 15, 1.5, False, 0, [[0,0,60], [0,0,60], [0,0,60], [0,0,60]])
# sideLengthOfJunction, lengthOfSim, simulationTimeUnit, carSpeed, carLength, realisticLengthFluctuation, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes,  hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes, specialLength, specialSpeed, specialRealisticLengthFluctuation, hasSpecialVehicleLane, specialVehicleRatio, specialPVH):
