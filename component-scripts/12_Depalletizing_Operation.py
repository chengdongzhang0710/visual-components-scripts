from vcScript import *
from vcHelpers.Robot2 import *

def OnRun():
  robot = getRobot("RobotInterface")  # can use interface to capture the external robot
  app = getApplication()

  while app.Simulation.IsRunning:
    while not robot.SignalMapIn.input(100):
      delay(0.1)
    robot.SignalMapOut.output(100, False)

    conveyorIn = app.findComponent("Sensor Conveyor")
    pallet = conveyorIn.ComponentChildren[0]  # ComponentChildren will return all the components that are directly attached to that node
    parts = pallet.ChildComponents  # ChildComponents will return all the components that are attached to that node and node's tree
    
    conveyorOut = app.findComponent("Sensor Conveyor #2")
    for _ in parts:
      robot.pickFromPallet(pallet, Approach=300, InversedOrder=True)
      robot.place(conveyorOut)

    robot.SignalMapOut.output(100, True)

    # wait for empty pallet to leave path
    while pallet in conveyorIn.ComponentChildren:
      delay(0.1)
