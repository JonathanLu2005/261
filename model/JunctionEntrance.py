from Car import Car, CarState
from TrafficControl import TrafficControl, Direction
import simpy

class Lane:
    def __init__(self):
        self.leadingCar : Car = None
        self.trailingCar : Car = None
        self.numberOfCarsPresent = 0
        self.totalWaitingTime = 0       # Initially no cars have waitied
        self.numberOfVehiclesPassed = 0 # Initially no vehicles have passed
        self.maxWaitingTime = -1        # Maximum default value (which is the maximum time a car has waited. Set to -1 as a N/A value to show no cars have entered the junction yet).
        self.maxQueueLength = -1        # Maximum default value (which is the maximum length a queue has been. Set to -1 as a N/A value to show no queues were formed yet.)
        self.isGreen = False


    def getNumberOfCars(self):
        return self.numberOfCarsPresent
    
    def addCar(self, turningExitCardinality, env):
        if(self.numberOfCarsPresent == 0):
            self.leadingCar = Car(0,0, turningExitCardinality, env.now, CarState.StationaryOnJunctionEntrance, None, self)
            self.trailingCar = self.leadingCar
            
            env.process(self.leadingCar.carTimeManager(env))
        else:
            self.trailingCar.pointerToCarBehind = Car(TrafficControl.carStationaryDistance, self.trailingCar.distanceFromJunctionEntrance + TrafficControl.carLength + TrafficControl.carStationaryDistance, turningExitCardinality, env.now, CarState.StationaryButNotLeading, self.trailingCar, self)
            self.trailingCar = self.trailingCar.pointerToCarBehind

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


class JunctionEntrance:
    def __init__(self, cardinalDirectionOfJunctionEntrance, numberOfLanes):
        self.cardinalDirectionOfJunctionEntrance = cardinalDirectionOfJunctionEntrance
        self.lanes = []                    # Linked lists of Cars according to number of lanes
        for _ in range(0, numberOfLanes):
            self.lanes.append(Lane())
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
    def signalRed():
        #...
        print("stub")
    
    """
        Function called by the TrafficControl class. This is a non-blocking function, which starts the flow 
        of vehicles across the junction from this particular junction entrance.
    """
    def signalGreen():
        #...
        print("stub")
    
    """
        Function called by the junctionEntranceTimeManager which adds a single car to a lane (particular 
        linked list of car objects), giving it an exit direction based on the inputted VPH from this junction 
        entrance and initialising other car variables like timeOfQueueStart.
    """
    def addCar():
        #...
        print("stub")

    """
        Function which adds cars to the back of queues based on the VPH distribution of vehicles throughout 
        the simulation. Calls the addCar function for however many cars need to be added over time and updates 
        maximumQueueLength if needed.
    """
    def junctionEntranceTimeManager(self, env):
        #Just add car to all lanes every 10 time units always bound to north
        while True:
            for lane in self.lanes:
                lane.addCar(Direction.North, env)
            yield env.timeout(10)



