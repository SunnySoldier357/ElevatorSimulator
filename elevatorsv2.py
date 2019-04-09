
from tkinter import *
from tkinter import messagebox
from functools import partial
from elevator import Elevator
import time
import threading

class ElevatorSim(Frame):

    def __init__(self, floors, elevators, master=None):
        """
            Initialize the elevator simulation\n
            Parameters:\n
                floors: number of floors in the simulation
                elevators: number of elevators in the simulation\n
            Args: \n
                master: the frame the simulation is built on
        """
        self.elevatorCount = elevators
        self.floors = floors
        self.toFloorMap = {}
        self.queue = list()
        Frame.__init__(self, master)
        self.master = master
        self.elevators = list()
        for e in range(self.elevatorCount):
            self.elevators.append(Elevator(e))
            elevatorT = threading.Thread(target=self.moveElevator, args=(e, ))
            elevatorT.daemon = True
            elevatorT.start()
        canvas_width = self.elevatorCount*100
        canvas_height = self.floors*50
        self.canvas = Canvas(self.master, highlightbackground="red", highlightcolor="red", width=canvas_width, height=canvas_height)
        self.canvas.place(x=0, y=75)
        for f in range(floors):
            for e in range(self.elevatorCount):
                self.removeElevator(e,f + 1)
            elevatorButton = Button(self, text="request elevator", command = partial(self.sendRequest, f + 1))
            elevatorButton.place(x=100 * self.elevatorCount, y=75 + (50 * f))

            number = Spinbox(master, from_=1, to=self.floors)
            number.place(x=(100 * self.elevatorCount) + 75, y=75 + (50 * f))
            self.toFloorMap[f] = number
        self.init_window()
        t = threading.Thread(target=self.fromQueue)
        t.daemon = True
        t.start()

    def sendRequest(self, fromFloor):
        """
            Send a request for an elevator from the floor the request was sent from to the selected floor\n
            Parameters:\n
                fromFloor: the floor the request for an elevator was sent from
        """
        toFloor = int(self.toFloorMap[fromFloor - 1].get())
        if toFloor < 1 or toFloor > self.floors:
            messagebox.showinfo("invalid floor", "this floor doesn't exist")
            return
        if toFloor == fromFloor:
            return
        print(str(fromFloor), str(toFloor), "sent")
        self.queue.append([fromFloor, toFloor])
        
    def fromQueue(self):
        """
            Main loop for taking requests from the queue of elevator requests and sending it to the elevator that is closest
        """
        while True:
            if len(self.queue) > 0:
                req = self.queue.pop(0)
                min = self.floors * 2
                mini = 0
                i = 0
                for e in self.elevators:
                    if e.isCompatable(req[0], req[1]):
                        tempDist = e.findDist(req[0])
                        if tempDist < min:
                            min = tempDist
                            mini = i
                    i = i + 1
                currE = self.elevators[mini]
                if currE.hasJob():
                    currE.job.add(req[0])
                    currE.job.add(req[1])
                else:
                    currE.addJob(req[0], req[1])
            else:
                time.sleep(0.5)

    def moveElevator(self, elevatorNum):
        """
            Main thread for each elevator to take requests from their job queue. Requests come after closest elevator is determined\n
            Parameters:\n
                elevatorNum: the number elevator that the thread is for
        """
        print("el", str(elevatorNum))
        thisElevator = self.elevators[elevatorNum]
        while True:
            if thisElevator.hasJob():
                print("job rec")
                thisElevator.moving = True

                i = 0
                while (i < len(thisElevator.job.targs)):
                    curr = thisElevator.floor
                    targ = thisElevator.job.targs[i]
                    print("running targ", str(targ))
                    print(str(i))
                    if curr > targ:
                        #going up
                        print("up")
                        while curr > targ:
                            curr = curr - 1
                            targ = thisElevator.job.targs[i]
                            thisElevator.floor = curr
                            self.drawElevator(elevatorNum, curr)
                            self.removeElevator(elevatorNum, curr + 1)
                            self.master.update()
                            time.sleep(1)
                    else:
                        #going down
                        print("down")
                        while curr < targ:
                            curr = curr + 1
                            targ = thisElevator.job.targs[i]
                            thisElevator.floor = curr
                            self.drawElevator(elevatorNum, curr)
                            self.removeElevator(elevatorNum, curr - 1)
                            self.master.update()
                            time.sleep(1)
                    i = i + 1
                    self.drawOpenElevator(elevatorNum, curr)
                    time.sleep(1)
                    self.drawElevator(elevatorNum, curr)
                
                thisElevator.moving = False
                thisElevator.job = None
            else:
                time.sleep(1)
        

    #Creation of init_window
    def init_window(self):
        """
            Creation of the window
        """
        self.master.title("NAME")
        self.pack(fill=BOTH, expand=1)

        th = Button(self, text="quit", command = self.quitComm)
        th.place(x=self.elevatorCount*50, y=self.floors*50 + 100)

        for x in range(0, self.elevatorCount):
            eleNum = Label(self, text = ("elevator " + str(x + 1)))
            eleNum.place(x=100 * x, y=50)
            self.drawElevator(x, 1)
    
    def drawElevator(self, number, floor):
        """
            Draws the specified elevator at the specified floor\n
            Parameters:\n
                number: the elevator number of the elevator that needs to be drawn
                floor: the floor the elevator needs to be drawn at
        """
        self.canvas.create_rectangle(100 * (number), 50 * (floor - 1), 100 * (number + .5), 50 * floor, fill="#476042")
        
    def drawOpenElevator(self, number, floor):
        """
            Draws the specified elevator at the specified floor as blue signaling that it has its doors open\n
            Parameters:\n
                number: the elevator number of the elevator that needs to be open at
                floor: the floor the elevator needs to be drawn as open
        """
        self.canvas.create_rectangle(100*(number), 50*(floor-1), 100*(number + .5), 50*floor, fill="#123090")
        
    def removeElevator(self, number, floor):
        """
            Removes the specified elevator at the specified floor\n
            Parameters:\n
                number: the elevator number of the elevator that needs to be removed from
                floor: the floor the elevator needs to be removed at
        """
        self.canvas.create_rectangle(100*(number), 50*(floor-1), 100*(number + .5), 50*floor, fill="#ffffff")
    
    def quitComm(self):
        """
            Stops the application
        """
        exit()
