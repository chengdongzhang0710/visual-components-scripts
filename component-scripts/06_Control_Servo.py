from vcScript import *

# joint targets
def OnRun():
  comp = getComponent()
  servo = comp.findBehaviour("Servo")
  servo.setJointTarget(0, 500.0)  # Joint_X
  servo.setJointTarget(1, 0.0)  # Joint_Y
  servo.move()

# joint conditions
# use a joint value as a condition for moving another joint
# getJointValue() and getJointTarget() methods in vcServoController can be used to define a condition for moving connected joints in sequence
def OnRun():
  comp = getComponent()
  servo = comp.findBehaviour("Servo")
  servo.setJointTarget(0, 500.0)
  servo.setJointTarget(1, 0.0)
  servo.move()

  condition(lambda: servo.getJointTarget(0) == servo.getJointValue(0))  # condition on Joint_X
  servo.setJointTarget(1, 500.0)
  servo.move()

# cycle times
# 1. a servo knows the target values of its joints you can calculate the cycle time of that movement -> vcServoController.calcMotionTime()
# 2. directly set the cycle time of the servo, threrby scaling joint speeds to complete a movement in that given time -> vcServoController.setMotionTime()
def OnRun():
  comp = getComponent()
  servo = comp.findBehaviour("Servo")
  servo.setJointTarget(0, 500.0)
  servo.setJointTarget(1, 0.0)

  time = servo.calcMotionTime()
  print "Original cycle time:", time

  time += 2
  servo.setMotionTime(time)
  print "New cycle time:", servo.calcMotionTime()

  servo.move()

# joint movements
# move joints without having to first set target values:
# 1. use the moveImmediate() method in vcServoController to move joints to target values in zero simulation time
# 2. use the moveJoint() method to drive a specific joint
# 3. pass target values for joints as optional arguments in the move() method, but the values would need to be given in the order that joints are listed in the servo
def OnRun():
  comp = getComponent()
  servo = comp.findBehaviour("Servo")

  servo.moveImmediate(0, 0)

  servo.moveJoint(0, 800.0)
  servo.moveJoint(1, 500.0)

  servo.move(0, 0)

# heartbeat mode
comp = getComponent()
servo = comp.findBehaviour("Servo")

targets = None
def addNewTarget(servo, event_type):
  global targets
  if event_type == VC_CONTROLLER_END:
    if servo.getJointTarget(0) == 0 and servo.getJointTarget(1) == 0:
      targets = (500, 0)
    elif servo.getJointTarget(0) == 500 and servo.getJointTarget(1) == 0:
      if len(targets) < 3:
        targets = (500, 500)
      else:
        targets = (0, 0)
    elif servo.getJointTarget(0) == 500 and servo.getJointTarget(1) == 500:
      targets = (500, 0, -1)  # -1 is not used by servo and is only for condition judgement
    for i in range(servo.JointCount):
      servo.setJointTarget(i, targets[i])
      resumeRun()

servo.OnHeartbeat = addNewTarget

def OnRun():
  for i in range(servo.JointCount):
    servo.setJointTarget(i, 0)
  while True:
    servo.move()
    suspendRun()

####################

# example
comp = getComponent()
servo = comp.findBehaviour("Servo")

def OnStart():
  for i in servo.Joints:
    print i.Name, i.IntialValue

def OnRun():
  servo.setJointTarget(0, 500.0)
  servo.setJointTarget(1, 500.0)
  servo.setMotionTime(10.0)
  print servo.calcMotionTime()  # -> 10.0
  servo.move()

  delay(5.0)
  servo.moveJoint(0, 250.0)

  trigger = servo.getJointValue(0)
  if trigger <= 250:
    servo.moveJoint(1, 250.0)
  
  delay(5.0)
  servo.moveImmediate(0.0, 0.0)

  while True:
    servo.move(800.0, 800.0)
    delay(5.0)
    servo.move(0.0, 0.0)

def customEvent(servo, event):
  global sim
  sim = getSimulation()
  if event == 0:
    print "The servo has started at:", sim.SimTime
  elif event == 2:
    print "The servo has ended at:", sim.SimTime

servo.OnHeartbeat = customEvent