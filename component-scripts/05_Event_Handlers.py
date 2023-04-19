# Event handlers: functions in a script that are called in response to an object event, e.g. a change in a property value
# A component script (Python Script) can be used to handle events related to components properties, signals and the pulse of the servo controller

from vcScript import *

comp = getComponent()

# property values
# define a function and assign it to the OnChanged event of a vcProperty object
# whenever the value of that property changes, the function is called to handle the event
def LengthChange(property):
  print "Platform length changed to %.2f"%property.Value

platform_length = comp.getProperty("PlatformLength")
platform_length.OnChanged = LengthChange

# signal values
# define a function and assign it to the OnValueChange event of a vcSignal object
# whenever the value of that signal changes, the function is called to handle the event
def JointValues(signal):
  jointX = comp.Joint_X
  jointY = comp.Joint_Y  # this returns the property value not the vcProperty
  print "Joint X is %s and Joint Y is %s"%(jointX, jointY)

signal = comp.findBehaviour("BooleanSignal")
signal.OnValueChange = JointValues

# create motions to trigger signal value changes
def OnRun():
  servo = comp.findBehaviour("Servo")
  while True:
    servo.moveJoint(0, 800.0)
    delay(5)
    servo.moveJoint(0, 0.0)

# heartbeats and states
# define a function and assign it to the OnHeartbeat event of a vcServoController object
# servo controllers/robot controllers can operate in pulse mode(heartbeat)
# in this mode, the servo controller/robot controller can indicate its current state for every pulse or beat
typemap = {
  VC_CONTROLLER_START: "Start",
  VC_CONTROLLER_RUNNING: "Running",
  VC_CONTROLLER_END: "End",
  VC_CONTROLLER_STOP: "Stop"
}
# a key-value pair is a valid state of the controller and its descriptive label
# you do not need to use all states of the controller

def HeartbeatState(servo, type):
  print "Servo heartbeat type %s"%typemap[type]

def OnRun():
  servo = comp.findBehaviour("Servo")
  servo.OnHeartbeat = HeartbeatState
  while True:
    servo.move(800.0, 800.0)
    delay(5)
    servo.move(0.0, 0.0)
