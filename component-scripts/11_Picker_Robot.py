from vcScript import *
from vcHelpers.Robot2 import *

def OnRun():
  robot = getRobot()
  picked = []
  app = getApplication()
  conveyor = app.findComponent("Sensor Conveyor")

  while app.Simulation.IsRunning:
    while not robot.SignalMapIn.input(100):
      delay(0.1)
    
    parts = conveyor.ChildComponents
    parts = filter(lambda p: p not in picked, parts)
    part = parts.pop()

    robot.pickMovingPart(part)
    picked.append(part)

    part = robot.GraspContainer.Components[0]
    pos = part.WorldPositionMatrix.P
    a = conveyor.BoundDiagonal
    offsetX = pos.X - a.X

    robot.place(conveyor, Tx=offsetX)  # can pass in extra arguments to set orientation

    picked = filter(lambda p: p in conveyor.ChildComponents, picked)
