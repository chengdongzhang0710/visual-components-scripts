from vcScript import *

comp = getComponent()
signal = comp.getBehaviour("BooleanSignal")
vehicle = comp.getBehaviour("Vehicle")
container = comp.getBehaviour("ComponentContainer")

app = getApplication()
conveyor = app.findComponent("StraightConveyorTemplate")
frame = conveyor.getFeature("PickUpLocation")
wpm = conveyor.WorldPositionMatrix
npm = frame.NodePositionMatrix
point = (wpm * npm).P

def OnSignal(signal):
    if signal.Value == True:
        resumeRun()

def OnRun():
    vehicle.clearMove()
    vehicle.Acceleration = 300.0
    vehicle.Deceleration = 300.0
    vehicle.MaxSpeed = 800.0
    vehicle.Interpolation = 0
    
    suspendRun()
    
    vehicle.addControlPoint(point)
    delay(vehicle.TotalTime)
    pm = comp.PositionMatrix
    angle = pm.getAxisAngle().W
    vehicle.rotateInPlace(-angle, 50, 50, 50)
    delay(vehicle.TotalTime)
    
    part = conveyor.ChildComponents[-1]
    
    # container.grab(part)
    # part.PositionMatrix = container.Location.FramePositionMatrix
    
    part.transfer(container, 0)
    
    pm.identity()
    # vehicle.replan()
    vehicle.clearPassedPoints()
    vehicle.addControlPoint(pm.P)
