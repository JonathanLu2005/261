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
    simulationTimeUnit = 0.01    # If this is 1/10, then it will take 10 time units in the simulation to simulate one second.
    carSpeed = None
    carLength = None
    carStationaryDistance = None
    carReactionTime = None
    numberOfGeneralLanes = None
    generalVPH = None
    hasLeftTurnLanes = None
    hasRightTurnLanes = None
    specialLength = None
    specialSpeed = None
    hasSpecialVehicleLane = None
    specialVehicleRatio = None
    specialVPH = None


    simulationComplete = False

    def __init__(self, sideLengthOfJunction, lengthOfSim, simulationTimeUnit, carSpeed, carLength, carStationaryDistance, carReactionTime, numberOfGeneralLanes, generalVPH, hasLeftTurnLanes, hasRightTurnLanes,  hasPedestrianCrossings, crossingPedestrianTime, crossingRequestsPerHour, trafficLightSequence, trafficLightGreenTimes, specialLength, specialSpeed, hasSpecialVehicleLane, specialVehicleRatio, specialVPH):
        self.sideLengthOfJunction = sideLengthOfJunction
        self.lengthOfSim = TrafficControl.convertSecondsToTimeUnits(lengthOfSim)
        TrafficControl.carSpeed = carSpeed * 0.44704 * TrafficControl.simulationTimeUnit # Multiplying by 0.44704 converts mph to meters per second. Multiplying by the simulation time unit means meters per time unit.
        TrafficControl.carLength = carLength
        TrafficControl.carStationaryDistance = carStationaryDistance
        TrafficControl.carReactionTime = TrafficControl.convertSecondsToTimeUnits(carReactionTime)
        print(f"Car reaction time in time units is {TrafficControl.carReactionTime}")
        TrafficControl.numberOfGeneralLanes = numberOfGeneralLanes
        TrafficControl.generalVPH = generalVPH
        TrafficControl.hasLeftTurnLanes = hasLeftTurnLanes
        TrafficControl.hasRightTurnLanes = hasRightTurnLanes
        self.hasPedestrianCrossings = hasPedestrianCrossings
        self.crossingPedestrianTime = TrafficControl.convertSecondsToTimeUnits(crossingPedestrianTime)
        self.crossingRequestsPerHour = crossingRequestsPerHour

        # New variables being added for the "could have" feature of Bus/Cycle lanes:
        # If there is no Bus lane and no Cycle lane, then these variables will be set to None and will not be needed in the program. 
        TrafficControl.specialLength = specialLength
        TrafficControl.specialSpeed = specialSpeed * 0.44704 * TrafficControl.simulationTimeUnit # Multiplying by 0.44704 converts mph to meters per second. Multiplying by the simulation time unit means meters per time unit.
        # This variable is used to determine whether the "specialLane" will be implemented, either for buses, or cycles - this information is not relevant to the model team, but may be relevant to those displaying results. 
        TrafficControl.hasSpecialVehicleLane = hasSpecialVehicleLane
        # The user must specify the ratio of green light time which will be applied for the special vehicles, 
            # and the flow of VPH for each arm of the junction and their turning direction, similar to the VPH for cars. 
        TrafficControl.specialVehicleRatio = specialVehicleRatio
        TrafficControl.specialVPH = specialVPH
        
        self.trafficLightSequence = trafficLightSequence
        self.trafficLightGreenTimes = [TrafficControl.convertSecondsToTimeUnits(greenLightTime) for greenLightTime in trafficLightGreenTimes]
        self.directions = [Direction.North, Direction.East, Direction.South, Direction.West]
        self.junctionEntrances = [JunctionEntrance(direction) for direction in self.directions]

        
        print(f"{TrafficControl.carSpeed} - Car speed")

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

        self.specialNorthMaxWaitingTime = None
        self.specialNorthMaxQueueLength = None
        self.specialNorthAvgWaitingTime = None
        self.specialNorthTotalVehiclesPassed = None

        self.specialEastMaxWaitingTime = None
        self.specialEastMaxQueueLength = None
        self.specialEastAvgWaitingTime = None
        self.specialEastTotalVehiclesPassed = None

        self.specialSouthMaxWaitingTime = None
        self.specialSouthMaxQueueLength = None
        self.specialSouthAvgWaitingTime = None
        self.specialSouthTotalVehiclesPassed = None

        self.specialWestMaxWaitingTime = None
        self.specialWestMaxQueueLength = None
        self.specialWestAvgWaitingTime = None
        self.specialWestTotalVehiclesPassed = None

        self.transferTime = TrafficControl.convertSecondsToTimeUnits(6) # Assume transfer time is 6 seconds constant for all cars for now.
        
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
            print(f"Pedestrian Crossing at {env.now}")
            timeOfLastCrossing = env.now
            timeInBetweenCrossings = (TrafficControl.convertSecondsToTimeUnits(60*60) / self.crossingRequestsPerHour) - self.crossingPedestrianTime
            
        while env.now < endTime:
            print(f"-=-New green light red light sequence at {env.now}")
            # Cycle through the traffic light sequence suggested by the user
            for direction in self.trafficLightSequence: 
                # If the time is exceeded, we need to leave this loop and get back to the while loop condition check: break will do this. 
                if env.now >= endTime:
                    break # Return to while loop to check for the condition to leave the loop.

            # Ensure to only give the green light to a direction if there are cars waiting - needs to not be the start time otherwise the whole sim fails due to no cars ever being generated into the queues
                if (env.now != 0 and self.junctionEntrances[direction].checkIfCarsWaiting() == False):
                    continue # Skip this arm of the junction since there are no vehicles waiting.

                remainingTime = endTime - env.now
                totalGreenTime = self.trafficLightGreenTimes[direction]            
                
                if (TrafficControl.hasSpecialVehicleLane == True): # Case 1: Simulating the flow of Buses/Cycles and Cars:
                    carGreenTime = totalGreenTime * (1 - TrafficControl.specialVehicleRatio)
                    specialGreenTime = totalGreenTime * TrafficControl.specialVehicleRatio
        
                    if remainingTime > 0 and self.specialVehicleRatio < 1:  
                        if carGreenTime > remainingTime:
                            carGreenTime = remainingTime            
                        self.junctionEntrances[direction].signalGreen()
                        print(f"Signal Green to {direction} for cars at {env.now}")
                        yield env.timeout(carGreenTime)
                        print(f"Signal Red to {direction} for cars at {env.now}")
                        self.junctionEntrances[direction].signalRed()

                        remainingTime = endTime - env.now  # Update remaining time
                        if remainingTime <= 0:
                            break 
                
                    if remainingTime > 0 and self.specialVehicleRatio > 0:
                        if specialGreenTime > remainingTime:
                            specialGreenTime = remainingTime  # Adjust to prevent exceeding endTime
                        self.junctionEntrances[direction].signalSpecialGreen()
                        print(f"Signal Green to {direction} for buses/cycles at {env.now}")
                        yield env.timeout(specialGreenTime)
                        print(f"Signal Red to {direction} for buses/cycles at {env.now}")
                        self.junctionEntrances[direction].signalSpecialRed()
                        remainingTime = endTime - env.now
                        if remainingTime <= 0:
                            break

                else: # Case 2: Only cars (No special vehicle lanes)
                    if remainingTime > 0:
                        if totalGreenTime > remainingTime:
                            totalGreenTime = remainingTime  # Adjust to prevent exceeding endTime
                        self.junctionEntrances[direction].signalGreen()
                        print(f"Signal Green to {direction} at {env.now}")
                        yield env.timeout(totalGreenTime)
                        print(f"Signal Red to {direction} at {env.now}")
                        self.junctionEntrances[direction].signalRed()
                        remainingTime = endTime - env.now
                        if remainingTime <= 0:
                            break


                    # Case 1: Only simulating the flow of buses/cycles
                    #if(TrafficControl.specialVehicleRatio == 1):           
                    #    self.junctionEntrances[direction].signalSpecialGreen() # Signal Green to the buses or cycles for this direction
                    #    print(f"Signal Green to {direction} at {env.now} for buses/cycles")
                    #    yield env.timeout(self.trafficLightGreenTimes[direction] * (TrafficControl.specialVehicleRatio)) # Give the green light time corresponding to this junction entrance
                    #    print(f"Signal Red to {direction} at {env.now} for buses/cycles")
                    #    self.junctionEntrances[direction].signalSpecialRed()   # Signal Red to the buses or cycles for this direction
                    
                    # Case 2: Simulating the flow of buses/cycles and cars
                    #else:
                    #            
                    #    self.junctionEntrances[direction].signalGreen() # Signal Green to this direction (for cars)
                    #    print(f"Signal Green to {direction} at {env.now}")
                    #    yield env.timeout(self.trafficLightGreenTimes[direction] * (1-TrafficControl.specialVehicleRatio)) # Give the green light time corresponding to this junction entrance
                    #    print(f"Signal Red to {direction} at {env.now}")
                    #    self.junctionEntrances[direction].signalRed()   # Signal Red to this direction
                    #    self.junctionEntrances[direction].signalSpecialGreen() # Signal Green to the buses or cycles for this direction
                    #    print(f"Signal Green to {direction} at {env.now} for buses/cycles")
                    #    yield env.timeout(self.trafficLightGreenTimes[direction] * (TrafficControl.specialVehicleRatio)) # Give the green light time corresponding to this junction entrance
                    #    print(f"Signal Red to {direction} at {env.now} for buses/cycles")
                    #    self.junctionEntrances[direction].signalSpecialRed()   # Signal Red to the buses or cycles for this direction
                # Case 3: Only simulating the flow of cars
                #else:
                #        
                #    self.junctionEntrances[direction].signalGreen() # Signal Green to this direction 
                #    print(f"Signal Green to {direction} at {env.now}")
                #    yield env.timeout(self.trafficLightGreenTimes[direction]) # Give the green light time corresponding to this junction entrance
                #    print(f"Signal Red to {direction} at {env.now}")
                #    self.junctionEntrances[direction].signalRed()   # Signal Red to this direction
                        
            # Pedestrian Crossing logic goes here
            if(self.hasPedestrianCrossings):
                if(env.now - timeOfLastCrossing > timeInBetweenCrossings):
                    print(f"Pedestrian Crossing Starting at {env.now}")
                    yield env.timeout(self.crossingPedestrianTime)
                    print(f"Pedestrian Crossing Ending at {env.now}")
                    timeOfLastCrossing = env.now
        
        #else:
        #    while env.now < endTime:
        #        # Cycle through the traffic light sequence suggested by the user
        #        for direction in self.trafficLightSequence:
        #            self.junctionEntrances[direction].signalGreen() # Signal Green to this direction
        #            print(f"Signal Green to {direction} at {env.now}")
        #            yield env.timeout(self.trafficLightGreenTimes[direction]) # Give the green light time corresopnding to this junction entrance 
        #            print(f"Signal Red to {direction} at {env.now}")
        #            self.junctionEntrances[direction].signalRed()   # Signal Red to this direction

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

        if (TrafficControl.hasSpecialVehicleLane == True):
            self.specialNorthMaxWaitingTime = self.junctionEntrances[Direction.North].getSpecialMaxWaitingTime()
            self.specialNorthMaxQueueLength = self.junctionEntrances[Direction.North].getSpecialMaxQueueLength()
            self.specialNorthAvgWaitingTime = self.junctionEntrances[Direction.North].getSpecialAvgWaitingTime()
            self.specialNorthTotalVehiclesPassed = self.junctionEntrances[Direction.North].getSpecialTotalVehiclesPassed()

            self.specialEastMaxWaitingTime = self.junctionEntrances[Direction.East].getSpecialMaxWaitingTime()
            self.specialEastMaxQueueLength = self.junctionEntrances[Direction.East].getSpecialMaxQueueLength()
            self.specialEastAvgWaitingTime = self.junctionEntrances[Direction.East].getSpecialAvgWaitingTime()
            self.specialEastTotalVehiclesPassed = self.junctionEntrances[Direction.East].getSpecialTotalVehiclesPassed()

            self.specialSouthMaxWaitingTime = self.junctionEntrances[Direction.South].getSpecialMaxWaitingTime()
            self.specialSouthMaxQueueLength = self.junctionEntrances[Direction.South].getSpecialMaxQueueLength()
            self.specialSouthAvgWaitingTime = self.junctionEntrances[Direction.South].getSpecialAvgWaitingTime()
            self.specialSouthTotalVehiclesPassed = self.junctionEntrances[Direction.South].getSpecialTotalVehiclesPassed()

            self.specialWestMaxWaitingTime = self.junctionEntrances[Direction.West].getSpecialMaxWaitingTime()
            self.specialWestMaxQueueLength = self.junctionEntrances[Direction.West].getSpecialMaxQueueLength()
            self.specialWestAvgWaitingTime = self.junctionEntrances[Direction.West].getSpecialAvgWaitingTime()
            self.specialWestTotalVehiclesPassed = self.junctionEntrances[Direction.West].getSpecialTotalVehiclesPassed()


        TrafficControl.simulationComplete = True

    """
        Takes the time such that the time unit meaning was a second in simulation time and returns the real portion of time with respect to simulationTimeUnit
    """
    @staticmethod
    def convertSecondsToTimeUnits(seconds):
        return seconds / TrafficControl.simulationTimeUnit
        # For example, if we want to wait one hour: 3600 seconds, we have to take into acount how many time units make up a second in the simlulation.
        # If our simulation time unit is 0.1, then we would need to wait 3600*10 = 36,000 time units.

    """
        The inverse operation of the function above
    """
    @staticmethod
    def convertTimeUnitsToSeconds(timeUnits):
        return timeUnits * TrafficControl.simulationTimeUnit
        # For example, if we want to wait one hour: 3600 seconds, we have to take into acount how many time units make up a second in the simlulation.
        # If our simulation time unit is 0.1, then we would need to wait 3600*10 = 36,000 time units.















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
    
    def addCar(self, turningExitCardinality, isCar, env):
        # If vehicleToAdd is not a Car, then we need to manually set the speed and length of the special vehicle.  
        if(self.numberOfCarsPresent == 0):
            self.leadingCar = Car(0, turningExitCardinality, env.now, None, self)
            if (isCar == False):
                self.leadingCar.setLength(TrafficControl.specialLength)
                self.leadingCar.setSpeed(TrafficControl.specialSpeed)
                print(f"Number of buses/cycles present is {self.numberOfCarsPresent+1} at junction entrance {self.junctionEntrance}")
            else:
                print(f"Number of cars present is {self.numberOfCarsPresent+1} at junction entrance {self.junctionEntrance}")
            self.trailingCar = self.leadingCar
            
            env.process(self.leadingCar.carTimeManager(env))
        else:
            self.trailingCar.pointerToCarBehind = Car(self.trailingCar.distanceFromJunctionEntrance + TrafficControl.carLength + TrafficControl.carStationaryDistance, turningExitCardinality, env.now, self.trailingCar, self)
            self.trailingCar = self.trailingCar.pointerToCarBehind
            if (isCar == False):
                self.trailingCar.setLength(TrafficControl.specialLength)
                self.trailingCar.setSpeed(TrafficControl.specialSpeed)
                print(f"Number of buses/cycles present is {self.numberOfCarsPresent+1} at junction entrance {self.junctionEntrance}")
            else:
                print(f"Number of cars present is {self.numberOfCarsPresent+1} at junction entrance {self.junctionEntrance}")
            env.process(self.trailingCar.carTimeManager(env))

        self.numberOfCarsPresent += 1
        self.maxQueueLength = max(self.maxQueueLength, self.numberOfCarsPresent)
    
    def leadingCarEnteringJunction(self, waitingTime, envTime):
        if(self.numberOfCarsPresent == 1):
            self.leadingCar = None
            self.trailingCar = None
        else:
            self.leadingCar = self.leadingCar.pointerToCarBehind

        print(f"Car Entering Junction from {self.junctionEntrance} at {envTime}")
        self.numberOfCarsPresent -= 1
        self.numberOfVehiclesPassed += 1
        self.totalWaitingTime += waitingTime
        self.maxWaitingTime = max(self.maxWaitingTime, waitingTime)








#-------------------
# JUNCTION ENTRANCE
#-------------------

class JunctionEntrance:
    def __init__(self, cardinalDirectionOfJunctionEntrance):
        self.cardinalDirectionOfJunctionEntrance = cardinalDirectionOfJunctionEntrance
        self.specialLane = None
        if (TrafficControl.hasSpecialVehicleLane == True):
            self.specialLane = Lane(cardinalDirectionOfJunctionEntrance)
        self.generalLanes = []              # Linked lists of Cars according to number of lanes. It should be noted that index 0 corresponds to the left most lane and the greatest index corresponds to the right most lane.
        for _ in range(0, TrafficControl.numberOfGeneralLanes):
            self.generalLanes.append(Lane(cardinalDirectionOfJunctionEntrance))
        self.timeUntilJunctionIsEmpty = 0   # The junction is initially empty when the junction is created

    """
        Called by the TrafficControl object. It is a blocking function terminating only when the junction is 
        empty, ensuring that cars stop entering the junction from this junction entrance when signalled red. 
        This enforces that no other junction entrance is signalled green when cars from another junction 
        entrance are still traversing.
    """
    def signalRed(self):
        print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved red signal for Cars")
        # No notion of transfer time yet but i have an idea of how to make it blocking.
        for lane in self.generalLanes:
            lane.isGreen = False
    
    """
        Function called by the TrafficControl class. This is a non-blocking function, which starts the flow 
        of vehicles across the junction from this particular junction entrance.
    """
    def signalGreen(self):
        print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved green signal for Cars")
        for lane in self.generalLanes:
            lane.isGreen = True

    def signalSpecialRed(self):
        if (self.specialLane is not None):
            print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved red signal For Buses/Cycles")
            self.specialLane.isGreen = False

    def signalSpecialGreen(self):
        if (self.specialLane is not None):
            print(f"Junction Entrance {self.cardinalDirectionOfJunctionEntrance} recieved green signal for Buses/Cycles")
            self.specialLane.isGreen = True

    def checkIfCarsWaiting(self):
        # Return true if there are any cars waiting in any queues
        for carLane in self.generalLanes:
            if (carLane.getNumberOfCars() > 0):
                return True
        if (self.specialLane is not None):
            if (self.specialLane.getNumberOfCars() > 0):
                return True 
        return False

    
    def getMaxWaitingTime(self):
        maxWaitingTime = -1
        for lane in self.generalLanes:
            maxWaitingTime = max(maxWaitingTime, lane.maxWaitingTime)
        return TrafficControl.convertTimeUnitsToSeconds(maxWaitingTime)
    
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
        return TrafficControl.convertTimeUnitsToSeconds(totalWaitingTime) / totalNumberOfVehiclesPassed if totalNumberOfVehiclesPassed > 0 else -1
    
    def getTotalVehiclesPassed(self):
        totalNumberOfVehiclesPassed = 0
        for lane in self.generalLanes:
            totalNumberOfVehiclesPassed += lane.numberOfVehiclesPassed
        return totalNumberOfVehiclesPassed

    def getSpecialMaxWaitingTime(self):
        return self.specialLane.maxWaitingTime

    def getSpecialMaxQueueLength(self):
        return self.specialLane.maxQueueLength

    def getSpecialAvgWaitingTime(self):
        totalWaitingTime = self.specialLane.totalWaitingTime
        totalNumberOfVehiclesPassed = self.specialLane.numberOfVehiclesPassed
        return TrafficControl.convertTimeUnitsToSeconds(totalWaitingTime) / totalNumberOfVehiclesPassed if totalNumberOfVehiclesPassed > 0 else -1

    def getSpecialTotalVehiclesPassed(self):
        return self.specialLane.numberOfVehiclesPassed

    def carGenerator(self, env, possibleLanesToSpawn, vph, exitCardinality):

        if(vph > 0):
            timeInBetweenVehicleSpawns = TrafficControl.convertSecondsToTimeUnits(60*60) / vph 
            
            while True and not TrafficControl.simulationComplete:
                print(f"Car spawning at {env.now} in junction {self.cardinalDirectionOfJunctionEntrance}")
                random.choice(possibleLanesToSpawn).addCar(exitCardinality, True, env)
                yield env.timeout(timeInBetweenVehicleSpawns)

    def buscycleGenerator(self, env, specialLane, vph, exitCardinality):
        if (vph > 0):
            timeInBetweenVehicleSpawns = TrafficControl.convertSecondsToTimeUnits(60*60) / vph 
            
            while True and not TrafficControl.simulationComplete:
                print(f"Bus/Cycle spawning at {env.now} in junction {self.cardinalDirectionOfJunctionEntrance}")
                specialLane.addCar(exitCardinality, False, env)
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

                # Bus/Cycle generators if needed:
                if (self.specialLane is not None and TrafficControl.specialVPH is not None):
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.North][2], Direction.West))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.North][1], Direction.East))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.North][0], Direction.North))

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
                
                # Bus/Cycle generators if needed:
                if (self.specialLane is not None and TrafficControl.specialVPH is not None):
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.East][2], Direction.North))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.East][1], Direction.South))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.East][0], Direction.East))



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

                # Bus/Cycle generators if needed:
                if (self.specialLane is not None and TrafficControl.specialVPH is not None):
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.South][2], Direction.East))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.South][1], Direction.West))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.South][0], Direction.South))


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
                
                # Bus/Cycle generators if needed:
                if (self.specialLane is not None and TrafficControl.specialVPH is not None):
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.West][2], Direction.South))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.West][1], Direction.North))
                    env.process(self.buscycleGenerator(env, self.specialLane, TrafficControl.specialVPH[Direction.West][0], Direction.West))







#-------------------
# CAR
#-------------------


class CarState(IntEnum):
    NotStationary = 1
    Stationary = 2

class Car:
    def __init__(self, distanceFromJunctionEntrance : int, turningExitCardinality : Direction, timeOfQueueStart : int, pointerToCarAhead, junctionEntranceLane : Lane):
        self.distanceFromJunctionEntrance = distanceFromJunctionEntrance
        self.turningExitCardinality = turningExitCardinality
        self.length = TrafficControl.carLength
        self.speed = TrafficControl.carSpeed
        self.timeOfQueueStart = timeOfQueueStart
        self.currentState = CarState.Stationary                 # The default is that cars spawn stationary (Don't worry they dont always spawn stationary depending on the car ahead's state.)
        self.pointerToCarBehind = None                          # There are no cars behind the car that was just added to the lane. This is not used in the car object itself, it is simply used by its corresponding lane object to refer to the next leading car after this car enters the junction.
        self.pointerToCarAhead = pointerToCarAhead
        self.junctionEntranceLane = junctionEntranceLane        # Integer indicating to the junction entrance which lane the car is in to remove it later

    def setLength(self, length):
        self.length = length
    
    def setSpeed(self, speed):
        self.speed = speed

    def getGapToCarAhead(self):
        return self.distanceFromJunctionEntrance - self.pointerToCarAhead.distanceFromJunctionEntrance - self.pointerToCarAhead.length

    def carTimeManager(self, env):
        trailingLastTimeStep = True if self.junctionEntranceLane.leadingCar != self else False

        # Currently, we are assuming that cars spawn directly one after the other. If when we spawn this car, the car in front of it is moving, then this car should also be moving too.
        if(self.junctionEntranceLane.leadingCar != self and self.pointerToCarAhead.currentState == CarState.NotStationary):
            self.currentState = CarState.NotStationary

        while True and not TrafficControl.simulationComplete:
            # Is leading
            if(self.junctionEntranceLane.leadingCar == self):
                if(self.currentState == CarState.Stationary and trailingLastTimeStep):
                    print(f"Became new leader at {env.now}")
                    yield env.timeout(TrafficControl.carReactionTime) # We have to wait the car reaction time duration before we can also begin moving.
                    trailingLastTimeStep = False
                    print(f"and starts to move at {env.now}")

                # If at the current speed you wont reach the junction entrance in the next time step, move as normal.
                if(self.distanceFromJunctionEntrance > self.speed):
                    self.currentState = CarState.NotStationary
                    self.distanceFromJunctionEntrance -= self.speed
                # If at the current speed you will cross the junction entrance in the next time step...
                elif(self.distanceFromJunctionEntrance == self.speed):
                    self.currentState = CarState.NotStationary if self.junctionEntranceLane.isGreen else CarState.Stationary
                    self.distanceFromJunctionEntrance -= self.speed
                else:
                    # Check if the signal is green. If this is the case, then just leave on this time step.
                    if(self.junctionEntranceLane.isGreen):
                        # Leave the junction entrance.
                        self.junctionEntranceLane.leadingCarEnteringJunction(env.now - self.timeOfQueueStart, env.now) # Must take into account transfer time?
                        break # Stop the while true loop as now this car will just despawn.

                    # If the signal is red, then you must stop at the junction entrance and become stationary.
                    else:
                        self.currentState = CarState.Stationary # Become Stationary
                        self.distanceFromJunctionEntrance = 0
            
            # Is not leading
            else:
                # If this car is not leading and it is stationary, then it must mean that it is right behind the other car with a gap of stationary distance.
                if(self.currentState == CarState.Stationary):
                    # We should only begin moving this car once the car in front begins moving. This is captured when the car in front's state becomes NotStationary.
                    if(self.pointerToCarAhead.currentState == CarState.NotStationary):
                        yield env.timeout(TrafficControl.carReactionTime) # We have to wait the car reaction time duration before we can also begin moving.
                        print(f"Detected Car Ahead moving at {env.now}")
                        self.distanceFromJunctionEntrance -= self.speed
                        self.currentState = CarState.NotStationary
                    # If the car ahead is still stationary, we don't do anything.
                
                # If the car is not leading and it is currently moving.
                else:
                    # If moving forward keeps the gap large enough then do it.
                    if(self.getGapToCarAhead() - self.speed > TrafficControl.carStationaryDistance):
                        self.distanceFromJunctionEntrance -= self.speed

                    # If moving forward is the exact stationary car distance, then we could change state depending if the car in front has stopped.
                    elif(self.getGapToCarAhead() - self.speed == TrafficControl.carStationaryDistance):
                        self.currentState = CarState.NotStationary if self.pointerToCarAhead.currentState == CarState.NotStationary else CarState.Stationary
                        self.distanceFromJunctionEntrance -= self.speed
                    
                    # If moving forward will close the gap beyond stationary distance, then the car must "slow down" or even stop.
                    else:
                        self.currentState = CarState.NotStationary if self.pointerToCarAhead.currentState == CarState.NotStationary else CarState.Stationary 
                        self.distanceFromJunctionEntrance = self.pointerToCarAhead.distanceFromJunctionEntrance + self.pointerToCarAhead.length + TrafficControl.carStationaryDistance
        

            yield env.timeout(1) # Wait one time unit in between car updates.

