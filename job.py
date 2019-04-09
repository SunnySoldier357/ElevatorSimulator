
class Job():

    def __init__(self, t, from_, to):
        """
            Initialize the elevator simulation\n
            Parameters:\n
                t: The type of elevator request this job is
                from_: The current floor of the elevator
                to: the furthest destination of the elevator\n
        """
        self.type = t
        self.targs = list()
        self.targs.append(from_)
        self.targs.append(to)
        self.currJobIndex = 0
        #type: 0 not moving, 1 down down, 2 down up, 3 up up, 4 up down

    def jumps(self, currFloor, floor):
        """
            Calculates the amount of stops the elevator will take on the way to a destination.\n
            Used in calculating the closest elevator for a request\n
            Parameters:\n
                currFloor: the current floor the elevator is on
                floor: the destination floor of the request
        """
        count = 0
        for t in self.targs:
            if (t > currFloor and t < floor) or (t < currFloor and t > floor):
                count = count + 1
        return count

    def add(self, floor):
        """
            The addition of a request to this job.\n
            Parameters:\n
                floor: the floor the request wants to go to
        """
        if self.type == 1:
            i = 0
            for t in self.targs:
                if floor < t:
                    self.targs.insert(i, floor)
                    break
                else:
                    i = i + 1
            self.targs.insert(i, floor)
        elif self.type == 2:
            i = 1
            for t in range(len(self.targs) - 1):
                if floor > self.targs[i]:
                    self.targs.insert(i, floor)
                    break
                else:
                    i = i + 1
        elif self.type == 3:
            i = 0
            for t in self.targs:
                if floor > t:
                    self.targs.insert(i, floor)
                    break
                else:
                    i = i + 1
            self.targs.insert(i, floor)
        elif self.type == 4:
            i = 1
            for t in range(len(self.targs) - 1):
                if floor < self.targs[i]:
                    self.targs.insert(i, floor)
                    break
                else:
                    i = i + 1
