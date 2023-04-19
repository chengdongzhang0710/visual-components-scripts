# you can write a component script that executes sub routines in a robot to control robot during a simulation
# that would not require you to execute the entire robot program
# you can create sub routines for tasks dynamically and automate robot motions using scripts and helper libraries

from vcScript import *

# call sub routines
# the executor of a robot program can be used to call sub routines in its executable program during a simulation
# important! if you don't want a robot to execute its main routine, set the IsEnabled property of its executor to False
def OnRun():
  comp = getComponent()
  robotExecutor = comp.findBehaviour("Executor")
  robotExecutor.IsEnabled = False

  routine = robotExecutor.Program.findRoutine("Example")
  if routine:
    robotExecutor.callRoutine(routine)

# another way to call routines in a robot program is to use vcHelpers.Robot2 library
# this library contains many useful methods for controlling a robot
from vcHelpers.Robot2 import *

def OnRun():
  robot = getRobot()
  robot.callSubRoutine("Example")

# move joints
# 1. moveJoint() method available to servo and robot controllers
# 2. driveJoints() method in vcHelpers.Robot2
def OnRun():
  robot = getRobot()

  # driveJoints() method is directly called on the robot
  robot.driveJoints(0, 0, 0, 0, 0, 0)

  # be careful moveJoint() method is called on the controller instead of robot!
  robot.Controller.moveJoint(2, 90.0)

  robot.callSubRoutine("Example")

# pick stationary parts
# use pick() method in vcHelpers.Robot2 to pick a component in the 3D world
def OnRun():
  app = getApplication()
  part = app.findComponent("VisualComponents_Box")  # if there is no box, robot will be told to pick nothing
  
  robot = getRobot()
  robot.pick(part, 300.0)  # pick the box with a 300.0 distance up

# pick moving parts
# you can control a robot form a different components and instruct the robot to pick moving part during a simulation
# the robot and the controlling component do not have to be connected to one another
# pickMovingPart() method in vcHelpers.Robot2 can be used to pick moving components
def OnRun():
  comp = getComponent()
  sensor_signal = comp.findBehaviour("SensorSignal")
  triggerCondition(lambda: sensor_signal.Value != None)
  part = sensor_signal.Value

  app = getApplication()
  robotComponent = app.findComponent("GenericRobot")
  robot = getRobot(robotComponent)

  robot.pickMovingPart(part)

# place parts
# use place() method in vcHelpers.Robot2 to place a component on top of a table, pallet or conveyor
def OnRun():
  pallet = app.findComponent("Euro Pallet")
  robot.place(pallet)

# pick parts from pallet
# use pickFromPallet() method in vcHelpers.Robot2 to pick components attached to a pallet
def OnRun():
  robot.pickFromPallet(pallet)

# record routines
# use RecordRoutine and RecordRSL properties in vcHelpers.Robot2 to record the actions of a robot as a routine in its program
# you need to define the name of a routine before recording
# if the routine already exists in robot, statements will be appended to that routine
# that is, recording will not override a routine, important!
def OnRun():
  robot.RecordRoutine = "PickPart"
  robot.RecordRSL = True
  robot.pick(part)
  robot.RecordRSL = False

  robot.RecordRoutine = "PlacePart"
  robot.RecordRSL = True
  pallet = app.findComponent("Euro Pallet")
  robot.place(pallet)
  robot.RecordRSL = False

# place parts in pattern
# use placeInPattern() method in vcHelpers.Robot2 to place components on top of a table, pallet or conveyor in a set pattern
def OnRun():
  app = getApplication()
  robotComponent = app.findComponent("GenericRobot")
  robot = getRobot(robotComponent)

  comp = getComponent()
  sensor_signal = comp.findBehaviour("SensorSignal")

  stack_size = 8
  x, y, z = 0, 0, 0  # x, y, z are index values
  while stack_size > 0:
    triggerCondition(lambda: sensor_signal.Value != None)
    part = sensor_signal.Value
    robot.callSubRoutine("PickPart")
    
    pallet = app.findComponent("Euro Pallet")
    robot.placeInPattern(pallet, x, y, z, 2, 2, 2)

    stack_size -= 1

    if x < 1:
      x += 1
    else:
      x = 0
      y += 1
    if y > 1:
      y = 0
      z += 1
