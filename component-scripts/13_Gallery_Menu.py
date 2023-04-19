# copy code to "__init__.py" in My Commands folder under Visual Components workspace and restart the application

from vcApplication import addMenuItem, loadCommand, getApplicationPath

cmduri = getApplicationPath() + "example.py"
cmd = loadCommand("AddRobotVariable", cmduri)

# default Visual Components icons are in folder "D:\Program Files\MideaCloud\MIoT.VC Premium 4.2\Icons"

# use d path in svg file to indicate location (open the svg file using text editor)
icon_path = "M16,9H9v7H7V9H0V7h7V0h2v7h7V9z"

addMenuItem("VcTabTeach/rGroup", "Add-Ons", -1, "gmTool", "", "", "", "GalleryMenuTool")

addMenuItem("VcTabTeach/rGroup/Variable", "Add", -1, "AddRobotVariable", "Add a global variable to robot program", "rAddArrow", "gmTool", "GalleryMenuToolItem")

addMenuItem("VcTabTeach/rGroup/Variable", "Delete", -1, "", "Delete a global variable from robot program", "rDelete", "gmTool", "GalleryMenuToolItem")

addMenuItem("VcTabTeach/rGroup/Schema", "Add position data", -1, "", "", icon_path, "gmTool", "GalleryMenuToolItem")

# new file
# save file as a command file "example.py" in My Commands folder
from vcCommand import *

def printOutput():
  cmd = getCommand()
  app = cmd.Application
  output = app.messageBox
  print output

addState(printOutput)
