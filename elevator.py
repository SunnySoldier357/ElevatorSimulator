
import time
from job import Job

class Elevator(object):
    def __init__(self, number):
        """
            Initializes an Elevator object\n
            Parameters:\n
                number: the elevator number
        """
        self.number = number
        self.floor = 0
        self.job = None
        self.moving = False

    def isCompatable(self, from_, to):
        """
            Check if this elevator can take the request\n
            Parameters:\n
                from_: the origin floor of a request
                to: the destination floor of the request
        """
        if self.hasJob():
            if from_ < to:
                #wants to move down
                if self.job.type == 1:
                    if from_ > self.floor:
                        return True
                if self.job.type == 4:
                    if from_ > self.job.targs[0]:
                        return True
            else:
                #wants to move up
                if self.job.type == 3:
                    if from_ < self.floor:
                        return True
                if self.job.type == 2:
                    if from_ <self.job.targs[0]:
                        return True
            return False
        else:
            return True

    def addTarg(self, floor):
        """
            Adds a target for the elevator to make a stop on\n
            Parameters:\n
                floor: the destination floor of the request
        """
        self.job.add(floor)

    def addJob(self, from_, to):
        """
            Adding a job to an elevator\n
            Parameters:\n
                from_: the origin floor of a request
                to: the destination floor of the request
        """
        ty = 0
        if from_ > to:
            #want to move up
            if self.floor > from_:
                #needs to move up
                ty = 3
            else:
                ty = 2
        else:
            #want to move down
            if self.floor < from_:
                #needs to move down
                ty = 1
            else:
                ty = 4
        self.job = Job(ty, from_, to)

    def hasJob(self):
        """
            Returns if elevator has a job or not
        """
        return not self.job == None

    def findDist(self, floor):
        """
            Calculates the distance this elevator is from a certain floor\n
            Parameters:\n
                floor: the destination floor of the request
        """
        if self.job == None:
            return abs(floor - self.floor)
        else:
            #type: 0 not moving, 1 down down, 2 down up, 3 up up, 4 up down
            if self.job.type == 1:
                return abs(floor - self.floor) + self.job.jumps(self.floor, floor)
            elif self.job.type == 2:
                if self.job.currJobIndex == 0:
                    b = self.job.targs[self.job.currJobIndex]
                    return abs(b - self.floor) + self.job.jumps(b, floor) + abs(floor - b)
                else:
                    return abs(floor - self.floor) + self.job.jumps(self.floor, floor)
            elif self.job.type == 3:
                return abs(floor - self.floor) + self.job.jumps(self.floor, floor)
            elif self.job.type == 4:
                if self.job.currJobIndex == 0:
                    b = self.job.targs[self.job.currJobIndex]
                    return abs(b - self.floor) + self.job.jumps(b, floor) + abs(floor - b)
                else:
                    return abs(floor - self.floor) + self.job.jumps(self.floor, floor)