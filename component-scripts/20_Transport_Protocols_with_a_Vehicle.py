'''
Mobile Robot Python Script
'''
from vcScript import *

comp = getComponent()
signal = comp.getBehaviour("BooleanSignal")
vehicle = comp.getBehaviour("Vehicle")
container = comp.getBehaviour("ComponentContainer")

app = getApplication()
conveyor = app.findComponent("StraightConveyorTemplate")

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
    
    part = conveyor.ChildComponents[-1]
    data = part.getTransportInfo(part.Parent)
    target = data[-1].P
    
    vehicle.addControlPoint(target)
    delay(vehicle.TotalTime)
    part.transfer(container, 0)
    
    vehicle.clearMove()
    
    other_conveyor = app.findComponent("Conveyor")
    data = part.getTransportInfo(other_conveyor)
    target = data[-1].P
    
    vehicle.addControlPoint(target)
    delay(vehicle.TotalTime)
    part.transfer(data[2], 0)


'''
Straight Conveyor Template Pyhton Script
'''
from vcScript import *

def order(caller):
    tp.setTargetInfo(VC_AVAILABLE, comp, path, location)

comp = getComponent()
path = comp.getBehaviour("MainPath")
frame = comp.getFeature("PickUpLocation")
location = comp.WorldPositionMatrix * frame.NodePositionMatrix

tp = comp.getBehaviour("TransportProtocol")
tp.OnTransportInfo = order


'''
Straight Conveyor Template Pyhton Script
'''
from vcScript import *

def order(caller):
    tp.setTargetInfo(VC_AVAILABLE, comp, path, location)

comp = getComponent()
path = comp.getBehaviour("Path__HIDE__")
frame = comp.getFeature("DropOffLocation")
location = comp.WorldPositionMatrix * frame.NodePositionMatrix

tp = comp.getBehaviour("TransportProtocol")
tp.OnTransportInfo = order
