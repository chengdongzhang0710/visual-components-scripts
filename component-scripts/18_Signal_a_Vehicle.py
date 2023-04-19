from vcScript import *
import vcVector
import vcMatrix

point1 = vcVector.new(2000, 0, 0)
point2 = vcVector.new(2000, 2000, 0)
route = [point1, point2]

queue = []
def OnSignal(signal):
    if signal.Value == True:
        # queue.append(route)
        comp = getComponent()
        vehicle = comp.getBehaviour("Vehicle")
        for p in route:
            vehicle.addControlPoint(p)

def OnRun():
    queue[:] = []
    comp = getComponent()
    signal = comp.getBehaviour("BooleanSignal")
    vehicle = comp.getBehaviour("Vehicle")
    
    vehicle.clearMove()
    vehicle.Acceleration = 300.0
    vehicle.Deceleration = 300.0
    vehicle.MaxSpeed = 800.0
    
    '''
    app = getApplication()
    while app.Simulation.IsRunning:
        if queue:
            path = queue.pop()
            for p in path:
                vehicle.addControlPoint(p)
        delay(0.1)
    ''' 
