
from tkinter import *
from elevatorsv2 import ElevatorSim

def runElevatorsv2(floors, elevators):
    """
        Runs the elevator simulation\n
        Parameters:\n
            floors: number of floors in the simulation\n
            elevators: number of elevators in the simulation\n
    """
    root = Tk()
    size = "" + str(elevators * 100 + 175) + "x" + str((floors + 2) * 100)
    print(size)
    root.geometry(size)
    win = ElevatorSim(floors, elevators, root)
    root.mainloop()

floors = 15
elevators = 4
runElevatorsv2(floors, elevators)
