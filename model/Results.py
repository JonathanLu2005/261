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

        self.print_results() # Comment this out in production

    def print_results(self):
        print(f"North Bound Junction Entrance: Max Waiting Time = {self.northMaxWaitingTime}, Max Queue Length = {self.northMaxQueueLength}, "
              f"Avg Waiting Time = {self.northAvgWaitingTime}, Total Vehicles Passed = {self.northTotalVehiclesPassed}")
        
        print(f"East Bound Junction Entrance: Max Waiting Time = {self.eastMaxWaitingTime}, Max Queue Length = {self.eastMaxQueueLength}, "
              f"Avg Waiting Time = {self.eastAvgWaitingTime}, Total Vehicles Passed = {self.eastTotalVehiclesPassed}")
        
        print(f"South Bound Junction Entrance: Max Waiting Time = {self.southMaxWaitingTime}, Max Queue Length = {self.southMaxQueueLength}, "
              f"Avg Waiting Time = {self.southAvgWaitingTime}, Total Vehicles Passed = {self.southTotalVehiclesPassed}")
        
        print(f"West Bound Junction Entrance: Max Waiting Time = {self.westMaxWaitingTime}, Max Queue Length = {self.westMaxQueueLength}, "
              f"Avg Waiting Time = {self.westAvgWaitingTime}, Total Vehicles Passed = {self.westTotalVehiclesPassed}")

# This is the function that the front-end calls to get results of a simulation
def runModel(sideLengthOfJunction, lengthOfSim, simulationSecondLength, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes, hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes):
    simulation = TrafficControl(sideLengthOfJunction, lengthOfSim, simulationSecondLength, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes,  hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes)
    
    while not simulation.simulationComplete:
        time.sleep(0.5)

    return Results(simulation)

"""
    Note to front-end developers, you simply need to call runModel() with all of its paramaters and it will return a Results object which you can pick
    through to get the results gathered from the simulation. (Refer to the definition of the Results class above to know how to do this).

    Paramaters will be listed in the order they need to be inputted into runModel:

    sideLengthOfJunction: The side length of the junction in meters.
    lengthOfSim: The length of the simulation in seconds. For example, if the simulation is 1 hour, this would be 3600.
    simulationSecondLength: N/A at the moment, doesn't currently do anything yet - may use later.
    carSpeed: Speed of cars in km/h.
    carLength: Length of cars in meters
    carStationaryDistance: How far the cars are from each other in meters.
    carReactionTime: The delay car behind takes to respond to the car's changes in speed.
    numberOfGeneralLanes: Number of general lanes (excluding bus lanes and cycle lanes and currently left turn lanes). Must be at least 2.
    generalVPH: An array of arrays holding the VPH values. It is a 2D array in the form of [[North Bound Traffic Exiting North, North Bound Traffic Exiting East, North Bound Traffic Exiting West], [East Bound Traffic Exiting East, East Bound Traffic Exiting South, East Bound Traffic Exiting North], [South Bound Traffic Exiting South, South Bound Traffic Exiting West, South Bound Traffic Exiting East], [West Bound Traffic Exiting West, West Bound Traffic Exiting North, West Bound Traffic Exiting South]]
    hasLeftTurnLanes: True or False. If both the junction has both left turn and right turn exclusive lanes, the number of general lanes must be at least 3. 
    hasRightTurnLanes: True or False. If both the junction has both left turn and right turn exclusive lanes, the number of general lanes must be at least 3.
    hasPedestrianCrossings: True or False.
    crossingPedestrianTime: How long pedestrians crossings last for in seconds. This should be None when no crossings occur.
    crossingRequestsPerHour: The number of pedestrain crossings occuring each hour. This should be None when no crossings occur
    trafficLightSequence: Specify the sequence in which traffic lights should trigger. Example: [Direction.North, Direction.East, Direction.South, Direction.West].
    trafficLightGreenTimes: The following times are in seconds: [Green light time for North Arm, Green light time for East Arm, Green light time for South Arm, Green light time for West arm]
"""
runModel(15, 3600, 1, 15, 3, 1, 2, 2, [[10,10,10], [10,10,10], [10,10,10], [10,10,10]], False, False, True, 60, 1, [Direction.North, Direction.East, Direction.South, Direction.West], [60,60,60,60])