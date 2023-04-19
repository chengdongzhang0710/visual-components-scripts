from vcScript import *
import vcVector
import vcMatrix

def OnSignal(signal):
    if signal.Value == True:
        resumeRun()

def OnRun():
    comp = getComponent()
    vehicle = comp.getBehaviour("Vehicle")
    
    # define vehicle speed, accel, and decel values
    vehicle.clearMove()
    vehicle.Acceleration = 300.0
    vehicle.Deceleration = 300.0
    vehicle.MaxSpeed = 800.0
    
    # interpolate path of vehicle
    vehicle.Interpolation = 0.35  # 0 by default
    
    # attach and detach wagons
    vehicle.detachAllWagons()
    
    app = getApplication()
    cylinder = app.findComponent("Cylinder")
    vehicle.attachWagonAtTheEnd(cylinder)  # default is to retain the offset between the component and cylinder
    vehicle.attachWagonAtTheEnd(cylinder, 200)
    
    t = vehicle.TotalTime
    delay(t / 2)
    vehicle.detachAllWagons()
    
    # offset origin of vehicle
    offset = vcMatrix.new()
    offset.translateRel(50, 50, 0)
    offset.rotateRelZ(45)
    vehicle.OffsetMatrix = offset
    
    vehicle.OffsetMatrix = None  # fix the offset to normal
    
    # signal a vehicle
    # triggerCondition(lambda: signal.Value == True)  # add script to signal's connection
    # suspendRun()  # combine with OnSignal() function
    
    # define path of vehicle
    point1 = vcVector.new(2000, 0, 0)
    point2 = vcVector.new(2000, 2000, 0)
    for p in [point1, point2]:
        vehicle.addControlPoint(p)
    
    # drive to other component
    app = getApplication()
    robot = app.findComponent("GenericRobot")
    wpm = robot.WorldPositionMatrix
    
    robot_point = wpm.P
    vehicle.addControlPoint(robot_point)
    
    # 以下代码块判断错误，在案例下成立是因为comp的位置就在原点
    # 在世界环境下，PositionMatrix和WorldPositionMatrix相同
    # 在vehicle.addControlPoint中输入目标的位置点即可
    # 正确的实现应该为vehicle.addControlPoint(p2)
    p1 = comp.PositionMatrix.P
    p2 = robot.PositionMatrix.P
    vehicle.addControlPoint(p2 - p1)
    
    frame = robot.getFeature("PickUpLocation")
    npm = frame.NodePositionMatrix
    frame_point = (wpm * npm).P
    vehicle.addControlPoint(frame_point)
    
    # get travel time and distance
    print vehicle.TotalTime
    print vehicle.PathLength
    
    # stop vehicle with time and distance
    d = vehicle.PathLength
    vehicle.resetStopAtDistance(d / 2)
    
    t = vehicle.TotalTime
    delay(t / 2)
    vehicle.clearMove()
    
    # reroute vehicle
    vehicle.addControlPoint(point1)
    t = vehicle.TotalTime
    delay(t / 2)
    vehicle.rePlan()
    vehicle.addControlPoint(point2)
    
    # rotate vehicle
    vehicle.addControlPoint(point1)
    t = vehicle.TotalTime
    delay(t)
    vehicle.rotateInPlace(180, 50, 50, 50)  # rotateInPlace(degree, speed, accel, decel)
    t = vehicle.TotalTime
    delay(t / 2)
    vehicle.rePlan()
    vehicle.addControlPoint(point2)
    
    # offset path of vehicle
    offset = vcVector.new(0, 500, 0)
    vehicle.offsetPath(offset)
