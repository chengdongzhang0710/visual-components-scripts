# the servo controller needs additional logic to operate during a simulation
# e.g. the controller needs to know when to move joints, what joints to move, and how far to move them
# the logic for the servo controller can be defined in a Python Script behavior

from vcScript import *

comp = getComponent()
servo = comp.findBehaviour("Servo Controller")

def OnRun():
  app = getApplication()
  
  while app.Simulation.IsRunning:
    servo.moveJoint(0, 0.0)
    servo.moveJoint(0, 600.0)

# additional script
def OnRun():
  app = getApplication()
  blue = app.findMaterial("blue")
  green = app.findMaterial("green")

  comp = getComponent()
  link = comp.findNode("Link1")
  link.MaterialInheritance = VC_MATERIAL_FORCE_INHERIT_NODE  # force the geometry of the node to inherit its material

  while app.Simulation.IsRunning:
    delay(1)
    link.NodeMaterial = blue
    delay(1)
    link.NodeMaterial = green
