from enum import IntEnum
import simpy
import random

class Direction(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3

class TrafficControl:
    # Can declare Static variables here.
    carspeed = None
    carLength = None
    carStationaryDistance = None
    carReactionTime = None
    numberOfGeneralLanes = None
    generalVPH = None
    hasLeftTurnLanes = None
    hasRightTurnLanes = None


    simulationComplete = False

    def __init__(self, sideLengthOfJunction, lengthOfSim, simulationSecondLength, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes,  hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes):
        self.sideLengthOfJunction = sideLengthOfJunction
        self.lengthOfSim = lengthOfSim
        self.simulationSecondLength = simulationSecondLength
        TrafficControl.carSpeed = carSpeed
        TrafficControl.carLength = carLength
        TrafficControl.carStationaryDistance = carStationaryDistance
        TrafficControl.carReactionTime = carReactionTime
        TrafficControl.numberOfGeneralLanes = numberOfGeneralLanes
        TrafficControl.generalVPH = generalVPH
        TrafficControl.hasLeftTurnLanes = hasLeftTurnLanes
        TrafficControl.hasRightTurnLanes = hasRightTurnLanes
        self.hasPedestrianCrossings = hasPedestrianCrossings
        self.crossingPedestrianTime = crossingPedestrianTime
        self.crossingRequestsPerHour = crossingRequestsPerHour
        self.trafficLightSequence = trafficLightSequence
        self.trafficLightGreenTimes = trafficLightGreenTimes
        self.directions = [Direction.North, Direction.East, Direction.South, Direction.West]
        self.junctionEntrances = [JunctionEntrance(direction) for direction in self.directions]
        
        # The below variables are for result handling

        self.northMaxWaitingTime = None
        self.northMaxQueueLength = None
        self.northAvgWaitingTime = None
        self.northTotalVehiclesPassed = None

        self.eastMaxWaitingTime = None
        self.eastMaxQueueLength = None
        self.eastAvgWaitingTime = None
        self.eastTotalVehiclesPassed = None

        self.southMaxWaitingTime = None
        self.southMaxQueueLength = None
        self.southAvgWaitingTime = None
        self.southTotalVehiclesPassed = None

        self.westMaxWaitingTime = None
        self.westMaxQueueLength = None
        self.westAvgWaitingTime = None
        self.westTotalVehiclesPassed = None

        self.transferTime = 6 # Assume transfer time is 6 seconds constant for all cars for now.
        
        print("Init Simpy Environment")

        # Init simpy environment
        env = simpy.Environment()
        env.process(self.junctionTimeManager(env))      # Add the junction time manager to the environment.
        for junctionEntrance in self.junctionEntrances: # Add all the junction entrance time managers to the environment.
            junctionEntrance.junctionEntranceCarGeneratorSetup(env)
        env.run()   # Run the simulation

    """
        A function which runs constantly to handle the sequencing of traffic lights, the occurrences and 
        frequency of pedestrian crossings and their duration, etc. This function runs until the junction has 
        been simulated for the duration specified by the user.
    """

    def junctionTimeManager(self, env):
        endTime = self.lengthOfSim + env.now

        if(self.hasPedestrianCrossings):
            timeOfLastCrossing = env.now
            timeInBetweenCrossings = (60*60 / self.crossingRequestsPerHour) - self.crossingPedestrianTime
            
            while env.now < endTime:
                # Cycle through the traffic light sequence suggested by the user
                for direction in self.trafficLightSequence:
                    self.junctionEntrances[direction].signalGreen() # Signal Green to this direction
                    print(f"Signal Green to {direction} at {env.now}")
                    yield env.timeout(self.trafficLightGreenTimes[direction]) # Give the green light time corresopnding to this junction entrance 
                    print(f"Signal Red to {direction} at {env.now}")
                    self.junctionEntrances[direction].signalRed()   # Signal Red to this direction
                    
                # Pedestrian Crossing logic goes here
                if(env.now - timeOfLastCrossing > timeInBetweenCrossings):
                    print(f"Pedestrian Crossing Starting at {env.now}")
                    yield env.timeout(self.crossingPedestrianTime)
                    print(f"Pedestrian Crossing Ending at {env.now}")
                    timeOfLastCrossing = env.now
        
        else:
            while env.now < endTime:
                # Cycle through the traffic light sequence suggested by the user
                for direction in self.trafficLightSequence:
                    self.junctionEntrances[direction].signalGreen() # Signal Green to this direction
                    print(f"Signal Green to {direction} at {env.now}")
                    yield env.timeout(self.trafficLightGreenTimes[direction]) # Give the green light time corresopnding to this junction entrance 
                    print(f"Signal Red to {direction} at {env.now}")
                    self.junctionEntrances[direction].signalRed()   # Signal Red to this direction

        # Fetch Results from junction entrances and set them.

        self.northMaxWaitingTime = self.junctionEntrances[Direction.North].getMaxWaitingTime()
        self.northMaxQueueLength = self.junctionEntrances[Direction.North].getMaxQueueLength()
        self.northAvgWaitingTime = self.junctionEntrances[Direction.North].getAvgWaitingTime()
        self.northTotalVehiclesPassed = self.junctionEntrances[Direction.North].getTotalVehiclesPassed()

        self.eastMaxWaitingTime = self.junctionEntrances[Direction.East].getMaxWaitingTime()
        self.eastMaxQueueLength = self.junctionEntrances[Direction.East].getMaxQueueLength()
        self.eastAvgWaitingTime = self.junctionEntrances[Direction.East].getAvgWaitingTime()
        self.eastTotalVehiclesPassed = self.junctionEntrances[Direction.East].getTotalVehiclesPassed()

        self.southMaxWaitingTime = self.junctionEntrances[Direction.South].getMaxWaitingTime()
        self.southMaxQueueLength = self.junctionEntrances[Direction.South].getMaxQueueLength()
        self.southAvgWaitingTime = self.junctionEntrances[Direction.South].getAvgWaitingTime()
        self.southTotalVehiclesPassed = self.junctionEntrances[Direction.South].getTotalVehiclesPassed()

        self.westMaxWaitingTime = self.junctionEntrances[Direction.West].getMaxWaitingTime()
        self.westMaxQueueLength = self.junctionEntrances[Direction.West].getMaxQueueLength()
        self.westAvgWaitingTime = self.junctionEntrances[Direction.West].getAvgWaitingTime()
        self.westTotalVehiclesPassed = self.junctionEntrances[Direction.West].getTotalVehiclesPassed()


        TrafficControl.simulationComplete = True

















#-------------------
# LANE
#-------------------

class Lane:
    def __init__(self, junctionEntrance):
        self.leadingCar : Car = None
        self.trailingCar : Car = None
        self.numberOfCarsPresent = 0
        self.totalWaitingTime = 0       # Initially no cars have waitied
        self.numberOfVehiclesPassed = 0 # Initially no vehicles have passed
        self.maxWaitingTime = -1        # Maximum default value (which is the maximum time a car has waited. Set to -1 as a N/A value to show no cars have entered the junction yet).
        self.maxQueueLength = -1        # Maximum default value (which is the maximum length a queue has been. Set to -1 as a N/A value to show no queues were formed yet.)
        self.isGreen = False
        self.junctionEntrance = junctionEntrance

    def getNumberOfCars(self):
        return self.numberOfCarsPresent
    
    def addCar(self, turningExitCardinality, env):
        if(self.numberOfCarsPresent == 0):
            self.leadingCar = Car(0,0, turningExitCardinality, env.now, CarState.StationaryOnJunctionEntrance, None, self, self.junctionEntrance)
            self.trailingCar = self.leadingCar
            
            print(f"Added Car {self.numberOfCarsPresent} to {self.junctionEntrance}")
            env.process(self.leadingCar.carTimeManager(env))
        else:
            self.trailingCar.pointerToCarBehind = Car(TrafficControl.carStationaryDistance, self.trailingCar.distanceFromJunctionEntrance + TrafficControl.carLength + TrafficControl.carStationaryDistance, turningExitCardinality, env.now, CarState.StationaryButNotLeading, self.trailingCar, self, self.junctionEntrance)
            self.trailingCar = self.trailingCar.pointerToCarBehind

            print(f"Added Car {self.numberOfCarsPresent} to {self.junctionEntrance}")
            env.process(self.trailingCar.carTimeManager(env))

        self.numberOfCarsPresent += 1
        self.maxQueueLength = max(self.maxQueueLength, self.numberOfCarsPresent)
    
    def leadingCarEnteringJunction(self, waitingTime):
        self.numberOfCarsPresent -= 1
        self.numberOfVehiclesPassed += 1
        self.totalWaitingTime += waitingTime
        self.maxWaitingTime = max(self.maxWaitingTime, waitingTime)

        if(self.numberOfCars == 1):
            self.leadingCar = None
            self.trailingCar = None
        else:
            self.leadingCar = self.leadingCar.pointerToCarBehind
            # Notify this car that it is now leading?












#-------------------
# JUNCION ENTRANCE
#-------------------

class JunctionEntrance:
    def __init__(self, cardinalDirectionOfJunctionEntrance):
        self.cardinalDirectionOfJunctionEntrance = cardinalDirectionOfJunctionEntrance
        self.generalLanes = []              # Linked lists of Cars according to number of lanes. It should be noted that index 0 corresponds to the left most lane and the greatest index corresponds to the right most lane.
        for _ in range(0, TrafficControl.numberOfGeneralLanes):
            self.generalLanes.append(Lane(cardinalDirectionOfJunctionEntrance))
        self.timeUntilJunctionIsEmpty = 0   # The junction is initially empty when the junction is created
        self.isGreen = False                # Assume traffis signal is red when the junction entrance is created
        self.totalWaitingTime = 0           # Initially no cars have waitied
        self.numberOfVehiclesPassed = 0     # Initially no vehicles have passed
        self.maxWaitingTime = -1        # Maximum default value (which is the maximum time a car has waited. Set to -1 as a N/A value to show no cars have entered the junction yet).
        self.maxQueueLength = -1        # Maximum default value (which is the maximum length a queue has been. Set to -1 as a N/A value to show no queues were formed yet.)

    """
        Called by the TrafficControl object. It is a blocking function terminating only when the junction is 
        empty, ensuring that cars stop entering the junction from this junction entrance when signalled red. 
        This enforces that no other junction entrance is signalled green when cars from another junction 
        entrance are still traversing.
    """
    def signalRed(self):
        #...
        print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved red signal")
    
    """
        Function called by the TrafficControl class. This is a non-blocking function, which starts the flow 
        of vehicles across the junction from this particular junction entrance.
    """
    def signalGreen(self):
        #...
        print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved green signal")
    
    def getMaxWaitingTime(self):
        maxWaitingTime = -1
        for lane in self.generalLanes:
            maxWaitingTime = max(maxWaitingTime, lane.maxWaitingTime)
        return maxWaitingTime
    
    def getMaxQueueLength(self):
        maxQueueLength = -1
        for lane in self.generalLanes:
            maxQueueLength = max(maxQueueLength, lane.maxQueueLength)
        return maxQueueLength
    
    def getAvgWaitingTime(self):
        totalWaitingTime = 0
        totalNumberOfVehiclesPassed = 0
        for lane in self.generalLanes:
            totalWaitingTime += lane.totalWaitingTime
            totalNumberOfVehiclesPassed += lane.numberOfVehiclesPassed
        return totalWaitingTime / totalNumberOfVehiclesPassed if totalNumberOfVehiclesPassed > 0 else -1
    
    def getTotalVehiclesPassed(self):
        totalNumberOfVehiclesPassed = 0
        for lane in self.generalLanes:
            totalNumberOfVehiclesPassed += lane.numberOfVehiclesPassed
        return totalNumberOfVehiclesPassed

    def carGenerator(self, env, possibleLanesToSpawn, vph, exitCardinality):

        timeInBetweenVehicleSpawns = 60*60 / vph
        
        while True and not TrafficControl.simulationComplete:
            print(f"Vehicle spawning at {env.now} in junction {self.cardinalDirectionOfJunctionEntrance}")
            random.choice(possibleLanesToSpawn).addCar(exitCardinality, env)
            yield env.timeout(timeInBetweenVehicleSpawns)


    """
        Function which adds cars to the back of queues based on the VPH distribution of vehicles throughout 
        the simulation. Calls the addCar function for however many cars need to be added over time and updates 
        maximumQueueLength if needed.
    """
    def junctionEntranceCarGeneratorSetup(self, env):
        # Reminder of the format of the vph: [[North Bound Traffic Exiting North, North Bound Traffic Exiting East, North Bound Traffic Exiting West], [East Bound Traffic Exiting East, East Bound Traffic Exiting South, East Bound Traffic Exiting North], [South Bound Traffic Exiting South, South Bound Traffic Exiting West, South Bound Traffic Exiting East], [West Bound Traffic Exiting West, West Bound Traffic Exiting North, West Bound Traffic Exiting South]]
        
        match self.cardinalDirectionOfJunctionEntrance:
            case Direction.North:
                # Corresponding Subarray: [North Bound Traffic Exiting North, North Bound Traffic Exiting East, North Bound Traffic Exiting West]
                
                # Going Left Generator (going left from facing north is west)
                env.process(self.carGenerator(env, [self.generalLanes[0]], TrafficControl.generalVPH[Direction.North][2], Direction.West))

                # Going Right Generator (going right from facing north is east)
                env.process(self.carGenerator(env, [self.generalLanes[len(self.generalLanes) - 1]], TrafficControl.generalVPH[Direction.North][1], Direction.East))

                # Going Straight Generator (going straight from facing north is north)
                includeLeftMostLanes = 1 if TrafficControl.hasLeftTurnLanes else 0
                includeRightMostLanes = len(self.generalLanes) - 1 if TrafficControl.hasRightTurnLanes else len(self.generalLanes)
                straightLanes = []
                
                for i in range(includeLeftMostLanes, includeRightMostLanes):
                    straightLanes.append(self.generalLanes[i])
                
                env.process(self.carGenerator(env, straightLanes, TrafficControl.generalVPH[Direction.North][0], Direction.North))

            case Direction.East:
                # Corresponding Subarray: [East Bound Traffic Exiting East, East Bound Traffic Exiting South, East Bound Traffic Exiting North]
                
                # Going Left Generator (going left from facing east is north)
                env.process(self.carGenerator(env, [self.generalLanes[0]], TrafficControl.generalVPH[Direction.East][2], Direction.North))

                # Going Right Generator (going right from facing east is south)
                env.process(self.carGenerator(env, [self.generalLanes[len(self.generalLanes) - 1]], TrafficControl.generalVPH[Direction.East][1], Direction.South))

                # Going Straight Generator (going straight from facing east is east)
                includeLeftMostLanes = 1 if TrafficControl.hasLeftTurnLanes else 0
                includeRightMostLanes = len(self.generalLanes) - 1 if TrafficControl.hasRightTurnLanes else len(self.generalLanes)
                straightLanes = []
                
                for i in range(includeLeftMostLanes, includeRightMostLanes):
                    straightLanes.append(self.generalLanes[i])
                
                env.process(self.carGenerator(env, straightLanes, TrafficControl.generalVPH[Direction.East][0], Direction.East))

            case Direction.South:
                # Corresponding Subarray: [South Bound Traffic Exiting South, South Bound Traffic Exiting West, South Bound Traffic Exiting East]
                
                # Going Left Generator (going left from facing south is east)
                env.process(self.carGenerator(env, [self.generalLanes[0]], TrafficControl.generalVPH[Direction.South][2], Direction.East))

                # Going Right Generator (going right from facing south is west)
                env.process(self.carGenerator(env, [self.generalLanes[len(self.generalLanes) - 1]], TrafficControl.generalVPH[Direction.South][1], Direction.West))

                # Going Straight Generator (going straight from facing south is south)
                includeLeftMostLanes = 1 if TrafficControl.hasLeftTurnLanes else 0
                includeRightMostLanes = len(self.generalLanes) - 1 if TrafficControl.hasRightTurnLanes else len(self.generalLanes)
                straightLanes = []
                
                for i in range(includeLeftMostLanes, includeRightMostLanes):
                    straightLanes.append(self.generalLanes[i])
                
                env.process(self.carGenerator(env, straightLanes, TrafficControl.generalVPH[Direction.South][0], Direction.South))

            case Direction.West:
                # Corresponding Subarray: [West Bound Traffic Exiting West, West Bound Traffic Exiting North, West Bound Traffic Exiting South]
            
                # Going Left Generator (going left from facing west is south)
                env.process(self.carGenerator(env, [self.generalLanes[0]], TrafficControl.generalVPH[Direction.West][2], Direction.South))

                # Going Right Generator (going right from facing west is north)
                env.process(self.carGenerator(env, [self.generalLanes[len(self.generalLanes) - 1]], TrafficControl.generalVPH[Direction.West][1], Direction.North))

                # Going Straight Generator (going straight from facing west is west)
                includeLeftMostLanes = 1 if TrafficControl.hasLeftTurnLanes else 0
                includeRightMostLanes = len(self.generalLanes) - 1 if TrafficControl.hasRightTurnLanes else len(self.generalLanes)
                straightLanes = []
                
                for i in range(includeLeftMostLanes, includeRightMostLanes):
                    straightLanes.append(self.generalLanes[i])
                
                env.process(self.carGenerator(env, straightLanes, TrafficControl.generalVPH[Direction.West][0], Direction.West))












#-------------------
# CAR
#-------------------


class CarState(IntEnum):
    NotStationaryNorLeading = 1
    NotStationaryButLeading = 2
    StationaryButNotLeading = 3
    StationaryAndLeading = 4
    StationaryOnJunctionEntrance = 5
    InsideJunction = 6

class Car:
    def __init__(self, distanceFromNextCar : int, distanceFromJunctionEntrance : int, turningExitCardinality : Direction, timeOfQueueStart : int, carState : CarState, pointerToCarAhead, junctionEntranceLane : Lane, junctionEntrance : JunctionEntrance):
        self.distanceFromNextCar = distanceFromNextCar
        self.distanceFromJunctionEntrance = distanceFromJunctionEntrance
        self.turningExitCardinality = turningExitCardinality
        self.timeOfQueueStart = timeOfQueueStart
        self.currentState = carState                            # Depending on if it spawns on the junction entrance, if it spawns being the leader, or if it spanws behind another car.       
        self.pointerToCarBehind = None                          # There are no cars behind the car that was just added to the lane. 
        self.pointerToCarAhead = pointerToCarAhead
        self.junctionEntranceLane = junctionEntranceLane        # Integer indicating to the junction entrance which lane the car is in to remove it later
        self.junctionEntrance = junctionEntrance
    
    """
        Used to alert the trailing car of this car’s new state. Used in the carTimeManager function
    """
    def notifyCarBehind():
        #...
        print("stub")

    """
        Called by a car entering the junction to inform its junction entrance to remove it from its lane and 
        update variables like maximumWaitingTime (this car then notifies its trailing car that it is leading)
    """
    def notifyJunctionEntrance():
        #...
        print("stub")
    
    """
        Manages the flow of time and changes of state of a car. If a moving car is notified by the car ahead 
        that it has stopped, it starts decrementing the distanceFromNextCar until it reaches the 
        carStationaryDistance value which stops the car before notifying the car behind that it has stopped. 
        If a car begins to move, it will notify the car behind it to start moving after the carReactionTime has
        elapsed. This process repeats for the cars behind. When both cars are moving, the distanceFromJunctionEntrance 
        decreases but distanceFromNextCar does not. For the first car, upon the green signal, the junction entrance
        will send a notification to all heads of the lanes to begin moving which starts this cascading of 
        notifications to begin moving. (See state diagram for a deeper explanation)
    """
    def carTimeManager(self, env):
        yield env.timeout(1)

        # For now cars don't do anything
        # lastUpdate = env.now
        # while True:
        #     if(self.currentState == CarState.StationaryOnJunctionEntrance and self.junctionEntranceLane.isGreen):
        #         self.junctionEntranceLane.leadingCarEnteringJunction(env.now - self.timeOfQueueStart)
        #     elif(self.currentState == CarState.StationaryOnJunctionEntrance and not self.junctionEntranceLane.isGreen):
        #         pass
        #     elif(self.currentState == CarState.NotStationaryButLeading and self.junctionEntranceLane.isGreen):
                

