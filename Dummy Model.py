# Signal equality
TrafficLightSequence = ["North", "East", "South", "West"]

# Predetermined times
TrafficLightDuration = {
    "North": 150,
    "East": 150,
    "South": 150,
    "West": 150
}

# VPH
VehiclePerHour = {
    "North": 100,
    "East": 100,
    "South": 100,
    "West": 100
}

# Simulation length
HoursRanFor = 3

# Assume this many will cross over the green duration
Group = 10

# Store time for each group
TimeForEachDirection = {
    "North": [],
    "East": [],
    "South": [],
    "West": []
}

# Store queue for each group
QueueForEachDirection = {
    "North": [],
    "East": [],
    "South": [],
    "West": []
}

# Store how many cars passed
CurrentCarsPassed = {
    "North": 0,
    "East": 0,
    "South": 0,
    "West": 0
}

# Run simulation for x many hours
for x in range(0, HoursRanFor):
    SimulationLength = 60 * 60

    while SimulationLength > 0:
        GreenPeriodWait = 0
        for direction in TrafficLightSequence:
            # Store the queue for the groups that drive through
            QueueForEachDirection[direction].append(CurrentCarsPassed[direction])

            # Increment how many cars passed through, to represent the queue in front of the next group of cars
            CurrentCarsPassed[direction] += Group
            
            # Time is how long they've to wait for their green period + the vehicles in front of them
            TimeForEachDirection[direction] = max(TimeForEachDirection[direction]) + GreenPeriodWait

            # Increment for how long the next direction need to wait for
            GreenPeriodWait += TrafficLightDuration[direction]

        # Decrement time of the simulation taken so far
        SimulationLength -= GreenPeriodWait

# While loop allow us to manage time and queue, whilst the for loop allow us to manage how long the simulation runs for