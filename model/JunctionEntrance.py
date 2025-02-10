class JunctionEntrance:
    def __init__(cardinalDirectionOfJunctionEntrance, numberOfLanes):
        self.cardinalDirectionOfJunctionEntrance = cardinalDirectionOfJunctionEntrance
        self.lanes = ...                    # Linked lists of Cars according to number of lanes
        self.timeUntilJunctionIsEmpty = 0   # The junction is initially empty when the junction is created
        self.isGreen = False                # Assume traffis signal is red when the junction entrance is created
        self.totalWaitingTime = 0           # Initially no cars have waitied
        self.numberOfVehiclesPassed = 0     # Initially no vehicles have passed
        self.maximumWaitingTime = -1        # Maximum default value (which is the maximum time a car has waited. Set to -1 as a N/A value to show no cars have entered the junction yet).
        self.maximumQueueLength = -1        # Maximum default value (which is the maximum length a queue has been. Set to -1 as a N/A value to show no queues were formed yet.)


        # Call JunctionEntranceTimeManager to begin acting.

    """
        Called by the TrafficControl object. It is a blocking function terminating only when the junction is 
        empty, ensuring that cars stop entering the junction from this junction entrance when signalled red. 
        This enforces that no other junction entrance is signalled green when cars from another junction 
        entrance are still traversing.
    """
    def signalRed():
        #...
    
    """
        Function called by the TrafficControl class. This is a non-blocking function, which starts the flow 
        of vehicles across the junction from this particular junction entrance.
    """
    def signalGreen():
        #...
    
    """
        Function called by the junctionEntranceTimeManager which adds a single car to a lane (particular 
        linked list of car objects), giving it an exit direction based on the inputted VPH from this junction 
        entrance and initialising other car variables like timeOfQueueStart.
    """
    def addCar():
        #...

    """
        Function which adds cars to the back of queues based on the VPH distribution of vehicles throughout 
        the simulation. Calls the addCar function for however many cars need to be added over time and updates 
        maximumQueueLength if needed.
    """
    def junctionTimeManager():
        #...


