from vcScript import *

comp = getComponent()
robotExecutor = comp.findBehavioursByType("rRobotExecutor")[0]
robotProgram = robotExecutor.Program
mainRoutine = robotProgram.MainRoutine

# write statements to main routine
# clear all statements in main routine
# to avoid repeatly add same statements to main routine each time compiling the Python file
mainRoutine.clear()

# print statement
statement = mainRoutine.addStatement(VC_STATEMENT_PRINT)
statement.Message = "Hello World"

# delay statement
# 0 is the index where to insert the statement, default is inserting at the end
statement = mainRoutine.addStatement(VC_STATEMENT_DELAY, 0)
statement.Delay = 2.0  # real number

# motion statement
statement = mainRoutine.addStatement(VC_STATEMENT_PTPMOTION)
print statement.Positions  # vc has already added a sample position point P1
position = statement.Positions[0]

# change P1's position using position matrix
pos_matrix = position.PositionInWorld
pos_matrix.translateRel(1000, 0, 1000)  # translate relative to current location
pos_matrix.rotateRelY(180.0)  # rotate relative to Y axis
position.PositionInWorld = pos_matrix

# teach robot to pick a cube
app = getApplication()
cube = app.findComponent("Cube")
pos_matrix = cube.PositionMatrix
cube_center = cube.BoundCenter
pos_matrix.translateRel(cube_center.X, cube_center.Y, cube_center.Z * 2)
pos_matrix.rotateRelY(180.0)
position.PositionInWorld = pos_matrix

# add new routine
# note that same sub routine will repeatly be added each time compiling the Python file
subRoutine = robotProgram.findRoutine("Example")
if subRoutine:
  subRoutine.clear()
else:
  subRoutine = robotProgram.addRoutine("Example")

statement = subRoutine.addStatement(VC_STATEMENT_PTPMOTION)
position = statement.Positions[0]
position.PositionInWorld = pos_matrix

# delete all sub routine in robot program
for subRoutine in robotProgram.Routines:
  robotProgram.deleteRoutine(subRoutine)
