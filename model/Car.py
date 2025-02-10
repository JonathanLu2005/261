class CarState(Enum):
    NotStationaryNorLeading = 1
    NotStationaryButLeading = 2
    StationaryButNotLeading = 3
    StationaryAndLeading = 4
    StationaryOnJunctionEntrance = 5
    InsideJunction = 6

class Car:
    def __init__(distanceFromNextCar, distanceFromJunctionEntrance, turningExitCardinality, carState, pointerToCarAhead, junctionEntrancePointer, junctionEntranceLane):
        self.distanceFromNextCar = distanceFromNextCar
        self.distanceFromJunctionEntrance = distanceFromJunctionEntrance
        self.turningExitCardinality = turningExitCardinality
        self.timeOfQueueStart = someTimeLibrary.getTimeStamp    # Get the time of the queue start
        self.currentState = carState                            # Depending on if it spawns on the junction entrance, if it spawns being the leader, or if it spanws behind another car.
        self.length = TrafficControl.carLength                  # Grab the static variable of car length
        self.pointerToCarBehind = None                          # There are no cars behind the car that was just added to the lane. 
        self.pointerToCarAhead = pointerToCarAhead
        self.currentStateOfCarAhead = pointerToCarAhead.currentState # Get this by fetching the pointer to the car ahead.
        self.junctionEntrancePointer = junctionEntrancePointer  # Pointer pointing to the junction entrance which the car is in so it can communicate with it when it enters the junction
        self.junctionEntranceLane = junctionEntranceLane        # Integer indicating to the junction entrance which lane the car is in to remove it late
        
        # Make a call to the carTimeManager to begin acting.

    
    """
        Used to alert the trailing car of this car’s new state. Used in the carTimeManager function
    """
    def notifyCarBehind():
        #...

    """
        Called by a car entering the junction to inform its junction entrance to remove it from its lane and 
        update variables like maximumWaitingTime (this car then notifies its trailing car that it is leading)
    """
    def notifyJunctionEntrance():
        #...
    
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
    def carTimeManager():
        #...
