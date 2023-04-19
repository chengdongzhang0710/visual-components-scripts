from vcScript import *
from vcHelpers.Robot2 import *
import vcMatrix

app = getApplication()
comp = getComponent()
path = comp.findBehaviour("Path__HIDE__")
robot = getRobot(app.findComponent("GenericRobot"))

def OnRun():
  while app.Simulation.IsRunning:
    if path.ComponentCount > 0:
      if robot.GraspContainer.ComponentCount == 0:
        part = path.Components[0]
        if len(part.ChildComponents) == 0:
          robot.pickMovingPart(part)
      else:
        pallet = path.Components[0]
        mtx = vcMatrix.new()
        mtx.translateRel(0, 0, 200)
        mtx.rotateRelY(180)
        robot.linearMoveToMtx_ExternalBase(pallet, mtx)
        robot.releaseComponent(pallet)
    
    delay(0.1)
