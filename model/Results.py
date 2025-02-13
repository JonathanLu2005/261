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

        self.print_results()

    def print_results(self):
        print(f"North Junction: Max Waiting Time = {self.northMaxWaitingTime}, Max Queue Length = {self.northMaxQueueLength}, "
              f"Avg Waiting Time = {self.northAvgWaitingTime}, Total Vehicles Passed = {self.northTotalVehiclesPassed}")
        
        print(f"East Junction: Max Waiting Time = {self.eastMaxWaitingTime}, Max Queue Length = {self.eastMaxQueueLength}, "
              f"Avg Waiting Time = {self.eastAvgWaitingTime}, Total Vehicles Passed = {self.eastTotalVehiclesPassed}")
        
        print(f"South Junction: Max Waiting Time = {self.southMaxWaitingTime}, Max Queue Length = {self.southMaxQueueLength}, "
              f"Avg Waiting Time = {self.southAvgWaitingTime}, Total Vehicles Passed = {self.southTotalVehiclesPassed}")
        
        print(f"West Junction: Max Waiting Time = {self.westMaxWaitingTime}, Max Queue Length = {self.westMaxQueueLength}, "
              f"Avg Waiting Time = {self.westAvgWaitingTime}, Total Vehicles Passed = {self.westTotalVehiclesPassed}")

# This is the function that the front-end calls to get results of a simulation
def runModel(sideLengthOfJunction, lengthOfSim, simulationSecondLength, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes):
    simulation = TrafficControl(sideLengthOfJunction, lengthOfSim, simulationSecondLength, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes)
    
    while not simulation.simulationComplete:
        time.sleep(0.5)

    return Results(simulation)


runModel(15, 300, 1, 15, 3, 1, 2, 2, None, None, None, None, [Direction.North, Direction.East, Direction.South, Direction.West], [10,60,30,60])