# use conditions, events, and triggers to control the execution of scripts

from vcScript import *

comp = getComponent()
servo = comp.findBehaviour("ServoController")
servoPath = comp.findBehaviour("ServoPath")

# ServoSensorSignal is a Component Signal behavior used to identify what component triggers a sensor in ServoPath
servoSensorSignal = comp.findBehaviour("ServoSensorSignal")

# ComponentEnteringSignal is a Boolean Signal behavior used as a transition signal to identify when a component enters and leaves ServoPath
partEnteringSignal = comp.findBehaviour("ComponentEnteringSignal")

def OnRun():
  if servoSensorSignal.Value != None:
    servo.moveJoint(0, 600.0)
  else:
    print "Component not at sensor"
# not work due to:
# 1. the script evaluates the condition of the if statement immediately and before a part triggers the sensor
# 2. the script does not know if the value of the signal has changed from None to a vcComponent object

# conditions: condition() and triggerCondition()
# the condition() method allows you to delay the execution of a script until a called function returns a True value
# the evaluation of that condition is immediate and continuous, i.e. the method will continue to call the function until it returns a True value
# the function can be defined in the same script or inlined by using a lambda operator
def OnRun():
  condition(lambda: servoSensorSignal.Value != None)
  print "Component reached sensor"
  servo.moveJoint(0, 600.0)
# not work due to:
# the servo signal has no way of knowing if the value of sensor signal has changed during the simulation
# one way for a signal to communicate its value to other behaviors is to call its signal() method
# important! signal() method force the sensor to send a signal though it is not triggered

def OnRun():
  servoSensorSignal.signal(comp)
  condition(lambda: servoSensorSignal.Value != None)
  print "Component reached sensor"
  servo.moveJoint(0, 600.0)
# not work due to:
# the platform will not wait for a part to trigger the sensor, the platform moves as soon as the component is created

# the triggerCondition() method is like the condition method
# but evaluates its condition when triggered by a signal or other behavior connected to the script
def OnRun():
  servoSensorSignal.signal(comp)
  triggerCondition(lambda: servoSensorSignal.Value != None)
  print "Component reached sensor"
  servo.moveJoint(0, 600.0)
# not work due to:
# the condition is never evaluated because the script currently has no triggers
# -> add the Python Script behavior as a connection to the ComponentEnteringSignal behavior
# the platform moves before the part reaches the sensor
# the platform moves as soon as the component origin reaches the ServoBegin -> ComponentEnteringSignal is triggered but not ServoSensorSignal

# add the Python Script behavior as a connection to the ServoSensorSignal behavior
# important! the signal() method is now redundant since the script is connected to the signal and recevies its signal events
def OnRun():
  triggerCondition(lambda: servoSensorSignal.Value != None)
  print "Component reached sensor"
  servo.moveJoint(0, 600.0)

# use the getTrigger() method to evaluate the last recorded trigger of a script
# this is helrful if you have a script that is connected to many signals and you need to specify which trigger is required for a condition to be true
def OnRun():
  condition(lambda: getTrigger() == servoSensorSignal)
  print "Component reached sensor"
  servo.moveJoint(0, 600.0)

def OnRun():
  while True:
    triggerCondition(lambda: getTrigger() == servoSensorSignal)  # here condition() and triggerCondition() make no difference
    servoPath.Enabled = False
    servo.moveJoint(0, 600.0)
    servoPath.Enabled = True
    condition(lambda: partEnteringSignal.Value == False)
    servoPath.Enabled = False
    servo.moveJoint(0, 0.0)
    servoPath.Enabled = True

# signal events
# use signal events to suspend and resume the OnRun() event, which is the main function of a Python Script
def OnSignal(signal):
  if signal == servoSensorSignal:
    if signal.Value != None:
      resumeRun()
  elif signal == partEnteringSignal:
    if signal.Value == False:
      resumeRun()

def OnRun():
  while True:
    suspendRun()
    servoPath.Enabled = False
    servo.moveJoint(0, 600.0)
    servoPath.Enabled = True
    suspendRun()
    servoPath.Enabled = False
    servo.moveJoint(0, 0.0)
    servoPath.Enabled = True
