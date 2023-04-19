# During a simulation you may want to highlight components to provide important visual indicators
# 1. Highlight the stage of a component in a product life cycle or color components in a workcell
# 2. Highlight the state of a component, e.g. whether a machine or resource is active, idle or broken

from vcScript import *

app = getApplication()
yellow = app.findMaterial("yellow")

comp = getComponent()
path = comp.findBehaviour("MainPath")
transition_signal = path.TransitionSignal

# hightlight FIFO
# change the material of the first part that enters the path
def OnRun():
  while True:
    if transition_signal.Value:
      part = path.getComponent(0)
      part.NodeMaterial = yellow
      part.MaterialInheritance = VC_MATERIAL_FORCE_INHERIT
      delay(0.1)
    else:
      delay(0.1)

# highlight all
# change the material of all components contained by the path when its transition signal value is true
def OnRun():
  while True:
    if transition_signal.Value:
      for part in path.Components:
        part.NodeMaterial = yellow
        part.MaterialInheritance = VC_MATERIAL_FORCE_INHERIT
        delay(0.1)
    else:
      delay(0.1)

# in a high volume conveyor the above code might degrade simulation performance
# an alternative is to use the OnTransition event inherited by a path from vcContainer to highlight arriving parts
def highlightPartEnteringPath(part, isPartArriving):
  if isPartArriving:
    part.NodeMaterial = yellow
    part.MaterialInheritance = VC_MATERIAL_FORCE_INHERIT

path.OnTransition = highlightPartEnteringPath

def OnRun():
  pass

# undo highlight
# create an event handler for the OnPhysicalTransition event of the path
# the event handler should get the material of a part entering the path and assign that same material back to the part when it leaves the path
origin_materials = {}

def undoHighlightPartLeavingPath(path, part, isPartArriving):
  if isPartArriving:
    origin_materials[part] = part.NodeMaterial
  elif not isPartArriving:
    part.NodeMaterial = origin_materials.get(part)
    part.MaterialInheritance = VC_MATERIAL_FORCE_INHERIT

path.OnPhysicalTransition = undoHighlightPartLeavingPath
