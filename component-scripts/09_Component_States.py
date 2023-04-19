# states are created in Statistics behavior and can be used to control the functionality of other behaviors
# e.g. when a component is in a Broken state, you can disable paths

# State Name -> System State
# a system state is a constant and used for data collection
# a state is defined by its label and mapped to a system state

from vcScript import *

# define idle and busy states
# it is possible to define the state of a component by editing the State property of its Statistics behavior, which is a vcStatistics object
# e.g. you can change the state of a component to record when the component is idle or busy
# use OnStateChange event to deal with state changes

def recordStateChange(stats, sim_time, state, comp):
  print state, "\t:\t", sim_time

def OnRun():
  # comp = getComponent()
  # servo = comp.findBehaviour("ServoController")
  # part_enter_signal = comp.findBehaviour("ComponentEnteringSignal")
  # servo_sensor_signal = comp.findBehaviour("ServoSensorSignal")
  # servo_path = comp.findBehaviour("ServoPath")

  statistics = comp.findBehaviour("Statistics")
  statistics.OnStateChange = recordStateChange

  while True:
    # servo_path.Enabled = False
    # servo.moveJoint(0,0.0)
    # servo_path.Enabled = True

    statistics.State = "Idle"

    # condition(lambda:servo_sensor_signal.Value != None )
    # servo_sensor_signal.Value = None
    # servo_path.Enabled = False

    statistics.State = "Busy"

    # servo.moveJoint(0,600.0)
    # servo_path.Enabled = True
    # condition(lambda: part_enter_signal.Value == False)

# -> the state of a component is printed as an integer that corresponding to a system statement constant (start from 0)

# use States and SystemStates properties of a vcStatistics object to print more specific data
def recordStateChange(stats, sim_time, state, comp):
  for s in stats.SystemStates:
    if state + 1 in s:
      state = s[0]  # s is a List, s[0] is system state description
  print state, "\t:\t", sim_time
# important! (state + 1) is the corresponding code in SystemStates list

# define failure and repair states
# it is possible to simulate a machine failure and the amount of time it takes to repair the machine
def OnRun():
  comp = getComponent()
  statistics = comp.findBehaviour("Statistics")

  while True:
    delay(comp.MTBF)
    statistics.State = "Broken"
    delay(5)
    statistics.State = "Repair"
    delay(comp.MTTR)

# define custome state
# Logic file
def recordStateChange(stats, sim_time, state, comp):
  print stats.State, "\t:\t", sim_time

  if stats.State == "Broken" or stats.State == "Repair":
    suspendRun()
  elif stats.State == "Fixed":
    resumeRun()

# PythonScript file
def OnRun():
  # comp = getComponent()
  # statistics = comp.findBehaviour("Statistics")

  while True:
    # delay(comp.MTBF)
    # statistics.State = "Broken"
    # delay(5)
    # statistics.State = "Repair"
    # delay(comp.MTTR)

    statistics.State = "Fixed"
# important! there might be some timing issues with the execution of both scripts
# one way you can try to avoid this issue is to create a condition that checks the current state of the component before transitioning to a new state

# Logic file
def recordStateChange(stats, sim_time, state, comp):
  print stats.State, "\t:\t", sim_time

  comp = getComponent()
  paths = [comp.findBehaviour("InPath"), comp.findBehaviour("ServoPath")]
  if stats.State == "Broken" or stats.State == "Repair":
    for p in paths:
      p.Enabled = False
  elif stats.State == "Fixed":
    for p in paths:
      p.Enabled = True

def checkState(stats):
  state = stats.State
  return state != "Broken" and state != "Repair"

def OnRun():
  # comp = getComponent()
  # servo = comp.findBehaviour("ServoController")
  # part_enter_signal = comp.findBehaviour("ComponentEnteringSignal")
  # servo_sensor_signal = comp.findBehaviour("ServoSensorSignal")
  # servo_path = comp.findBehaviour("ServoPath")

  # statistics = comp.findBehaviour("Statistics")
  # statistics.OnStateChange = recordStateChange

  while True:
    # servo_path.Enabled = False
    # servo.moveJoint(0,0.0)
    # servo_path.Enabled = True

    condition(lambda: checkState(statistics))  # avoid component go to an Idle state before it is being repaired
    # statistics.State = "Idle"

    # condition(lambda:servo_sensor_signal.Value != None )
    # servo_sensor_signal.Value = None
    # servo_path.Enabled = False

    # statistics.State = "Busy"

    # servo.moveJoint(0,600.0)
    # servo_path.Enabled = True
    # condition(lambda: part_enter_signal.Value == False)

# export state statistics
import csv
import os.path

def exportStateStatistics(property):
  username = os.getenv("username")
  path = os.path.join("C:\\Users\\", username, "Desktop")
  f = open(path + "\example.csv", "w")

  state_write = csv.writer(f, delimiter=",")
  state_write.writerow(getStateData())
  f.close()

def getStateData():
  l = []
  statistics = comp.findBehaviour("Statistics")
  for state in statistics.States:
    l.append(state[0])
    l.append(statistics.getTime(state[0]))
  return l

comp = getComponent()
button = comp.getProperty("Export To CSV")
button.OnChanged = exportStateStatistics
