class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

class TrafficControl:
    # Can declare Static variables here.

    def __init__(self, sideLengthOfJunction, lengthOfSim, simulationSecondLength,
    carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes
    generalVPH, hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour,
    trafficLightSequence, trafficLightGreenTime):
        self.sideLengthOfJunction = sideLengthOfJunction
        self.lengthOfSim = lengthOfSim
        self.simulationSecondLength = simulationSecondLength
        self.carSpeed = carSpeed
        self.carLength = carLength
        self.carStationaryDistance = carStationaryDistance
        self.carReactionTime = carReactionTime
        self.numberOfGeneralLanes = numberOfGeneralLanes
        self.generalVPH = generalVPH
        self.hasPedestrianCrossings = hasPedestrianCrossings
        self.crossingPedestrianTime = crossingPedestrianTime
        self.crossingRequestsPerHour = crossingRequestsPerHour
        self.trafficLightSequence = trafficLightSequence
        self.trafficLightGreenTime = trafficLightGreenTime

        # Init junction class array using Direction Enum.
        # Init junciton Traverse time array (call calculateTransferTimes()?)

    """
        A function which runs constantly to handle the sequencing of traffic lights, the occurrences and 
        frequency of pedestrian crossings and their duration, etc. This function runs until the junction has 
        been simulated for the duration specified by the user.
    """
    def junctionTimeManager():
        #...


