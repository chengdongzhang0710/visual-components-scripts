from vcScript import *

comp = getComponent()

# joints are controlled by robot controller
# robotController = comp.findBehaviour("Controller")  # refer component graph
robotController = comp.findBehavioursByType(VC_ROBOTCONTROLLER)[0]

# find all robot joints
print len(robotController.Joints)

# find all internal joints
internal_joints = []
for joint in robotController.Joints:
  if not joint.ExternalController:
    internal_joints.append(joint)

print len(internal_joints)

# find all external joints
external_joints = []
for joint in robotController.Joints:
  if joint.ExternalController:
    external_joints.append(joint)

print len(external_joints)

# define a funtion to capture all internal joints in robot
def getInternalJointsInRobot(rc):
  return list(filter(lambda x: x.ExternalController == None, rc.Joints))

print len(getInternalJointsInRobot(robotController))

# define a function to capture all external joints in robot
def getExternalJointsInRobot(rc):
  return list(filter(lambda x: x.ExternalController != None, rc.Joints))

print len(getExternalJointsInRobot(robotController))

# change joint values
for joint in getInternalJointsInRobot(robotController):
  joint.CurrentValue = 0

# important! we need to render the 3D world after we set joint values
getApplication().render()

for joint in getExternalJointsInRobot(robotController):
  joint.CurrentValue = 500

getApplication().render()

# degree of freedom (dof)
# in most case, the root node will not have a joint
print comp.Dof  # -> None

# it is recommended to use dof to set joint values for internal joints
# for external joints, just use robot controller as above way
comp.findNode("Axis 1").Dof.VALUE = 90
getApplication().render()

# define a function to capture all nodes in component, not in other components such as positioners or tools
def getAllNodesInComponent(comp, nodes=[], includeRootNode=False):
  if not nodes:
    nodes = []
  
  if includeRootNode == True:
    nodes.append(comp)
  
  for node in comp.Children:
    if node.Component == comp.Component:  # otherwise the node is from different components
      nodes.append(node)
      if node.Children:
        getAllNodesInComponent(node, nodes)
  
  return nodes

print len(getAllNodesInComponent(comp))

# define a function to capture all dof in component
# important! a node with a fixed joint will also have its dof property set to None
def getAllDofInComponent(comp):
  dof_list = map(lambda x: x.Dof, getAllNodesInComponent(comp))
  return list(filter(lambda x: x != None, dof_list))

print len(getAllDofInComponent(comp))

for dof in getAllDofInComponent(comp):
  dof.VALUE = 0

getApplication().render()
